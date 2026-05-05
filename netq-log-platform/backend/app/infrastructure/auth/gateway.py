from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from app.core.config import Settings
from app.infrastructure.auth.ldap_client import LdapDirectoryClient


@dataclass
class SessionCookie:
    name: str
    value: str
    max_age: int


@dataclass
class AuthenticatedSession:
    domain: str
    username: str
    cookie: SessionCookie
    last_activity_at: datetime


class AuthProviderUnavailableError(Exception):
    pass


class AuthGateway:
    def is_user_allowed(self, username: str) -> bool:
        raise NotImplementedError

    def authenticate(self, domain: str, username: str, password: str) -> bool:
        raise NotImplementedError

    def create_session(self, domain: str, username: str) -> AuthenticatedSession:
        raise NotImplementedError

    def get_session(self, session_token: str | None) -> AuthenticatedSession | None:
        raise NotImplementedError

    def refresh_session(self, session_token: str | None) -> AuthenticatedSession | None:
        raise NotImplementedError

    def clear_session(self, session_token: str | None) -> None:
        raise NotImplementedError


class InMemoryAuthGateway(AuthGateway):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._sessions: dict[str, AuthenticatedSession] = {}

    def is_user_allowed(self, username: str) -> bool:
        if not self.settings.allowed_users:
            return True
        return username in self.settings.allowed_users

    def authenticate(self, domain: str, username: str, password: str) -> bool:
        mock_password = self.settings.mock_password_value
        return bool(domain and username and mock_password and password == mock_password)

    def create_session(self, domain: str, username: str) -> AuthenticatedSession:
        token = token_urlsafe(24)
        session = AuthenticatedSession(
            domain=domain,
            username=username,
            cookie=SessionCookie(
                name=self.settings.session_cookie_name,
                value=token,
                max_age=self.settings.session_idle_timeout_seconds,
            ),
            last_activity_at=datetime.now(UTC),
        )
        self._sessions[token] = session
        return session

    def get_session(self, session_token: str | None) -> AuthenticatedSession | None:
        return self._get_active_session(session_token)

    def refresh_session(self, session_token: str | None) -> AuthenticatedSession | None:
        session = self._get_active_session(session_token)
        if session is None:
            return None
        session.last_activity_at = datetime.now(UTC)
        session.cookie.max_age = self.settings.session_idle_timeout_seconds
        self._sessions[session.cookie.value] = session
        return session

    def clear_session(self, session_token: str | None) -> None:
        if session_token:
            self._sessions.pop(session_token, None)

    def _get_active_session(self, session_token: str | None) -> AuthenticatedSession | None:
        if not session_token:
            return None
        session = self._sessions.get(session_token)
        if session is None:
            return None
        if self._is_expired(session):
            self._sessions.pop(session_token, None)
            return None
        return session

    def _is_expired(self, session: AuthenticatedSession) -> bool:
        expires_at = session.last_activity_at + timedelta(
            seconds=self.settings.session_idle_timeout_seconds
        )
        return datetime.now(UTC) > expires_at


class LdapAuthGateway(InMemoryAuthGateway):
    def __init__(self, settings: Settings, ldap_client: LdapDirectoryClient) -> None:
        super().__init__(settings)
        self.ldap_client = ldap_client

    def authenticate(self, domain: str, username: str, password: str) -> bool:
        try:
            return self.ldap_client.authenticate(
                domain=domain,
                username=username,
                password=password,
            )
        except RuntimeError as exc:
            raise AuthProviderUnavailableError(str(exc)) from exc
