"""
Spaced Repetition Algorithm (SM-2 adapted).

This module implements an adapted SM-2 algorithm for scheduling word reviews.
The algorithm calculates optimal intervals between reviews based on user performance.
"""

from datetime import datetime, timedelta
from app.database.models.user_word import UserWord


class SpacedRepetition:
    """
    Spaced repetition scheduler using adapted SM-2 algorithm.
    
    Quality ratings:
    0 - Complete failure
    1 - Wrong, but recognized
    2 - Wrong, but easy to remember
    3 - Correct with difficulty
    4 - Correct with hesitation
    5 - Perfect response
    """
    
    # Minimum and maximum intervals
    MIN_INTERVAL = 1  # day
    MAX_INTERVAL = 365  # days
    
    # Mastery thresholds
    MASTERY_THRESHOLD = 85.0  # Word is considered "learned"
    
    @staticmethod
    def calculate_quality(is_correct: bool, response_time: float | None = None) -> int:
        """
        Calculate quality rating based on correctness and response time.
        
        Args:
            is_correct: Whether the answer was correct
            response_time: Time taken to answer in seconds
            
        Returns:
            Quality rating 0-5
        """
        if not is_correct:
            return 1  # Wrong answer
        
        # Correct answer - adjust based on response time
        if response_time is None:
            return 4  # Default for correct answer
        
        if response_time < 2.0:
            return 5  # Very fast - perfect
        elif response_time < 5.0:
            return 4  # Fast - good
        elif response_time < 10.0:
            return 3  # Medium - okay
        else:
            return 2  # Slow - difficult
    
    @staticmethod
    def update_user_word(user_word: UserWord, quality: int) -> UserWord:
        """
        Update UserWord with new review data using SM-2 algorithm.
        
        Args:
            user_word: UserWord instance to update
            quality: Quality rating 0-5
            
        Returns:
            Updated UserWord instance
        """
        # Update statistics
        user_word.times_shown += 1
        if quality >= 3:
            user_word.times_correct += 1
            user_word.repetitions += 1
        else:
            user_word.times_wrong += 1
        
        # Update ease factor (SM-2 formula)
        if quality >= 3:
            # Good response - increase ease factor
            user_word.ease_factor = max(
                1.3,
                user_word.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )
        else:
            # Bad response - decrease ease factor
            user_word.ease_factor = max(1.3, user_word.ease_factor - 0.2)
        
        # Calculate next interval
        if quality < 3:
            # Failed - reset interval to 1 day
            user_word.interval_days = SpacedRepetition.MIN_INTERVAL
        else:
            # Success - increase interval
            if user_word.repetitions == 1:
                user_word.interval_days = 1
            elif user_word.repetitions == 2:
                user_word.interval_days = 6
            else:
                user_word.interval_days = round(user_word.interval_days * user_word.ease_factor)
            
            # Cap at maximum
            user_word.interval_days = min(user_word.interval_days, SpacedRepetition.MAX_INTERVAL)
        
        # Calculate next review date
        user_word.next_review_date = datetime.utcnow() + timedelta(days=user_word.interval_days)
        user_word.last_review_date = datetime.utcnow()
        
        # Update mastery scores based on exercise type
        SpacedRepetition._update_mastery_scores(user_word, quality)
        
        # Check if word is learned
        if user_word.mastery_level >= SpacedRepetition.MASTERY_THRESHOLD:
            user_word.is_learned = 1
        
        return user_word
    
    @staticmethod
    def _update_mastery_scores(user_word: UserWord, quality: int):
        """Update mastery scores based on quality."""
        # Convert quality (0-5) to score increment (0-100)
        score_increment = (quality / 5.0) * 20  # Max 20 points per review
        
        # Update overall mastery (weighted average)
        old_mastery = user_word.mastery_level
        total_reviews = user_word.times_shown
        
        if total_reviews == 1:
            user_word.mastery_level = score_increment * 5
        else:
            # Weighted moving average
            weight = 1.0 / min(total_reviews, 10)  # Recent reviews matter more
            user_word.mastery_level = old_mastery * (1 - weight) + score_increment * 5 * weight
        
        # Cap at 100
        user_word.mastery_level = min(100.0, user_word.mastery_level)
    
    @staticmethod
    def get_priority_score(user_word: UserWord) -> float:
        """
        Calculate priority score for review scheduling.
        
        Lower mastery + overdue = higher priority.
        
        Returns:
            Priority score (higher = more urgent)
        """
        now = datetime.utcnow()
        
        # Base priority from mastery (lower mastery = higher priority)
        mastery_priority = 100 - user_word.mastery_level
        
        # Overdue bonus
        overdue_days = 0
        if user_word.next_review_date:
            overdue_delta = now - user_word.next_review_date
            overdue_days = max(0, overdue_delta.days)
        
        overdue_priority = min(overdue_days * 10, 50)  # Cap at 50
        
        # Error rate bonus
        if user_word.times_shown > 0:
            error_rate = user_word.times_wrong / user_word.times_shown
            error_priority = error_rate * 30
        else:
            error_priority = 0
        
        return mastery_priority + overdue_priority + error_priority
