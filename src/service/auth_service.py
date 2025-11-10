import hashlib
import secrets

import jwt

from src.config import JWT_ALGORITHM, JWT_SECRET_KEY
from src.repository.model.user import User
from src.repository.user_repository import UserRepository
from src.service.error import ConflictError, UnauthorizedError


class AuthService:
    _ACTIVE_TOKENS: dict[int, set[str]] = {}

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, username: str, password: str) -> User:
        if await self.user_repo.username_exists(username):
            raise ConflictError("User with this username already exists")

        password_hash = self._hash_password(password)
        return await self.user_repo.create_user(username, password_hash)

    async def verify_credentials(self, username: str, password: str) -> User:
        user = await self.user_repo.get_user_by_username(username)
        if not user:
            raise UnauthorizedError("Incorrect username or password")

        if not self._verify_password(password, user.password_hash):
            raise UnauthorizedError("Incorrect username or password")

        return user

    def create_access_token(self, user: User) -> str:
        payload = {"sub": str(user.id), "username": user.username}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        self._store_token(user.id, token)
        return token

    async def get_user_from_token(self, token: str) -> User:
        payload = self._decode_token(token)

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid token payload")

        user = await self.user_repo.get_user_by_id(int(user_id))
        if not user:
            raise UnauthorizedError("Invalid token payload")

        if not self._is_token_active(user.id, token):
            raise UnauthorizedError("Token is inactive or has been logged out")

        return user

    def invalidate_user_tokens(self, user_id: int) -> None:
        AuthService._ACTIVE_TOKENS.pop(user_id, None)

    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        salt, hash_value = hashed_password.split("$")
        hash_obj = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 100000)
        return hash_obj.hex() == hash_value

    def _store_token(self, user_id: int, token: str) -> None:
        tokens = AuthService._ACTIVE_TOKENS.get(user_id)
        if not tokens:
            tokens = set()
            AuthService._ACTIVE_TOKENS[user_id] = tokens
        tokens.add(token)

    def _is_token_active(self, user_id: int, token: str) -> bool:
        tokens = AuthService._ACTIVE_TOKENS.get(user_id)
        return token in tokens if tokens else False

    def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError as exc:
            raise UnauthorizedError("Invalid or expired token") from exc
