import pytest

from app.application.auth.service import reset_auth_service_cache
from app.core.config import reset_settings_cache


@pytest.fixture(autouse=True)
def isolate_test_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NETQ_AUTH_PROVIDER", "mock")
    monkeypatch.setenv("NETQ_ALLOWED_USERS", "jdoe,operator")
    monkeypatch.delenv("NETQ_LEGACY_CONFIG_FILE", raising=False)
    reset_settings_cache()
    reset_auth_service_cache()
    yield
    reset_settings_cache()
    reset_auth_service_cache()
