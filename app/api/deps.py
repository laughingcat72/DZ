from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)


async def get_chat_message_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ChatMessageRepository:
    return ChatMessageRepository(session)


async def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthUseCase:
    return AuthUseCase(user_repository)


async def get_chat_usecase(
    message_repository: ChatMessageRepository = Depends(
        get_chat_message_repository),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    return ChatUseCase(
        message_repository=message_repository,
        openrouter_client=openrouter_client,
    )


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedError("Token subject is missing")

        return int(user_id)

    except (UnauthorizedError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
