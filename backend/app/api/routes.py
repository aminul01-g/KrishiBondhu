from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from app.db import get_db
from app.models.db_models import Conversation

router = APIRouter()

@router.get("/conversations")
async def get_conversations(db: AsyncSession = Depends(get_db)):
    """
    Get all conversations from the database, ordered by created_at descending.
    Returns conversations with id, user_id, transcript, confidence, and media_url.
    Gracefully handles database connection errors.
    """
    # Check if database connection is available
    if db is None:
        print("Database not available - returning empty conversations list")
        return []
    
    try:
        result = await db.execute(
            select(Conversation).order_by(Conversation.created_at.desc())
        )
        conversations = result.scalars().all()
        return [
            {
                "id": conv.id,
                "user_id": conv.user_id,
                "transcript": conv.transcript,
                "confidence": conv.confidence,
                "media_url": conv.media_url,
                "tts_path": conv.tts_path,
                "metadata": conv.meta_data,  # Using meta_data from model, but returning as metadata in API
                "created_at": conv.created_at.isoformat() if conv.created_at else None
            }
            for conv in conversations
        ]
    except (OperationalError, ConnectionRefusedError, Exception) as e:
        # Database not available - return empty list instead of crashing
        print(f"Database connection error (conversations endpoint): {e}")
        print("Returning empty conversations list - database may not be running")
        return []
