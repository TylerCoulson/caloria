from fastapi import Depends, APIRouter

from .db import User
from .schemas import UserCreate, UserRead, UserUpdate
from .users import cookie_auth_backend, jwt_auth_backend, current_active_user, fastapi_users, get_current_profile
from app.models import Profile

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(jwt_auth_backend), prefix="/auth/jwt", tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_auth_router(cookie_auth_backend), prefix="/auth/cookie", tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@auth_router.get("/authenticated-route")
async def authenticated_route(profile: Profile = Depends(get_current_profile)):
    return profile


