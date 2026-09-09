from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.sql import func
from app.database.base import Base


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    
    # Level tracking
    current_level = Column(String(10), default="A0")  # A0, A1, A2, B1, B2, C1
    vocabulary_level = Column(String(10), default="A0")
    grammar_level = Column(String(10), default="A0")
    listening_level = Column(String(10), default="A0")
    speaking_level = Column(String(10), default="A0")
    
    # Progress
    total_xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime)
    last_practice_date = Column(DateTime)
    
    # Settings
    daily_goal_minutes = Column(Integer, default=15)
    morning_reminder_time = Column(String(10))  # HH:MM
    evening_reminder_time = Column(String(10))   # HH:MM
    
    # Stats
    total_words_learned = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_wrong = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, level={self.current_level})>"
