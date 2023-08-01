from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin
from starlette.responses import JSONResponse, RedirectResponse

from .models import User
from .utils import get_user_db, get_jwt_strategy
from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH


async def get_user_manager(user_db=Depends(get_user_db)):
    return UserManager(user_db)
