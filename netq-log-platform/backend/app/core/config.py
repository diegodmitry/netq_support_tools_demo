import json
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NETQ_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "dev"
    api_prefix: str = "/api/v1"

    session_cookie_name: str = "netq_session"
    session_idle_timeout_seconds: int = 28800
    keep_alive_interval_seconds: int = 300
    outbound_http_timeout_seconds: float = 5.0
    outbound_http_max_retries: int = 2
    outbound_http_retry_backoff_seconds: float = 0.2

    auth_provider: str = "mock"
    auth_domains: list[dict[str, str | bool]] = Field(
        default_factory=lambda: [
            {"value": "ptportugal", "label": "PTPORTUGAL", "default": True},
            {"value": "ptc", "label": "PTC", "default": False},
            {"value": "ptcom", "label": "PTCOM", "default": False},
            {"value": "ptin", "label": "PTIN", "default": False},
            {"value": "ptsi", "label": "PTSI", "default": False},
            {"value": "tmn", "label": "TMN", "default": False},
        ]
    )
    allowed_users: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["jdoe", "operator"]
    )
    allowed_users_file: Path | None = None
    legacy_config_file: Path | None = None

    mock_password: SecretStr | None = SecretStr("secret")
    mock_password_file: Path | None = None

    ldap_server: str | None = None
    ldap_port: int = 3269
    ldap_use_ssl: bool = True
    ldap_validate_certificates: bool = True
    ldap_connect_timeout_seconds: int = 5
    ldap_user_dn: str | None = None
    ldap_user_db_password: SecretStr | None = None
    ldap_user_db_password_file: Path | None = None

    mongo_prod_url: str | None = None
    mongo_prod_basic_auth_enabled: bool = False
    mongo_prod_basic_auth_user: str | None = None
    mongo_prod_basic_auth_pass: SecretStr | None = None
    mongo_prod_basic_auth_pass_file: Path | None = None

    audit_prod_url: str | None = None
    audit_prod_basic_auth_enabled: bool = False
    audit_prod_basic_auth_user: str | None = None
    audit_prod_basic_auth_pass: SecretStr | None = None
    audit_prod_basic_auth_pass_file: Path | None = None

    mongo_qa_url: str | None = None
    audit_qa_url: str | None = None
    aux_url: str = "?related=true"
    aux_url_audit: str = "?cache=true"
    sapa_url: str | None = None

    sigra_app: str | None = None
    sigra_code_app: str | None = None
    sigra_url: str | None = None
    sigra_action: str | None = None
    sigra_timeout_seconds: int = 30

    @field_validator("allowed_users", mode="before")
    @classmethod
    def parse_allowed_users(cls, value: object) -> object:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def load_file_backed_settings(self) -> "Settings":
        if self.legacy_config_file:
            self._load_legacy_json_config(self.legacy_config_file)

        if self.allowed_users_file:
            self.allowed_users = self._read_list_file(self.allowed_users_file)

        self.mock_password = self._resolve_secret(
            self.mock_password,
            self.mock_password_file,
        )
        self.ldap_user_db_password = self._resolve_secret(
            self.ldap_user_db_password,
            self.ldap_user_db_password_file,
        )
        self.mongo_prod_basic_auth_pass = self._resolve_secret(
            self.mongo_prod_basic_auth_pass,
            self.mongo_prod_basic_auth_pass_file,
        )
        self.audit_prod_basic_auth_pass = self._resolve_secret(
            self.audit_prod_basic_auth_pass,
            self.audit_prod_basic_auth_pass_file,
        )
        return self

    @property
    def mock_password_value(self) -> str | None:
        if self.mock_password is None:
            return None
        return self.mock_password.get_secret_value()

    @property
    def ldap_user_db_password_value(self) -> str | None:
        if self.ldap_user_db_password is None:
            return None
        return self.ldap_user_db_password.get_secret_value()

    @property
    def mongo_prod_basic_auth_pass_value(self) -> str | None:
        if self.mongo_prod_basic_auth_pass is None:
            return None
        return self.mongo_prod_basic_auth_pass.get_secret_value()

    @property
    def audit_prod_basic_auth_pass_value(self) -> str | None:
        if self.audit_prod_basic_auth_pass is None:
            return None
        return self.audit_prod_basic_auth_pass.get_secret_value()

    @staticmethod
    def _resolve_secret(
        current_value: SecretStr | None,
        file_path: Path | None,
    ) -> SecretStr | None:
        if current_value is not None:
            return current_value
        if file_path is None:
            return None
        return SecretStr(Settings._read_secret_file(file_path))

    @staticmethod
    def _read_secret_file(file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8").strip()

    @staticmethod
    def _read_list_file(file_path: Path) -> list[str]:
        return [
            line.strip()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    def _load_legacy_json_config(self, file_path: Path) -> None:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        configuration = payload.get("configuration", {})
        explicit_fields = set(self.model_fields_set)

        legacy_to_settings_map = {
            "mongoProd": "mongo_prod_url",
            "mongoProdBasicAuth": "mongo_prod_basic_auth_enabled",
            "mongoProdBasicAuthUser": "mongo_prod_basic_auth_user",
            "mongoProdBasicAuthPass": "mongo_prod_basic_auth_pass",
            "auditProd": "audit_prod_url",
            "auditProdBasicAuth": "audit_prod_basic_auth_enabled",
            "auditProdBasicAuthUser": "audit_prod_basic_auth_user",
            "auditProdBasicAuthPass": "audit_prod_basic_auth_pass",
            "mongoQA": "mongo_qa_url",
            "auditQA": "audit_qa_url",
            "auxURL": "aux_url",
            "auxURLaudit": "aux_url_audit",
            "sapaUrl": "sapa_url",
            "sigraApp": "sigra_app",
            "sigraCodeApp": "sigra_code_app",
            "sigraUrl": "sigra_url",
            "sigraAction": "sigra_action",
            "sigraTimeout": "sigra_timeout_seconds",
            "ldap_server": "ldap_server",
            "ldap_port": "ldap_port",
            "ldap_user_dn": "ldap_user_dn",
            "ldap_user_db_password": "ldap_user_db_password",
        }

        for legacy_key, settings_key in legacy_to_settings_map.items():
            if settings_key in explicit_fields or legacy_key not in configuration:
                continue

            value = configuration[legacy_key]
            if settings_key in {
                "mongo_prod_basic_auth_pass",
                "audit_prod_basic_auth_pass",
                "ldap_user_db_password",
            }:
                setattr(self, settings_key, SecretStr(str(value)))
                continue

            if settings_key == "sigra_timeout_seconds":
                setattr(self, settings_key, int(value))
                continue

            setattr(self, settings_key, value)


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
