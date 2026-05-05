from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache

from fastapi import Request, Response, status

from app.core.config import Settings, get_settings
from app.domain.auth.errors import AuthAPIError
from app.domain.auth.schemas import (
    AuthConfigResponse,
    DomainOption,
    ErrorDetail,
    ErrorResponse,
    KeepAliveResponse,
    LoginRequest,
    LoginSuccessResponse,
    LogoutResponse,
    PermissionInfo,
    SessionInfo,
    SessionResponse,
    UserInfo,
)
from app.infrastructure.auth.gateway import (
    AuthenticatedSession,
    AuthGateway,
    AuthProviderUnavailableError,
    InMemoryAuthGateway,
    LdapAuthGateway,
    SessionCookie,
)
from app.infrastructure.auth.ldap_client import LdapDirectoryClient


@dataclass
class AuthActionResult:
    body: LoginSuccessResponse | KeepAliveResponse
    session_cookie: SessionCookie


class AuthService:
    def __init__(self, gateway: AuthGateway, settings: Settings) -> None:
        self.gateway = gateway
        self.settings = settings

    def login(self, payload: LoginRequest) -> AuthActionResult:
        if not payload.username or not payload.password:
            raise self._error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                code="AUTH_VALIDATION_ERROR",
                message="Credenciais incompletas.",
                fields={
                    "username": "required" if not payload.username else None,
                    "password": "required" if not payload.password else None,
                },
            )

        if not self.gateway.is_user_allowed(payload.username):
            raise self._error(
                status.HTTP_403_FORBIDDEN,
                code="AUTH_FORBIDDEN",
                message="Erro na autenticacao.",
            )

        try:
            authenticated_ok = self.gateway.authenticate(
                payload.domain,
                payload.username,
                payload.password,
            )
        except AuthProviderUnavailableError as exc:
            raise self._error(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                code="AUTH_PROVIDER_UNAVAILABLE",
                message="Erro na autenticacao.",
            ) from exc

        if not authenticated_ok:
            raise self._error(
                status.HTTP_401_UNAUTHORIZED,
                code="AUTH_INVALID_CREDENTIALS",
                message="Erro na autenticacao.",
            )

        authenticated = self.gateway.create_session(payload.domain, payload.username)
        body = LoginSuccessResponse(
            authenticated=True,
            user=self._to_user(authenticated),
            session=self._to_session_info(authenticated),
            redirectTo="/app",
        )
        return AuthActionResult(body=body, session_cookie=authenticated.cookie)

    def get_session(self, request: Request) -> SessionResponse:
        session = self.gateway.get_session(self._get_session_token(request))
        if session is None:
            raise self._error(
                status.HTTP_401_UNAUTHORIZED,
                code="SESSION_NOT_AUTHENTICATED",
                message="Sessao expirada ou inexistente.",
            )
        return SessionResponse(
            authenticated=True,
            user=self._to_user(session),
            session=self._to_session_info(session),
        )

    def keep_alive(self, request: Request) -> AuthActionResult:
        session = self.gateway.refresh_session(self._get_session_token(request))
        if session is None:
            raise self._error(
                status.HTTP_401_UNAUTHORIZED,
                code="SESSION_EXPIRED",
                message="Sessao expirada ou inexistente.",
            )
        body = KeepAliveResponse(
            ok=True,
            session=self._to_session_info(session, include_refresh_time=True),
        )
        return AuthActionResult(body=body, session_cookie=session.cookie)

    def logout(self) -> LogoutResponse:
        return LogoutResponse(ok=True, loggedOut=True, redirectTo="/login")

    def logout_by_request(self, request: Request) -> LogoutResponse:
        self.gateway.clear_session(self._get_session_token(request))
        return LogoutResponse(ok=True, loggedOut=True, redirectTo="/login")

    def get_config(self) -> AuthConfigResponse:
        return AuthConfigResponse(
            domains=[
                DomainOption(
                    value=domain["value"],
                    label=domain["label"],
                    default=domain["default"],
                )
                for domain in self.settings.auth_domains
            ]
        )

    def apply_session_cookie(self, response: Response, cookie: SessionCookie) -> None:
        response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            max_age=cookie.max_age,
            httponly=True,
            secure=self.settings.environment != "dev",
            samesite="lax",
            path="/",
        )

    def clear_session_cookie(self, response: Response) -> None:
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
        response.delete_cookie(key=self.settings.session_cookie_name, path="/")

    def _get_session_token(self, request: Request) -> str | None:
        return request.cookies.get(self.settings.session_cookie_name)

    def _to_user(self, session: AuthenticatedSession) -> UserInfo:
        return UserInfo(
            username=session.username,
            displayName=session.username,
            domain=session.domain,
            permissions=PermissionInfo(allowed=True, roles=["user"]),
        )

    def _to_session_info(
        self,
        session: AuthenticatedSession,
        *,
        include_refresh_time: bool = False,
    ) -> SessionInfo:
        refreshed_at = datetime.now(UTC) if include_refresh_time else None
        return SessionInfo(
            authenticated=True,
            expiresInSeconds=self.settings.session_idle_timeout_seconds,
            idleTimeoutSeconds=self.settings.session_idle_timeout_seconds,
            keepAliveIntervalSeconds=self.settings.keep_alive_interval_seconds,
            lastActivityAt=session.last_activity_at,
            refreshedAt=refreshed_at,
        )

    def _error(
        self,
        status_code: int,
        *,
        code: str,
        message: str,
        fields: dict[str, str | None] | None = None,
    ) -> AuthAPIError:
        field_errors = None
        if fields:
            field_errors = {key: value for key, value in fields.items() if value is not None}
        detail = ErrorResponse(
            authenticated=False if code.startswith("AUTH") or code.startswith("SESSION") else None,
            ok=False if code.startswith("SESSION") else None,
            error=ErrorDetail(code=code, message=message, fields=field_errors),
        )
        return AuthAPIError(status_code=status_code, body=detail.model_dump(exclude_none=True))


def build_auth_gateway(settings: Settings) -> AuthGateway:
    if settings.auth_provider == "ldap":
        return LdapAuthGateway(settings, LdapDirectoryClient(settings))
    return InMemoryAuthGateway(settings)


@lru_cache
def get_auth_gateway() -> AuthGateway:
    settings = get_settings()
    return build_auth_gateway(settings)


def reset_auth_service_cache() -> None:
    get_auth_gateway.cache_clear()


def get_auth_service() -> AuthService:
    settings = get_settings()
    gateway = get_auth_gateway()
    return AuthService(gateway, settings)
