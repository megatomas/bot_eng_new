from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database.base import Base


class UserWord(Base):
    """Tracks user's progress for each word."""
    __tablename__ = "user_words"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Mastery levels (0-100) for each skill
    recognition_score = Column(Float, default=0.0)  # English → Russian
    recall_score = Column(Float, default=0.0)       # Russian → English
    listening_score = Column(Float, default=0.0)    # Audio → meaning
    production_score = Column(Float, default=0.0)   # Free production
    
    # Overall mastery
    mastery_level = Column(Float, default=0.0)  # 0-100
    
    # Spaced repetition data (SM-2 / FSRS adapted)
    ease_factor = Column(Float, default=2.5)  # SM-2 ease factor
    interval_days = Column(Integer, default=0)  # Current interval
    repetitions = Column(Integer, default=0)  # Successful repetitions
    
    # Scheduling
    next_review_date = Column(DateTime(timezone=True), index=True)
    last_review_date = Column(DateTime(timezone=True))
    
    # Statistics
    times_shown = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    times_wrong = Column(Integer, default=0)
    average_response_time = Column(Float, default=0.0)  # seconds
    
    # Status
    is_learned = Column(Integer, default=0)  # mastery >= 85
    is_active = Column(Integer, default=1)  # in rotation
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'word_id', name='uq_user_word'),
    )
    
    def __repr__(self):
        return f"<UserWord(user_id={self.user_id}, word_id={self.word_id}, mastery={self.mastery_level:.1f})>"
