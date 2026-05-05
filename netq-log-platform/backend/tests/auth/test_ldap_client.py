from types import SimpleNamespace

import pytest

from app.core.config import Settings
from app.infrastructure.auth.ldap_client import LdapDirectoryClient


class FakeBindError(Exception):
    pass


class FakeLdapError(Exception):
    pass


class FakeConnection:
    def __init__(self, *_args, **_kwargs) -> None:
        self.bound = True
        self.unbound = False
        self.rebind_calls: list[dict[str, str]] = []

    def unbind(self) -> None:
        self.unbound = True

    def rebind(self, **kwargs) -> bool:
        self.rebind_calls.append(kwargs)
        self.bound = True
        return True


def build_fake_ldap3() -> SimpleNamespace:
    return SimpleNamespace(
        SIMPLE="SIMPLE",
        Server=lambda *args, **kwargs: {"args": args, "kwargs": kwargs},
        Connection=lambda *args, **kwargs: FakeConnection(*args, **kwargs),
        Tls=lambda **kwargs: {"tls": kwargs},
        utils=SimpleNamespace(
            dn=SimpleNamespace(escape_rdn=lambda value: value.replace(",", "\\,"))
        ),
        core=SimpleNamespace(
            exceptions=SimpleNamespace(
                LDAPBindError=FakeBindError,
                LDAPException=FakeLdapError,
            )
        ),
    )


def test_ldap_client_authenticates_with_escaped_username(monkeypatch) -> None:
    captured: dict[str, str] = {}
    fake_ldap3 = build_fake_ldap3()

    def connection_factory(_server, **kwargs):
        captured["user"] = kwargs["user"]
        return FakeConnection()

    settings = Settings(
        _env_file=None,
        auth_provider="ldap",
        ldap_server="ldap.example",
        ldap_validate_certificates=False,
    )
    client = LdapDirectoryClient(
        settings,
        connection_factory=connection_factory,
    )
    monkeypatch.setattr(
        "app.infrastructure.auth.ldap_client.LdapDirectoryClient._import_ldap3",
        staticmethod(lambda: fake_ldap3),
    )

    authenticated = client.authenticate(
        domain="ptportugal",
        username="john,doe",
        password="secret",
    )

    assert authenticated is True
    assert captured["user"] == "ptportugal\\john\\,doe"


def test_ldap_client_binds_with_service_account_then_rebinds_user(monkeypatch) -> None:
    captured: dict[str, object] = {}
    fake_ldap3 = build_fake_ldap3()

    def connection_factory(_server, **kwargs):
        captured["initial_user"] = kwargs["user"]
        captured["initial_password"] = kwargs["password"]
        connection = FakeConnection()
        captured["connection"] = connection
        return connection

    settings = Settings(
        _env_file=None,
        auth_provider="ldap",
        ldap_server="ldap.example",
        ldap_user_dn="CN=svc,OU=Apps,DC=example,DC=com",
        ldap_user_db_password="service-secret",
    )
    client = LdapDirectoryClient(settings, connection_factory=connection_factory)
    monkeypatch.setattr(
        "app.infrastructure.auth.ldap_client.LdapDirectoryClient._import_ldap3",
        staticmethod(lambda: fake_ldap3),
    )

    authenticated = client.authenticate(
        domain="ptportugal",
        username="john,doe",
        password="user-secret",
    )

    assert authenticated is True
    assert captured["initial_user"] == "CN=svc,OU=Apps,DC=example,DC=com"
    assert captured["initial_password"] == "service-secret"
    connection = captured["connection"]
    assert isinstance(connection, FakeConnection)
    assert connection.rebind_calls == [
        {
            "user": "ptportugal\\john\\,doe",
            "password": "user-secret",
            "authentication": "SIMPLE",
        }
    ]
    assert connection.unbound is True


def test_ldap_client_returns_false_for_invalid_credentials(monkeypatch) -> None:
    fake_ldap3 = build_fake_ldap3()

    def connection_factory(_server, **_kwargs):
        raise FakeBindError("invalid credentials")

    settings = Settings(_env_file=None, auth_provider="ldap", ldap_server="ldap.example")
    client = LdapDirectoryClient(settings, connection_factory=connection_factory)
    monkeypatch.setattr(
        "app.infrastructure.auth.ldap_client.LdapDirectoryClient._import_ldap3",
        staticmethod(lambda: fake_ldap3),
    )

    assert client.authenticate(domain="ptportugal", username="jdoe", password="wrong") is False


def test_ldap_client_returns_false_when_user_rebind_fails(monkeypatch) -> None:
    fake_ldap3 = build_fake_ldap3()

    class InvalidRebindConnection(FakeConnection):
        def rebind(self, **_kwargs) -> bool:
            raise FakeBindError("invalid credentials")

    settings = Settings(
        _env_file=None,
        auth_provider="ldap",
        ldap_server="ldap.example",
        ldap_user_dn="CN=svc,OU=Apps,DC=example,DC=com",
        ldap_user_db_password="service-secret",
    )
    client = LdapDirectoryClient(
        settings,
        connection_factory=lambda _server, **_kwargs: InvalidRebindConnection(),
    )
    monkeypatch.setattr(
        "app.infrastructure.auth.ldap_client.LdapDirectoryClient._import_ldap3",
        staticmethod(lambda: fake_ldap3),
    )

    assert client.authenticate(domain="ptportugal", username="jdoe", password="wrong") is False


def test_ldap_client_raises_runtime_error_when_provider_is_unavailable(monkeypatch) -> None:
    fake_ldap3 = build_fake_ldap3()

    def connection_factory(_server, **_kwargs):
        raise FakeLdapError("network error")

    settings = Settings(_env_file=None, auth_provider="ldap", ldap_server="ldap.example")
    client = LdapDirectoryClient(settings, connection_factory=connection_factory)
    monkeypatch.setattr(
        "app.infrastructure.auth.ldap_client.LdapDirectoryClient._import_ldap3",
        staticmethod(lambda: fake_ldap3),
    )

    with pytest.raises(RuntimeError, match="LDAP provider unavailable"):
        client.authenticate(domain="ptportugal", username="jdoe", password="secret")
