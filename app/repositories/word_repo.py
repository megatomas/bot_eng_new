from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.word import Word
from app.database.models.user_word import UserWord
from datetime import datetime
from typing import List


class WordRepository:
    """Repository for Word operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, word_id: int) -> Word | None:
        """Get word by ID."""
        result = await self.session.execute(
            select(Word).where(Word.id == word_id)
        )
        return result.scalar_one_or_none()
    
    async def get_words_for_level(
        self,
        level: str,
        limit: int = 10,
        exclude_word_ids: List[int] = None,
    ) -> List[Word]:
        """Get words for a specific level."""
        query = select(Word).where(Word.level == level)
        
        if exclude_word_ids:
            query = query.where(Word.id.notin_(exclude_word_ids))
        
        query = query.order_by(Word.frequency_rank.asc()).limit(limit)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_new_words_for_user(
        self,
        user_id: int,
        level: str,
        limit: int = 5,
    ) -> List[Word]:
        """Get new words that user hasn't learned yet."""
        # Get IDs of words user already has
        existing = await self.session.execute(
            select(UserWord.word_id).where(UserWord.user_id == user_id)
        )
        existing_ids = [row[0] for row in existing.all()]
        
        # Get new words
        query = select(Word).where(Word.level == level)
        if existing_ids:
            query = query.where(Word.id.notin_(existing_ids))
        
        query = query.order_by(Word.frequency_rank.asc()).limit(limit)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_words_due_for_review(self, user_id: int, limit: int = 20) -> List[UserWord]:
        """Get words that are due for review."""
        now = datetime.utcnow()
        
        result = await self.session.execute(
            select(UserWord)
            .where(
                and_(
                    UserWord.user_id == user_id,
                    UserWord.next_review_date <= now,
                    UserWord.is_active == 1,
                )
            )
            .order_by(UserWord.next_review_date.asc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_total_words_count(self) -> int:
        """Get total number of words in database."""
        result = await self.session.execute(
            select(func.count(Word.id))
        )
        return result.scalar()
    
    async def get_words_by_category(
        self,
        category: str,
        limit: int = 10,
    ) -> List[Word]:
        """Get words by category."""
        result = await self.session.execute(
            select(Word)
            .where(Word.category == category)
            .order_by(Word.frequency_rank.asc())
            .limit(limit)
        )
        return list(result.scalars().all())
