from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(
        self,
        user_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )

        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)

        return message

    async def get_last_messages(
        self,
        user_id: int,
        limit: int,
    ) -> list[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.desc())
            .limit(limit),
        )

        messages = list(result.scalars().all())
        messages.reverse()

        return messages

    async def get_history(
        self,
        user_id: int,
        limit: int,
    ) -> list[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.asc())
            .limit(limit),
        )

        return list(result.scalars().all())

    async def delete_history(self, user_id: int) -> int:
        count_result = await self._session.execute(
            select(func.count(ChatMessage.id)).where(
                ChatMessage.user_id == user_id),
        )
        deleted_count = count_result.scalar_one()

        await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id),
        )
        await self._session.commit()

        return deleted_count
