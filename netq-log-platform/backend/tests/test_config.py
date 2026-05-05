from pathlib import Path

from app.core.config import Settings


def test_settings_read_values_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("NETQ_ENVIRONMENT", "test")
    monkeypatch.setenv("NETQ_AUTH_PROVIDER", "ldap")
    monkeypatch.setenv("NETQ_SESSION_COOKIE_NAME", "custom_session")
    monkeypatch.setenv("NETQ_ALLOWED_USERS", "alice,bob")
    monkeypatch.setenv("NETQ_MONGO_PROD_URL", "https://mongo.example")

    settings = Settings(_env_file=None)

    assert settings.environment == "test"
    assert settings.auth_provider == "ldap"
    assert settings.session_cookie_name == "custom_session"
    assert settings.allowed_users == ["alice", "bob"]
    assert settings.mongo_prod_url == "https://mongo.example"


def test_settings_load_file_backed_secrets_and_user_list(
    monkeypatch,
    tmp_path: Path,
) -> None:
    allowed_users_file = tmp_path / "allowed-users"
    allowed_users_file.write_text("operator\n# comment\nsupport\n", encoding="utf-8")

    mock_password_file = tmp_path / "mock-password"
    mock_password_file.write_text("file-secret\n", encoding="utf-8")

    ldap_password_file = tmp_path / "ldap-password"
    ldap_password_file.write_text("ldap-secret\n", encoding="utf-8")

    monkeypatch.setenv("NETQ_ALLOWED_USERS_FILE", str(allowed_users_file))
    monkeypatch.delenv("NETQ_ALLOWED_USERS", raising=False)
    monkeypatch.setenv("NETQ_MOCK_PASSWORD_FILE", str(mock_password_file))
    monkeypatch.setenv("NETQ_LDAP_USER_DB_PASSWORD_FILE", str(ldap_password_file))

    settings = Settings(_env_file=None, mock_password=None, ldap_user_db_password=None)

    assert settings.allowed_users == ["operator", "support"]
    assert settings.mock_password_value == "file-secret"
    assert settings.ldap_user_db_password_value == "ldap-secret"


def test_settings_read_dotenv_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "NETQ_ENVIRONMENT=prod",
                "NETQ_KEEP_ALIVE_INTERVAL_SECONDS=600",
                "NETQ_SIGRA_URL=https://sigra.example",
            ]
        ),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.environment == "prod"
    assert settings.keep_alive_interval_seconds == 600
    assert settings.sigra_url == "https://sigra.example"


def test_settings_can_load_legacy_netqtools_json_config(tmp_path: Path) -> None:
    legacy_config = tmp_path / "app_DEV.json"
    legacy_config.write_text(
        """
        {
          "configuration": {
            "mongoProd": "https://mongo-prod.example/netq/test/",
            "mongoProdBasicAuth": true,
            "mongoProdBasicAuthUser": "netq",
            "mongoProdBasicAuthPass": "mongo-secret",
            "auditProd": "https://audit-prod.example/netq/audit/",
            "auditProdBasicAuth": false,
            "auditQA": "https://audit-qa.example/netq/audit/",
            "mongoQA": "https://mongo-qa.example/netq/test/",
            "auxURL": "?related=true",
            "auxURLaudit": "?cache=true",
            "sapaUrl": "https://sapa.example/query?id_servico=",
            "sigraApp": "NETQ",
            "sigraCodeApp": "99",
            "sigraUrl": "https://sigra.example/service",
            "sigraAction": "https://sigra.example/action",
            "sigraTimeout": "30",
            "ldap_server": "ldap.example.internal",
            "ldap_port": 3269,
            "ldap_user_dn": "CN=service-account,OU=Applications,DC=example,DC=com",
            "ldap_user_db_password": "ldap-secret"
          }
        }
        """,
        encoding="utf-8",
    )

    settings = Settings(_env_file=None, legacy_config_file=legacy_config)

    assert settings.mongo_prod_url == "https://mongo-prod.example/netq/test/"
    assert settings.mongo_prod_basic_auth_enabled is True
    assert settings.mongo_prod_basic_auth_user == "netq"
    assert settings.mongo_prod_basic_auth_pass.get_secret_value() == "mongo-secret"
    assert settings.audit_prod_url == "https://audit-prod.example/netq/audit/"
    assert settings.mongo_qa_url == "https://mongo-qa.example/netq/test/"
    assert settings.audit_qa_url == "https://audit-qa.example/netq/audit/"
    assert settings.sapa_url == "https://sapa.example/query?id_servico="
    assert settings.sigra_url == "https://sigra.example/service"
    assert settings.sigra_action == "https://sigra.example/action"
    assert settings.sigra_timeout_seconds == 30
    assert settings.ldap_server == "ldap.example.internal"
    assert settings.ldap_port == 3269
    assert settings.ldap_user_dn == "CN=service-account,OU=Applications,DC=example,DC=com"
    assert settings.ldap_user_db_password.get_secret_value() == "ldap-secret"
