"""
Auth
"""
import os
import secrets
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# from src.models import RefreshToken


from .config.database import engine, get_session
import jwt
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
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

# def login_db(user: str, passwrd: str, db: Session = Depends(get_session)):
#     from .models import User
#     auth_details = AuthDetails(username=user, password=passwrd)
#     user_db  = db.query(User).filter_by(username=auth_details.username).first() 
#     if (user_db is None) or (
#         not AuthHandler.verify_password(auth_details.password, user.password)
#     ) or (not user_db.is_active):
#         return Response(status_code=status.HTTP_401_UNAUTHORIZED)
#     token = AuthHandler.encode_token(user.id)
#     refresh_token = AuthHandler.refresh_token(token)
#     return {
#         "token": token,
#         "refresh_token": refresh_token,
#     }



def perform_login(username: str, password: str):
    from .router import login_user
    auth_details = AuthDetails(username=username, password=password)
    print(auth_details)
    # db = get_session()
    return login_user(auth_details)

users = {
    "admin": {
        "name": "Admin",
        "avatar": None,
        "roles": ["read", "create", "edit", "delete", "action_make_published"],
    },
    "viewer": {"name": "Viewer", "avatar": "guest.png", "roles": ["read"]},
}


class MyAuthProvider(AuthProvider):
    from src.models import RefreshToken
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
    db: Session,
        ) -> Response:
        from src.models import User, RefreshToken

        user = db.query(User).filter_by(username=username).first()
        if user and self.verify_password(password, user.password):
            access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )

            refresh_token = self.create_refresh_token(user.id, db)
            db.add(RefreshToken(user_id=user.id, token=refresh_token))
            db.commit()

            tokens = {
                "token": access_token,
                "refresh_token": refresh_token
            }
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            return tokens

        raise LoginFailed("Invalid username or password")


    # async def login(
    #     self,
    #     username: str,
    #     password: str,
    #     remember_me: bool,
    #     request: Request,
    #     response: Response,
    #     db: Session, 
    # ) -> Response:
    #     from src.models import User
    #     # if len(username) < 3:
    #     #     """Form data validation"""
    #     #     raise FormValidationError(
    #     #         {"username": "Ensure username has at least 03 characters"}
    #     #     )
    #     # #Aquí entra funcion login#
        
    #     # # if username in users and password == "gsCS7QAdJj":
    #     # #     """Save `username` in session"""
    #     # #     request.session.update({"username": username})
    #     # #     return response
    #     # if username is not None and password is not None:
           
    #     #     """Save `username` in session"""
    #     #     request.session.update({"username": username})
    #     #     if perform_login(username, password) is not None:
    #     #         request.session.update({"username": username})
    #     #         return response
    #     #     # return response
    #     # raise LoginFailed("Invalid username or password")
    #      # Consultar la base de datos para el usuario con el nombre de usuario proporcionado
    #     user = db.query(User).filter_by(username=username).first()
    #     # Verificar si el usuario existe y la contraseña es correcta
    #     if user and self.verify_password(password, user.password):
    #         # Guardar el nombre de usuario en la sesión
    #         request.session.update({"username": username})
    #         return response

    #     # Si el usuario o la contraseña son inválidos, lanzar una excepción de fallo de inicio de sesión
    #     raise LoginFailed("Invalid username or password")

    def create_refresh_token(self, user_id: int, db: Session):
        # Generate a secure, random token
        refresh_token = secrets.token_hex(32)

        # Store the refresh token in the database
        new_refresh_token = RefreshToken(user_id=user_id, token=refresh_token)
        db.add(new_refresh_token)
        db.commit()

        return refresh_token
    
    def create_access_token(self, data: dict, expires_delta: datetime.timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    
    # async def refresh_token(self, request: Request, response: Response) -> Response:
    #     refresh_token = request.cookies.get("refresh_token")

    #     if not refresh_token:
    #         raise HTTPException(status_code=400, detail="Refresh token not found")

    #     try:
    #         payload = self.verify_refresh_token(refresh_token)
    #         new_access_token = self.create_access_token({"sub": payload["sub"]})

    #         response.set_cookie("access_token", new_access_token, httponly=True)
    #         return response

    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail="Refresh token") from e

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
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