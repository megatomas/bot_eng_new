from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Word(Base):
    """Word/phrase model with rich linguistic data."""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    
    # Core data
    word = Column(String(255), nullable=False, index=True)
    translation = Column(Text, nullable=False)
    part_of_speech = Column(String(50))  # noun, verb, adjective, etc.
    
    # Classification
    frequency_rank = Column(Integer, index=True)  # 1-10000
    level = Column(String(10), default="A1", index=True)  # A0, A1, A2, B1, B2, C1
    importance = Column(Float, default=5.0)  # 1-10
    
    # Pronunciation
    pronunciation = Column(String(255))  # IPA or phonetic
    
    # Rich content (stored as JSON)
    examples = Column(JSON, default=[])  # [{"en": "...", "ru": "..."}]
    common_phrases = Column(JSON, default=[])  # ["run out of", "run late"]
    collocations = Column(JSON, default=[])  # ["run a business", "run a program"]
    synonyms = Column(JSON, default=[])  # ["sprint", "jog"]
    antonyms = Column(JSON, default=[])  # ["walk", "stop"]
    forms = Column(JSON, default=[])  # ["run", "ran", "running"]
    
    # Categorization
    tags = Column(JSON, default=[])  # ["daily", "movement", "work"]
    category = Column(String(100), index=True)  # main category
    
    # Flags
    is_phrasal_verb = Column(Integer, default=0)
    is_idiom = Column(Integer, default=0)
    is_slang = Column(Integer, default=0)
    is_contraction = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Word(id={self.id}, word='{self.word}', level={self.level})>"
