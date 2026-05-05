from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from app.application.auth.service import AuthService, get_auth_service
from app.domain.auth.schemas import (
    AuthConfigResponse,
    ErrorResponse,
    KeepAliveResponse,
    LoginRequest,
    LoginSuccessResponse,
    LogoutResponse,
    SessionResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/login",
    response_model=LoginSuccessResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def login(
    payload: LoginRequest,
    response: Response,
    service: AuthServiceDep,
) -> LoginSuccessResponse:
    result = service.login(payload)
    service.apply_session_cookie(response, result.session_cookie)
    return result.body


@router.get(
    "/session",
    response_model=SessionResponse,
    responses={401: {"model": ErrorResponse}},
)
def get_session(
    request: Request,
    service: AuthServiceDep,
) -> SessionResponse:
    return service.get_session(request)


@router.post(
    "/keep-alive",
    response_model=KeepAliveResponse,
    responses={401: {"model": ErrorResponse}},
)
def keep_alive(
    request: Request,
    response: Response,
    service: AuthServiceDep,
) -> KeepAliveResponse:
    result = service.keep_alive(request)
    service.apply_session_cookie(response, result.session_cookie)
    return result.body


@router.delete("/session", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    response: Response,
    service: AuthServiceDep,
) -> LogoutResponse:
    body = service.logout_by_request(request)
    service.clear_session_cookie(response)
    return body


@router.get("/config", response_model=AuthConfigResponse)
def auth_config(
    service: AuthServiceDep,
) -> AuthConfigResponse:
    return service.get_config()
