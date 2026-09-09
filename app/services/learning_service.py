"""
Learning Service - orchestrates the learning process.

This service manages:
- Selecting words for learning
- Generating exercises
- Processing answers
- Updating user progress
"""

import random
from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.database.models.word import Word
from app.database.models.user_word import UserWord
from app.repositories.user_repo import UserRepository
from app.repositories.word_repo import WordRepository
from app.repositories.review_repo import ReviewRepository
from app.services.spaced_repetition import SpacedRepetition


class LearningService:
    """Main learning orchestration service."""
    
    # Exercise types
    RECOGNITION = "recognition"      # English → Russian (multiple choice)
    RECALL = "recall"                # Russian → English (type answer)
    LISTENING = "listening"          # Audio → meaning
    PRODUCTION = "production"        # Free sentence construction
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.word_repo = WordRepository(session)
        self.review_repo = ReviewRepository(session)
        self.srs = SpacedRepetition()
    
    async def get_next_words(
        self,
        user: User,
        count: int = 5,
    ) -> List[Word]:
        """Get next words to learn for user."""
        return await self.word_repo.get_new_words_for_user(
            user_id=user.id,
            level=user.current_level,
            limit=count,
        )
    
    async def get_words_for_review(
        self,
        user: User,
        count: int = 20,
    ) -> List[UserWord]:
        """Get words due for review."""
        return await self.word_repo.get_words_due_for_review(
            user_id=user.id,
            limit=count,
        )
    
    async def create_user_word(self, user_id: int, word_id: int) -> UserWord:
        """Create a new UserWord entry."""
        user_word = UserWord(
            user_id=user_id,
            word_id=word_id,
            next_review_date=datetime.utcnow(),  # Review immediately
        )
        self.session.add(user_word)
        await self.session.flush()
        return user_word
    
    async def generate_exercise(
        self,
        word: Word,
        user: User,
        exercise_type: str | None = None,
    ) -> Dict:
        """
        Generate an exercise for a word.
        
        Returns:
            Dict with exercise data
        """
        if exercise_type is None:
            # Choose exercise type based on user's weak areas
            exercise_type = self._choose_exercise_type(word, user)
        
        if exercise_type == self.RECOGNITION:
            return await self._generate_recognition_exercise(word)
        elif exercise_type == self.RECALL:
            return await self._generate_recall_exercise(word)
        elif exercise_type == self.LISTENING:
            return await self._generate_listening_exercise(word)
        elif exercise_type == self.PRODUCTION:
            return await self._generate_production_exercise(word)
        else:
            return await self._generate_recognition_exercise(word)
    
    def _choose_exercise_type(self, word: Word, user: User) -> str:
        """Choose exercise type based on user's mastery levels."""
        # Get user's word progress if exists
        # For now, use simple logic
        types = [self.RECOGNITION, self.RECALL, self.LISTENING]
        
        # If user is advanced, include production
        if user.current_level in ["B1", "B2", "C1"]:
            types.append(self.PRODUCTION)
        
        return random.choice(types)
    
    async def _generate_recognition_exercise(self, word: Word) -> Dict:
        """Generate recognition exercise: English → Russian (multiple choice)."""
        # Get distractors
        distractors = await self.word_repo.get_words_for_level(
            level=word.level,
            limit=3,
            exclude_word_ids=[word.id],
        )
        
        options = [word.translation] + [w.translation for w in distractors]
        random.shuffle(options)
        
        return {
            "type": self.RECOGNITION,
            "word": word,
            "question": f"What does '{word.word}' mean?",
            "options": options,
            "correct_answer": word.translation,
        }
    
    async def _generate_recall_exercise(self, word: Word) -> Dict:
        """Generate recall exercise: Russian → English (type answer)."""
        return {
            "type": self.RECALL,
            "word": word,
            "question": f"How do you say '{word.translation}' in English?",
            "correct_answer": word.word,
            "hint": word.pronunciation,
        }
    
    async def _generate_listening_exercise(self, word: Word) -> Dict:
        """Generate listening exercise: Audio → meaning."""
        # Get distractors
        distractors = await self.word_repo.get_words_for_level(
            level=word.level,
            limit=3,
            exclude_word_ids=[word.id],
        )
        
        options = [word.word] + [w.word for w in distractors]
        random.shuffle(options)
        
        return {
            "type": self.LISTENING,
            "word": word,
            "question": "Listen and choose the correct word",
            "audio_text": word.word,  # Will be converted to audio
            "options": options,
            "correct_answer": word.word,
        }
    
    async def _generate_production_exercise(self, word: Word) -> Dict:
        """Generate production exercise: Create a sentence."""
        example = word.examples[0] if word.examples else None
        
        return {
            "type": self.PRODUCTION,
            "word": word,
            "question": f"Make a sentence using the word '{word.word}'",
            "example": example,
            "correct_answer": None,  # Will be checked by AI
        }
    
    async def process_answer(
        self,
        user: User,
        word: Word,
        exercise_type: str,
        user_answer: str,
        correct_answer: str,
        response_time: float | None = None,
    ) -> Tuple[bool, Dict]:
        """
        Process user's answer and update progress.
        
        Returns:
            Tuple of (is_correct, feedback_dict)
        """
        # Check if answer is correct
        is_correct = self._check_answer(user_answer, correct_answer, exercise_type)
        
        # Calculate quality
        quality = self.srs.calculate_quality(is_correct, response_time)
        
        # Get or create UserWord
        user_word = await self._get_or_create_user_word(user.id, word.id)
        
        # Update with SRS
        self.srs.update_user_word(user_word, quality)
        
        # Create review record
        await self.review_repo.create_review(
            user_id=user.id,
            word_id=word.id,
            exercise_type=exercise_type,
            is_correct=is_correct,
            response_time=response_time,
            user_answer=user_answer,
            correct_answer=correct_answer,
            quality=quality,
        )
        
        # Update user stats
        await self.user_repo.update_stats(user, is_correct)
        await self.user_repo.update_activity(user)
        
        # Record mistake if wrong
        if not is_correct:
            error_type = self._classify_error(user_answer, correct_answer, exercise_type)
            await self.review_repo.create_mistake(
                user_id=user.id,
                word_id=word.id,
                error_type=error_type,
                user_input=user_answer,
                expected=correct_answer,
                exercise_type=exercise_type,
            )
        
        # Calculate XP
        xp = 10 if is_correct else 2
        await self.user_repo.add_xp(user, xp)
        
        # Update daily progress
        await self.review_repo.update_daily_progress(
            user_id=user.id,
            words_reviewed=1,
            correct=1 if is_correct else 0,
            wrong=0 if is_correct else 1,
            xp=xp,
        )
        
        # Generate feedback
        feedback = self._generate_feedback(is_correct, word, user_answer, correct_answer)
        
        return is_correct, feedback
    
    def _check_answer(self, user_answer: str, correct_answer: str, exercise_type: str) -> bool:
        """Check if user's answer is correct."""
        if exercise_type == self.PRODUCTION:
            # For production, we'll use AI to check
            # For now, simple check
            return correct_answer.lower() in user_answer.lower()
        
        # Normalize answers
        user_clean = user_answer.strip().lower()
        correct_clean = correct_answer.strip().lower()
        
        return user_clean == correct_clean
    
    def _classify_error(self, user_answer: str, correct_answer: str, exercise_type: str) -> str:
        """Classify the type of error."""
        # Simple classification - can be enhanced
        if exercise_type in [self.RECOGNITION, self.LISTENING]:
            return "vocabulary"
        elif exercise_type == self.RECALL:
            return "spelling"
        else:
            return "grammar"
    
    def _generate_feedback(
        self,
        is_correct: bool,
        word: Word,
        user_answer: str,
        correct_answer: str,
    ) -> Dict:
        """Generate feedback for the user."""
        if is_correct:
            return {
                "is_correct": True,
                "message": "✅ Correct!",
                "word": word.word,
                "translation": word.translation,
            }
        else:
            return {
                "is_correct": False,
                "message": f"❌ Not quite. The correct answer is: {correct_answer}",
                "word": word.word,
                "translation": word.translation,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
            }
    
    async def _get_or_create_user_word(self, user_id: int, word_id: int) -> UserWord:
        """Get existing UserWord or create new one."""
        from sqlalchemy import select
        
        result = await self.session.execute(
            select(UserWord).where(
                UserWord.user_id == user_id,
                UserWord.word_id == word_id,
            )
        )
        user_word = result.scalar_one_or_none()
        
        if not user_word:
            user_word = await self.create_user_word(user_id, word_id)
        
        return user_word
