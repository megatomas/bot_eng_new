import { useState, useCallback, useEffect } from 'react';
import { lessons, Word, Lesson } from '../data/lessons';

export type ExerciseType = 'translate_to_english' | 'translate_to_russian' | 'listen_and_choose' | 'type_word' | 'match_pairs';

export interface Exercise {
  type: ExerciseType;
  word: Word;
  options?: string[];
  question: string;
  correctAnswer: string;
}

export interface UserProgress {
  learnedWords: string[];
  correctAnswers: number;
  wrongAnswers: number;
  currentLessonIndex: number;
  currentWordIndex: number;
  streak: number;
  totalXP: number;
  level: number;
  lastPracticeDate: string;
  wordsToRepeat: string[];
}

const STORAGE_KEY = 'english_bot_progress';

const defaultProgress: UserProgress = {
  learnedWords: [],
  correctAnswers: 0,
  wrongAnswers: 0,
  currentLessonIndex: 0,
  currentWordIndex: 0,
  streak: 0,
  totalXP: 0,
  level: 1,
  lastPracticeDate: '',
  wordsToRepeat: [],
};

function loadProgress(): UserProgress {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (e) {
    console.error('Failed to load progress:', e);
  }
  return defaultProgress;
}

function saveProgress(progress: UserProgress) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  } catch (e) {
    console.error('Failed to save progress:', e);
  }
}

function generateExercise(word: Word, type: ExerciseType, allWords: Word[]): Exercise {
  switch (type) {
    case 'translate_to_english':
      return {
        type,
        word,
        question: `Переведи на английский:\n\n"${word.russian}"`,
        correctAnswer: word.english.toLowerCase(),
      };
    
    case 'translate_to_russian': {
      const options = generateOptions(word.english, allWords.map(w => w.english));
      return {
        type,
        word,
        options,
        question: `Выбери правильный перевод:\n\n"${word.english}"`,
        correctAnswer: word.russian,
      };
    }
    
    case 'listen_and_choose': {
      const options = generateOptions(word.english, allWords.map(w => w.english));
      return {
        type,
        word,
        options,
        question: `🔊 Послушай и выбери слово`,
        correctAnswer: word.english,
      };
    }
    
    case 'type_word':
      return {
        type,
        word,
        question: `Напиши по-английски:\n\n"${word.russian}"\n\nПодсказка: ${word.transcription}`,
        correctAnswer: word.english.toLowerCase(),
      };
    
    case 'match_pairs': {
      const options = generateOptions(word.russian, allWords.map(w => w.russian));
      return {
        type,
        word,
        options,
        question: `Соедини:\n\n"${word.english}" = ?`,
        correctAnswer: word.russian,
      };
    }
  }
}

function generateOptions(correct: string, allOptions: string[]): string[] {
  const others = allOptions.filter(o => o !== correct);
  const shuffled = others.sort(() => Math.random() - 0.5).slice(0, 3);
  const options = [correct, ...shuffled].sort(() => Math.random() - 0.5);
  return options;
}

const exerciseTypes: ExerciseType[] = [
  'translate_to_english',
  'translate_to_russian',
  'listen_and_choose',
  'type_word',
  'match_pairs',
];

export function useLearningSystem() {
  const [progress, setProgress] = useState<UserProgress>(loadProgress);
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
  const [isLessonActive, setIsLessonActive] = useState(false);
  const [lessonComplete, setLessonComplete] = useState(false);
  const [exerciseCount, setExerciseCount] = useState(0);
  const maxExercisesPerSession = 5;

  useEffect(() => {
    saveProgress(progress);
  }, [progress]);

  const getCurrentLesson = useCallback((): Lesson => {
    return lessons[progress.currentLessonIndex % lessons.length];
  }, [progress.currentLessonIndex]);

  const getNextExercise = useCallback(() => {
    const lesson = getCurrentLesson();
    const word = lesson.words[progress.currentWordIndex % lesson.words.length];
    const exerciseType = exerciseTypes[Math.floor(Math.random() * exerciseTypes.length)];
    const exercise = generateExercise(word, exerciseType, lesson.words);
    setCurrentExercise(exercise);
  }, [getCurrentLesson, progress.currentWordIndex]);

  const startLesson = useCallback(() => {
    setIsLessonActive(true);
    setLessonComplete(false);
    setExerciseCount(0);
    getNextExercise();
  }, [getNextExercise]);

  const checkAnswer = useCallback((answer: string): boolean => {
    if (!currentExercise) return false;
    
    const isCorrect = answer.toLowerCase().trim() === currentExercise.correctAnswer.toLowerCase().trim();
    
    setProgress(prev => {
      const newProgress = { ...prev };
      
      if (isCorrect) {
        newProgress.correctAnswers++;
        newProgress.streak++;
        newProgress.totalXP += 10 + (newProgress.streak * 2);
        
        // Level up every 100 XP
        newProgress.level = Math.floor(newProgress.totalXP / 100) + 1;
        
        // Add word to learned
        if (!newProgress.learnedWords.includes(currentExercise.word.id)) {
          newProgress.learnedWords.push(currentExercise.word.id);
        }
        
        // Remove from repeat list
        newProgress.wordsToRepeat = newProgress.wordsToRepeat.filter(id => id !== currentExercise.word.id);
      } else {
        newProgress.wrongAnswers++;
        newProgress.streak = 0;
        
        // Add to repeat list
        if (!newProgress.wordsToRepeat.includes(currentExercise.word.id)) {
          newProgress.wordsToRepeat.push(currentExercise.word.id);
        }
      }
      
      // Move to next word
      const lesson = lessons[newProgress.currentLessonIndex % lessons.length];
      newProgress.currentWordIndex = (newProgress.currentWordIndex + 1) % lesson.words.length;
      
      // Move to next lesson after completing all words
      if (newProgress.currentWordIndex === 0) {
        newProgress.currentLessonIndex = (newProgress.currentLessonIndex + 1) % lessons.length;
      }
      
      return newProgress;
    });

    // Check if session is complete
    const newCount = exerciseCount + 1;
    setExerciseCount(newCount);
    
    if (newCount >= maxExercisesPerSession) {
      setLessonComplete(true);
      setIsLessonActive(false);
    } else {
      // Generate next exercise after a delay
      setTimeout(() => {
        getNextExercise();
      }, 1000);
    }

    return isCorrect;
  }, [currentExercise, exerciseCount, getNextExercise]);

  const resetProgress = useCallback(() => {
    setProgress(defaultProgress);
    setIsLessonActive(false);
    setLessonComplete(false);
    setCurrentExercise(null);
  }, []);

  const skipExercise = useCallback(() => {
    getNextExercise();
  }, [getNextExercise]);

  return {
    progress,
    currentExercise,
    isLessonActive,
    lessonComplete,
    lessons,
    getCurrentLesson,
    startLesson,
    checkAnswer,
    resetProgress,
    skipExercise,
    exerciseCount,
    maxExercisesPerSession,
  };
}
