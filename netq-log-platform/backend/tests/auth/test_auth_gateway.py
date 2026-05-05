from app.core.config import Settings
from app.infrastructure.auth.gateway import InMemoryAuthGateway


def test_allowed_users_can_be_bypassed_when_list_is_empty() -> None:
    settings = Settings(_env_file=None, allowed_users=[])
    gateway = InMemoryAuthGateway(settings)

    assert gateway.is_user_allowed("real-directory-user") is True


def test_allowed_users_are_enforced_when_list_is_configured() -> None:
    settings = Settings(_env_file=None, allowed_users=["jdoe"])
    gateway = InMemoryAuthGateway(settings)

    assert gateway.is_user_allowed("jdoe") is True
    assert gateway.is_user_allowed("other-user") is False
