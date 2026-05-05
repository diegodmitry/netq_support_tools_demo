import logging
from collections.abc import Callable
from ssl import CERT_NONE, CERT_REQUIRED, PROTOCOL_TLS_CLIENT
from typing import Any

from app.core.config import Settings

logger = logging.getLogger("netq.auth.ldap")


class LdapDirectoryClient:
    def __init__(
        self,
        settings: Settings,
        *,
        server_factory: Callable[..., Any] | None = None,
        connection_factory: Callable[..., Any] | None = None,
        escape_rdn: Callable[[str], str] | None = None,
        tls_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.settings = settings
        self._server_factory = server_factory
        self._connection_factory = connection_factory
        self._escape_rdn = escape_rdn
        self._tls_factory = tls_factory

    def authenticate(self, *, domain: str, username: str, password: str) -> bool:
        if not domain or not username or not password:
            return False
        if not self.settings.ldap_server:
            raise RuntimeError("LDAP server is not configured.")

        ldap3 = self._import_ldap3()
        bind_user = f"{domain}\\{self._escape_username(username)}"
        server = self._build_server(ldap3)
        service_account_dn = self.settings.ldap_user_dn
        service_account_password = self.settings.ldap_user_db_password_value
        connection = None

        try:
            if service_account_dn and service_account_password:
                connection = self._build_connection(
                    ldap3=ldap3,
                    server=server,
                    bind_user=service_account_dn,
                    password=service_account_password,
                )
                return bool(
                    connection.rebind(
                        user=bind_user,
                        password=password,
                        authentication=ldap3.SIMPLE,
                    )
                )

            connection = self._build_connection(
                ldap3=ldap3,
                server=server,
                bind_user=bind_user,
                password=password,
            )
            return bool(connection.bound)
        except ldap3.core.exceptions.LDAPBindError:
            return False
        except ldap3.core.exceptions.LDAPException as exc:
            logger.warning("LDAP provider unavailable", extra={"event": "auth.ldap.unavailable"})
            raise RuntimeError("LDAP provider unavailable.") from exc
        finally:
            if connection is not None:
                connection.unbind()

    def _build_server(self, ldap3: Any) -> Any:
        tls_factory = self._tls_factory or ldap3.Tls
        validate_mode = CERT_REQUIRED if self.settings.ldap_validate_certificates else CERT_NONE
        tls_config = tls_factory(validate=validate_mode, version=PROTOCOL_TLS_CLIENT)

        server_factory = self._server_factory or ldap3.Server
        return server_factory(
            self.settings.ldap_server,
            port=self.settings.ldap_port,
            use_ssl=self.settings.ldap_use_ssl,
            connect_timeout=self.settings.ldap_connect_timeout_seconds,
            tls=tls_config,
        )

    def _build_connection(
        self,
        *,
        ldap3: Any,
        server: Any,
        bind_user: str,
        password: str,
    ) -> Any:
        connection_factory = self._connection_factory or ldap3.Connection
        return connection_factory(
            server,
            user=bind_user,
            password=password,
            auto_bind=True,
            raise_exceptions=True,
            authentication=ldap3.SIMPLE,
        )

    def _escape_username(self, username: str) -> str:
        if self._escape_rdn is not None:
            return self._escape_rdn(username)

        ldap3 = self._import_ldap3()
        return ldap3.utils.dn.escape_rdn(username)

    @staticmethod
    def _import_ldap3() -> Any:
        import ldap3

        return ldap3
