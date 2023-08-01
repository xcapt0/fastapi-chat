from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport

from .manager import get_user_manager
from .models import User
from .utils import get_jwt_strategy


cookie_transport = CookieTransport(cookie_name="secret", cookie_max_age=3600,
                                   cookie_samesite="none", cookie_domain="localhost")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
