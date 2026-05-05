from datetime import datetime

from pydantic import BaseModel, Field


class DomainOption(BaseModel):
    value: str
    label: str
    default: bool


class PermissionInfo(BaseModel):
    allowed: bool
    roles: list[str]


class UserInfo(BaseModel):
    username: str
    displayName: str
    domain: str
    permissions: PermissionInfo


class SessionInfo(BaseModel):
    authenticated: bool
    expiresInSeconds: int
    idleTimeoutSeconds: int
    keepAliveIntervalSeconds: int
    lastActivityAt: datetime | None = None
    refreshedAt: datetime | None = None


class LoginRequest(BaseModel):
    domain: str = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginSuccessResponse(BaseModel):
    authenticated: bool
    user: UserInfo
    session: SessionInfo
    redirectTo: str


class SessionResponse(BaseModel):
    authenticated: bool
    user: UserInfo
    session: SessionInfo


class KeepAliveResponse(BaseModel):
    ok: bool
    session: SessionInfo


class LogoutResponse(BaseModel):
    ok: bool
    loggedOut: bool
    redirectTo: str


class AuthConfigResponse(BaseModel):
    domains: list[DomainOption]


class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: dict[str, str] | None = None


class ErrorResponse(BaseModel):
    authenticated: bool | None = None
    ok: bool | None = None
    error: ErrorDetail
