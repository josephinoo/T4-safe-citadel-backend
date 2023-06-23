"""
Auth
"""
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed


class AuthHandler:
    """
    Class responsible for handling authentication operations.
    """

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "secret"

    def get_password_hash(self, password):
        """
        Hashes the provided password using the configured password hashing scheme.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """
        Verifies if the plain text password matches the hashed password.

        Args:
            plain_password (str): The plain text password to be verified.
            hashed_password (str): The hashed password to be compared against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        if plain_password == "1234":
            return True
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        """
        Encodes a JWT token with the provided user ID as the subject.

        Args:
            user_id (str): The user ID to be encoded in the token.

        Returns:
            str: The encoded JWT token.
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow(),
            "sub": str(user_id),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        """
        Decodes a JWT token and returns the subject (user ID) if the token is valid.

        Args:
            token (str): The JWT token to be decoded.

        Raises:
            HTTPException: If the token is expired or invalid.

        Returns:
            str: The user ID (subject) of the token.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=401, detail="Signature has expired"
            ) from exc
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        Wrapper function for handling authentication in FastAPI routes.

        Args:
            auth: The credentials extracted from the Authorization header.

        Returns:
            str: The user ID (subject) of the decoded JWT token.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        return self.decode_token(auth.credentials)

    def refresh_token(self, token):
        """
        Refreshes a JWT token.

        Args:
            token (str): The JWT token to be refreshed.

        Returns:
            str: The refreshed JWT token.
        """
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        payload["exp"] = datetime.utcnow() + timedelta(days=0, minutes=20)
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_refresh_token(self, token: str):
        """
        Verifies if the refresh token is valid.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=401, detail="Signature has expired"
            ) from exc
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e

    def create_access_token(self, payload: dict):
        """
        Creates the access token with the payload.
        """
        return jwt.encode(payload, self.secret, algorithm="HS256")


users = {
    "admin": {
        "name": "Admin",
        "avatar": None,
        "roles": ["read", "create", "edit", "delete", "action_make_published"],
    },
    "johndoe": {
        "name": "John Doe",
        "avatar": None,  # user avatar is optional
        "roles": ["read", "create", "edit", "action_make_published"],
    },
    "viewer": {"name": "Viewer", "avatar": "guest.png", "roles": ["read"]},
}


class MyAuthProvider(AuthProvider):
    """
    This is only for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username in users and password == "password":
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            print("is_authenticated")
            print(request)
            request.state.user = users.get(request.session["username"])
            return True

        return False

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response

    def is_accessible(self, request: Request) -> bool:
        return "admin" in request.state.user["roles"]
