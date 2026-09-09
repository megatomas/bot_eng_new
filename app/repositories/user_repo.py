from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from datetime import datetime


class UserRepository:
    """Repository for User operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by Telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
    ) -> User:
        """Create a new user."""
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_activity_date=datetime.utcnow(),
        )
        self.session.add(user)
        await self.session.flush()
        return user
    
    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
    ) -> User:
        """Get existing user or create new one."""
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(telegram_id, username, first_name)
        return user
    
    async def update_activity(self, user: User):
        """Update user's last activity timestamp."""
        user.last_activity_date = datetime.utcnow()
        await self.session.flush()
    
    async def update_streak(self, user: User):
        """Update user's streak based on last practice date."""
        today = datetime.utcnow().date()
        
        if user.last_practice_date:
            last_date = user.last_practice_date.date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                pass  # Already practiced today
            elif days_diff == 1:
                user.streak_days += 1
            else:
                user.streak_days = 1  # Reset streak
        else:
            user.streak_days = 1
        
        user.last_practice_date = datetime.utcnow()
        await self.session.flush()
    
    async def add_xp(self, user: User, xp: int):
        """Add XP to user."""
        user.total_xp += xp
        await self.session.flush()
    
    async def update_stats(self, user: User, correct: bool):
        """Update user's answer statistics."""
        user.total_reviews += 1
        if correct:
            user.total_correct += 1
        else:
            user.total_wrong += 1
        await self.session.flush()
