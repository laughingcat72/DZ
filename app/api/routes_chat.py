from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import (
    ChatMessagePublic,
    ChatRequest,
    ChatResponse,
    ClearHistoryResponse,
)
from app.usecases.chat import ChatUseCase

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    data: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
) -> ChatResponse:
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=data.prompt,
            system=data.system,
            max_history=data.max_history,
            temperature=data.temperature,
        )
    except ExternalServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    return ChatResponse(answer=answer)


@router.get(
    "/history",
    response_model=list[ChatMessagePublic],
)
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
    limit: int = Query(default=50, ge=1, le=100),
) -> list[ChatMessagePublic]:
    messages = await chat_usecase.get_history(
        user_id=user_id,
        limit=limit,
    )

    return [ChatMessagePublic.model_validate(message) for message in messages]


@router.delete(
    "/history",
    response_model=ClearHistoryResponse,
)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
) -> ClearHistoryResponse:
    deleted = await chat_usecase.clear_history(user_id)

    return ClearHistoryResponse(
        status="ok",
        deleted=deleted,
    )
