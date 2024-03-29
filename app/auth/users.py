from typing import Optional, Annotated, Any, Dict

from fastapi import Depends, Request, Response, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, CookieTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase


from app import models, crud
from app.deps import get_db
from app.auth.email.email import send_email, EmailSchema
from .db import User, get_user_db
from .secrets import secrets

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = secrets['SECRET_KEY']
    verification_token_secret = secrets['SECRET_KEY']

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        await self.request_verify(user=user, request=request)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        email = EmailSchema(email=user.email)
        await send_email(email=email, request=request, _type="forgot", token=token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        email = EmailSchema(email=user.email)
        await send_email(email=email, request=request, _type="verify", token=token)

    async def on_after_login(
        self, user: User, request: Optional[Request] = None, response: Optional[Response] = None
    ) -> None:
        print(f'{user.email} has logged in')
        return
    
    async def validate_password(
        self, password: str, email: str
    ) -> None:
        """
        Validate a password.

        *You should overload this method to add your own validation logic.*

        :param password: The password to validate.
        :param user: The user associated to this password.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        print(f"the password is {password}")
        print(f"the user is {email}")
        return  # pragma: no cover

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful password reset.

        *You should overload this method to add your own logic.*

        :param user: The user that reset its password.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        print(f"The password for {user.email} been reset")
        return  # pragma: no cover
    
    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ) -> None:
        """
        Perform logic after successful user update.

        *You should overload this method to add your own logic.*

        :param user: The updated user
        :param update_dict: Dictionary with the updated user fields.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        print(user, update_dict)
        return  # pragma: no cover

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=secrets['SECRET_KEY'], lifetime_seconds=secrets['ACCESS_TOKEN_EXPIRE_SECONDS'])


jwt_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

session_transport = CookieTransport()
cookie_transport = CookieTransport(cookie_max_age=secrets['ACCESS_TOKEN_EXPIRE_SECONDS'])


session_auth_backend = AuthenticationBackend(
    name="session",
    transport=session_transport,
    get_strategy=get_jwt_strategy,
)

cookie_auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)



fastapi_users = FastAPIUsers[User, int](get_user_manager, [jwt_auth_backend, cookie_auth_backend, session_auth_backend])

current_active_user = fastapi_users.current_user(active=True, optional=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

async def get_current_profile(user: User = Depends(current_active_user), db = Depends(get_db)):
    """
    Retrieves the current profile of the user.
    Parameters:
        user (User): The user for whom to retrieve the profile. Defaults to the current active user.
        db: The database connection. Defaults to the database obtained from the get_db dependency.
    Returns:
        Profile: The profile object associated with the user.
    Raises:
        HTTPException: If the user does not have a profile.
    """

    if user is None:
        return None
    
    if user.profile is None:
        raise HTTPException(status_code=404, detail="Profile Not Found")
        
    return await crud.read(_id=user.profile.id, db=db, model=models.Profile, profile=user.profile)
    

Annotated_User = Annotated[models.User, Depends(current_active_user)]
Annotated_Superuser = Annotated[models.User, Depends(current_superuser)]
Annotated_Profile = Annotated[models.Profile, Depends(get_current_profile)]