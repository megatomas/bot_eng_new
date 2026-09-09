from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.base import Base


class Review(Base):
    """History of all review attempts."""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Exercise type
    exercise_type = Column(String(50), nullable=False)  # recognition, recall, listening, production
    
    # Result
    is_correct = Column(Integer, nullable=False)  # 0 or 1
    response_time = Column(Float)  # seconds
    user_answer = Column(Text)
    correct_answer = Column(Text)
    
    # Quality (for SM-2: 0-5)
    quality = Column(Integer)  # 0=forgot, 5=perfect
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<Review(user_id={self.user_id}, word_id={self.word_id}, correct={self.is_correct})>"


class Mistake(Base):
    """Tracks user mistakes for error analysis."""
    __tablename__ = "mistakes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Error classification
    error_type = Column(String(50), nullable=False, index=True)
    # Types: vocabulary, grammar, word_order, article, preposition,
    #        pronunciation, listening, spelling, tense, naturalness
    
    # Details
    user_input = Column(Text)
    expected = Column(Text)
    explanation = Column(Text)
    
    # Context
    exercise_type = Column(String(50))
    sentence_context = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<Mistake(user_id={self.user_id}, type={self.error_type})>"


class DailyProgress(Base):
    """Daily activity tracking."""
    __tablename__ = "daily_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Activity
    minutes_spent = Column(Integer, default=0)
    new_words_learned = Column(Integer, default=0)
    words_reviewed = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)
    
    # XP
    xp_earned = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<DailyProgress(user_id={self.user_id}, date={self.date})>"
