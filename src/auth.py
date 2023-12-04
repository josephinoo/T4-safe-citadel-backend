"""
Auth
"""
import os
import secrets
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session



from .config.database import engine, get_session
import jwt
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from .schema import AuthDetails
os.environ["TZ"] = "America/Guayaquil"
# time.tzset()


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
            "exp": datetime.utcnow() + timedelta(days=1, minutes=20),
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
        payload["exp"] = datetime.utcnow() + timedelta(days=2, minutes=20)
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




class MyAuthProvider(AuthProvider):
    from src.models import User, Role
    login_path = '/login' 
    logout_path = '/logout'
    allow_paths = ['/login', '/logout']
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, engine):
       self.engine = engine


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def is_admin(self, role):
        return role == self.Role.ADMIN
    
    session = Session(bind=engine)
    
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        
        
        user = self.session.query(self.User).filter_by(username=username).first()
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )
        if user and self.verify_password(password, user.password) and self.is_admin(user.role):
            """Save `username` in session"""
            request.session.update({"username": username})
            return response
        raise LoginFailed("Usuario o contraseña incorrecta.")


    async def is_authenticated(self, request) -> bool:
        username = request.session.get("username", None)
        user = self.session.query(self.User).filter_by(username=username).first()
        if user:  
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = user
            return True

        return False

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user.name)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response

    def is_accessible(self, request: Request) -> bool:
        return "ADMIN" in request.state.user.role