from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.review import Review, Mistake, DailyProgress
from datetime import datetime, date
from typing import List, Dict


class ReviewRepository:
    """Repository for Review operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_review(
        self,
        user_id: int,
        word_id: int,
        exercise_type: str,
        is_correct: bool,
        response_time: float | None = None,
        user_answer: str | None = None,
        correct_answer: str | None = None,
        quality: int | None = None,
    ) -> Review:
        """Create a new review record."""
        review = Review(
            user_id=user_id,
            word_id=word_id,
            exercise_type=exercise_type,
            is_correct=1 if is_correct else 0,
            response_time=response_time,
            user_answer=user_answer,
            correct_answer=correct_answer,
            quality=quality,
        )
        self.session.add(review)
        await self.session.flush()
        return review
    
    async def get_user_accuracy(self, user_id: int) -> float:
        """Calculate user's overall accuracy."""
        result = await self.session.execute(
            select(
                func.count(Review.id),
                func.sum(Review.is_correct)
            ).where(Review.user_id == user_id)
        )
        row = result.one()
        total = row[0] or 0
        correct = row[1] or 0
        
        if total == 0:
            return 0.0
        return (correct / total) * 100
    
    async def get_accuracy_by_type(self, user_id: int) -> Dict[str, float]:
        """Get accuracy broken down by exercise type."""
        result = await self.session.execute(
            select(
                Review.exercise_type,
                func.count(Review.id),
                func.sum(Review.is_correct)
            )
            .where(Review.user_id == user_id)
            .group_by(Review.exercise_type)
        )
        
        accuracy_by_type = {}
        for row in result.all():
            exercise_type, total, correct = row
            if total > 0:
                accuracy_by_type[exercise_type] = (correct / total) * 100
        
        return accuracy_by_type
    
    async def create_mistake(
        self,
        user_id: int,
        word_id: int | None,
        error_type: str,
        user_input: str | None = None,
        expected: str | None = None,
        explanation: str | None = None,
        exercise_type: str | None = None,
        sentence_context: str | None = None,
    ) -> Mistake:
        """Record a mistake."""
        mistake = Mistake(
            user_id=user_id,
            word_id=word_id,
            error_type=error_type,
            user_input=user_input,
            expected=expected,
            explanation=explanation,
            exercise_type=exercise_type,
            sentence_context=sentence_context,
        )
        self.session.add(mistake)
        await self.session.flush()
        return mistake
    
    async def get_mistake_profile(self, user_id: int) -> Dict[str, int]:
        """Get user's mistake profile (counts by error type)."""
        result = await self.session.execute(
            select(
                Mistake.error_type,
                func.count(Mistake.id)
            )
            .where(Mistake.user_id == user_id)
            .group_by(Mistake.error_type)
            .order_by(func.count(Mistake.id).desc())
        )
        
        return {row[0]: row[1] for row in result.all()}
    
    async def update_daily_progress(
        self,
        user_id: int,
        minutes_spent: int = 0,
        new_words: int = 0,
        words_reviewed: int = 0,
        correct: int = 0,
        wrong: int = 0,
        xp: int = 0,
    ):
        """Update or create daily progress record."""
        today = date.today()
        
        result = await self.session.execute(
            select(DailyProgress).where(
                and_(
                    DailyProgress.user_id == user_id,
                    func.date(DailyProgress.date) == today,
                )
            )
        )
        progress = result.scalar_one_or_none()
        
        if not progress:
            progress = DailyProgress(
                user_id=user_id,
                date=datetime.combine(today, datetime.min.time()),
            )
            self.session.add(progress)
        
        progress.minutes_spent += minutes_spent
        progress.new_words_learned += new_words
        progress.words_reviewed += words_reviewed
        progress.correct_answers += correct
        progress.wrong_answers += wrong
        progress.xp_earned += xp
        
        await self.session.flush()
