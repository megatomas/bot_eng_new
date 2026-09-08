import { useState, useEffect, useRef, useCallback } from 'react';
import { useLearningSystem } from './hooks/useLearningSystem';
import { speechService } from './utils/speech';
import { grammarRules } from './data/lessons';

type Screen = 'welcome' | 'menu' | 'lesson' | 'grammar' | 'progress' | 'settings';

interface Message {
  id: string;
  text: string;
  sender: 'bot' | 'user';
  timestamp: Date;
  buttons?: { text: string; action: string }[];
  highlight?: 'correct' | 'wrong' | null;
}

function App() {
  const {
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
  } = useLearningSystem();

  const [screen, setScreen] = useState<Screen>('welcome');
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState('');
  const [showTranslation, setShowTranslation] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showGrammar, setShowGrammar] = useState(false);
  const [selectedGrammar, setSelectedGrammar] = useState(0);
  const [feedbackAnimation, setFeedbackAnimation] = useState<'correct' | 'wrong' | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const goToMenu = useCallback(() => {
    setScreen('menu');
    setMessages([]);
    setTimeout(() => {
      setMessages([{
        id: Date.now().toString(),
        text: '📋 Главное меню\n\nВыбери, что хочешь делать:',
        sender: 'bot',
        timestamp: new Date(),
        buttons: [
          { text: '🚀 Начать урок', action: 'start' },
          { text: '📊 Мой прогресс', action: 'progress' },
          { text: '📖 Грамматика', action: 'grammar' },
          { text: '🔊 Произношение слов', action: 'pronunciation' },
          { text: '🔄 Сбросить прогресс', action: 'reset' },
        ],
      }]);
    }, 100);
  }, []);

  useEffect(() => {
    if (screen === 'welcome') {
      setMessages([{
        id: '1',
        text: '👋 Привет! Я твой персональный репетитор английского языка!\n\n🧠 Я использую метод интервального повторения — это самый быстрый способ запомнить слова.\n\n🔊 Все слова озвучиваются — слушай и повторяй!\n\n🎯 Готов начать?',
        sender: 'bot',
        timestamp: new Date(),
        buttons: [
          { text: '🚀 Начать обучение', action: 'start' },
          { text: '📊 Мой прогресс', action: 'progress' },
          { text: '📖 Грамматика', action: 'grammar' },
        ],
      }]);
    }
  }, [screen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (lessonComplete) {
      const xpEarned = exerciseCount * 12;
      setTimeout(() => {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          text: `🎉 Сессия завершена!\n\n✅ Правильных: ${progress.correctAnswers}\n❌ Ошибок: ${progress.wrongAnswers}\n⭐ Получено XP: +${xpEarned}\n🔥 Серия: ${progress.streak}\n\n💪 Продолжай в том же духе!`,
          sender: 'bot',
          timestamp: new Date(),
          buttons: [
            { text: '🔄 Ещё сессию', action: 'restart' },
            { text: '📋 Меню', action: 'menu' },
          ],
        }]);
      }, 500);
    }
  }, [lessonComplete]);

  useEffect(() => {
    if (isLessonActive && currentExercise) {
      if (currentExercise.type === 'listen_and_choose') {
        setTimeout(() => {
          speakWord(currentExercise.word.english);
        }, 600);
      }
      
      const buttons = currentExercise.options 
        ? currentExercise.options.map(opt => ({ text: opt, action: `answer:${opt}` }))
        : [];
      
      setMessages(prev => [...prev, {
        id: Date.now().toString() + Math.random(),
        text: currentExercise.question,
        sender: 'bot',
        timestamp: new Date(),
        buttons: buttons.length > 0 ? buttons : undefined,
      }]);

      // Focus input for text exercises
      if (!currentExercise.options) {
        setTimeout(() => inputRef.current?.focus(), 300);
      }
    }
  }, [currentExercise, isLessonActive]);

  const speakWord = async (word: string) => {
    setIsSpeaking(true);
    try {
      await speechService.speakWord(word);
    } catch (e) {
      console.error('Speech error:', e);
    }
    setIsSpeaking(false);
  };

  const showFeedback = (correct: boolean) => {
    setFeedbackAnimation(correct ? 'correct' : 'wrong');
    setTimeout(() => setFeedbackAnimation(null), 1500);
  };

  const handleAction = (action: string) => {
    switch (action) {
      case 'start':
        setScreen('lesson');
        setMessages([]);
        setTimeout(() => {
          setMessages([{
            id: Date.now().toString(),
            text: `📚 Начинаем урок!\n\n📖 "${getCurrentLesson().title}"\n${getCurrentLesson().description}\n\n🎯 Каждое задание = 10 XP\n🔥 Серия правильных ответов даёт бонус!\n\nПоехали! 🚀`,
            sender: 'bot',
            timestamp: new Date(),
          }]);
          setTimeout(() => startLesson(), 1500);
        }, 100);
        break;
      
      case 'progress':
        setScreen('progress');
        break;
      
      case 'grammar':
        setScreen('grammar');
        break;
      
      case 'menu':
        goToMenu();
        break;
      
      case 'reset':
        if (confirm('Точно сбросить весь прогресс?')) {
          resetProgress();
          setMessages(prev => [...prev, {
            id: Date.now().toString(),
            text: '🗑️ Прогресс сброшен. Начинаем заново!',
            sender: 'bot',
            timestamp: new Date(),
            buttons: [{ text: '🚀 Начать заново', action: 'start' }],
          }]);
        }
        break;
      
      case 'restart':
        setMessages([]);
        setTimeout(() => {
          setMessages([{
            id: Date.now().toString(),
            text: `🔄 Новая сессия!\n\n📖 ${getCurrentLesson().title}`,
            sender: 'bot',
            timestamp: new Date(),
          }]);
          setTimeout(() => startLesson(), 1000);
        }, 100);
        break;
      
      case 'pronunciation':
        setMessages([]);
        setTimeout(() => {
          const lesson = getCurrentLesson();
          setMessages([{
            id: Date.now().toString(),
            text: '🔊 Режим произношения\n\nНажимай на слово, чтобы услышать произношение. Повторяй за мной!',
            sender: 'bot',
            timestamp: new Date(),
            buttons: lesson.words.map(w => ({
              text: `${w.english} — ${w.russian} 🔊`,
              action: `speak:${w.english}|${w.russian}`
            })),
          }]);
        }, 100);
        break;
      
      default:
        if (action.startsWith('answer:')) {
          const answer = action.replace('answer:', '');
          handleAnswer(answer);
        } else if (action.startsWith('speak:')) {
          const parts = action.replace('speak:', '').split('|');
          speakWord(parts[0]);
        }
    }
  };

  const handleAnswer = (answer: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString() + Math.random(),
      text: answer,
      sender: 'user',
      timestamp: new Date(),
    }]);
    
    const isCorrect = checkAnswer(answer);
    showFeedback(isCorrect);
    
    if (isCorrect) {
      setTimeout(() => {
        setMessages(prev => [...prev, {
          id: Date.now().toString() + Math.random(),
          text: '✅ Правильно! 🎉',
          sender: 'bot',
          timestamp: new Date(),
          highlight: 'correct',
        }]);
        if (currentExercise) {
          speakWord(currentExercise.word.english);
        }
      }, 400);
    } else {
      setTimeout(() => {
        const correct = currentExercise?.correctAnswer || 'N/A';
        setMessages(prev => [...prev, {
          id: Date.now().toString() + Math.random(),
          text: `❌ Неверно.\n\nПравильный ответ: "${correct}"\n\n📝 Запомни!`,
          sender: 'bot',
          timestamp: new Date(),
          highlight: 'wrong',
        }]);
        if (currentExercise) {
          speakWord(currentExercise.word.english);
        }
      }, 400);
    }
    
    setShowTranslation(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (userInput.trim()) {
      handleAnswer(userInput.trim());
      setUserInput('');
    }
  };

  const accuracy = progress.correctAnswers + progress.wrongAnswers > 0 
    ? Math.round(progress.correctAnswers / (progress.correctAnswers + progress.wrongAnswers) * 100) 
    : 0;

  const xpForNextLevel = (progress.level) * 100;
  const xpProgress = ((progress.totalXP % 100) / 100) * 100;

  const renderProgress = () => (
    <div className="p-4 space-y-4">
      {/* Stats Card */}
      <div className="bg-gradient-to-br from-blue-500 via-blue-600 to-purple-700 rounded-2xl p-5 text-white shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">📊 Прогресс</h2>
          <div className="bg-white/20 px-3 py-1 rounded-full text-sm font-bold">
            Lv. {progress.level}
          </div>
        </div>
        
        {/* XP Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-xs mb-1 opacity-80">
            <span>XP до следующего уровня</span>
            <span>{progress.totalXP % 100}/{100}</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-2.5">
            <div className="bg-yellow-400 h-2.5 rounded-full transition-all duration-500" style={{ width: `${xpProgress}%` }} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white/15 backdrop-blur rounded-xl p-3 text-center">
            <div className="text-2xl font-bold">{progress.learnedWords.length}</div>
            <div className="text-xs opacity-80 mt-1">Слов изучено</div>
          </div>
          <div className="bg-white/15 backdrop-blur rounded-xl p-3 text-center">
            <div className="text-2xl font-bold">{progress.streak}🔥</div>
            <div className="text-xs opacity-80 mt-1">Серия</div>
          </div>
          <div className="bg-white/15 backdrop-blur rounded-xl p-3 text-center">
            <div className="text-2xl font-bold">{accuracy}%</div>
            <div className="text-xs opacity-80 mt-1">Точность</div>
          </div>
          <div className="bg-white/15 backdrop-blur rounded-xl p-3 text-center">
            <div className="text-2xl font-bold">{progress.totalXP}</div>
            <div className="text-xs opacity-80 mt-1">Всего XP</div>
          </div>
        </div>
      </div>

      {/* Detailed Stats */}
      <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-bold text-base mb-3 flex items-center gap-2">
          <span>📈</span> Детальная статистика
        </h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-600 text-sm">✅ Правильных ответов</span>
            <span className="font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded">{progress.correctAnswers}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600 text-sm">❌ Ошибок</span>
            <span className="font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded">{progress.wrongAnswers}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600 text-sm">🔄 Нужно повторить</span>
            <span className="font-bold text-orange-500 bg-orange-50 px-2 py-0.5 rounded">{progress.wordsToRepeat.length}</span>
          </div>
        </div>
      </div>

      {/* Lessons */}
      <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-bold text-base mb-3 flex items-center gap-2">
          <span>📚</span> Уроки
        </h3>
        <div className="space-y-2">
          {lessons.map((lesson, idx) => {
            const isCurrent = idx === progress.currentLessonIndex % lessons.length;
            return (
              <div key={lesson.id} className={`flex items-center justify-between p-3 rounded-xl transition ${isCurrent ? 'bg-blue-50 border-2 border-blue-300' : 'bg-gray-50 hover:bg-gray-100'}`}>
                <div>
                  <div className="font-medium text-sm">{lesson.title}</div>
                  <div className="text-xs text-gray-500 mt-0.5">Уровень {lesson.level} • {lesson.words.length} слов</div>
                </div>
                {isCurrent && (
                  <span className="text-[10px] bg-blue-500 text-white px-2 py-0.5 rounded-full font-bold">СЕЙЧАС</span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <button
        onClick={goToMenu}
        className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3.5 rounded-xl font-bold hover:from-blue-600 hover:to-blue-700 transition shadow-md active:scale-[0.98]"
      >
        ← Назад в меню
      </button>
    </div>
  );

  const renderGrammar = () => (
    <div className="p-4 space-y-4">
      <div className="bg-gradient-to-br from-green-500 via-green-600 to-teal-700 rounded-2xl p-5 text-white shadow-lg">
        <h2 className="text-xl font-bold mb-1">📖 Грамматика</h2>
        <p className="text-sm opacity-80">Изучай правила с примерами и произношением</p>
      </div>

      <div className="space-y-3">
        {grammarRules.map((rule, idx) => (
          <div
            key={rule.id}
            onClick={() => { setSelectedGrammar(idx); setShowGrammar(!showGrammar || selectedGrammar !== idx); }}
            className={`bg-white rounded-2xl shadow-sm border transition cursor-pointer hover:shadow-md ${selectedGrammar === idx && showGrammar ? 'border-green-300 ring-2 ring-green-100' : 'border-gray-100'}`}
          >
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-base">{rule.title}</h3>
                  <span className="text-[10px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full mt-1 inline-block">Уровень {rule.level}</span>
                </div>
                <span className={`text-gray-400 transition-transform ${showGrammar && selectedGrammar === idx ? 'rotate-180' : ''}`}>▼</span>
              </div>
            </div>
            
            {showGrammar && selectedGrammar === idx && (
              <div className="px-4 pb-4 border-t border-gray-100 pt-3">
                <p className="text-gray-700 text-sm mb-3 bg-blue-50 p-3 rounded-xl">{rule.explanation}</p>
                <div className="space-y-2">
                  <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">Примеры:</p>
                  {rule.examples.map((ex, i) => (
                    <div key={i} className="bg-gray-50 rounded-xl p-3 group hover:bg-gray-100 transition">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-blue-700 text-sm">{ex.english}</span>
                        <button
                          onClick={(e) => { e.stopPropagation(); speakWord(ex.english); }}
                          className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-sm hover:bg-blue-200 transition active:scale-90"
                        >
                          🔊
                        </button>
                      </div>
                      <span className="text-xs text-gray-500 mt-1 block">{ex.russian}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <button
        onClick={goToMenu}
        className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3.5 rounded-xl font-bold hover:from-green-600 hover:to-green-700 transition shadow-md active:scale-[0.98]"
      >
        ← Назад в меню
      </button>
    </div>
  );

  const renderChat = () => (
    <div className="flex flex-col h-full relative">
      {/* Feedback overlay */}
      {feedbackAnimation && (
        <div className={`absolute inset-0 z-50 pointer-events-none flex items-center justify-center ${feedbackAnimation === 'correct' ? 'bg-green-500/10' : 'bg-red-500/10'}`}>
          <div className={`text-6xl animate-bounce ${feedbackAnimation === 'correct' ? '' : 'animate-pulse'}`}>
            {feedbackAnimation === 'correct' ? '✅' : '❌'}
          </div>
        </div>
      )}

      {/* Session Progress */}
      {isLessonActive && (
        <div className="px-4 py-2.5 bg-white/95 backdrop-blur border-b border-gray-100">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="text-gray-500 font-medium">Прогресс сессии</span>
            <span className="font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">{exerciseCount}/{maxExercisesPerSession}</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-1.5">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-1.5 rounded-full transition-all duration-700 ease-out"
              style={{ width: `${(exerciseCount / maxExercisesPerSession) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5 bg-[#e5ddd5]">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}>
            <div
              className={`max-w-[85%] rounded-2xl px-3.5 py-2 shadow-sm ${
                msg.sender === 'user'
                  ? 'bg-[#dcf8c6] rounded-br-md'
                  : 'bg-white rounded-bl-md'
              } ${msg.highlight === 'correct' ? 'ring-2 ring-green-300 bg-green-50' : ''} ${msg.highlight === 'wrong' ? 'ring-2 ring-red-300 bg-red-50' : ''}`}
            >
              <p className="text-[13px] leading-relaxed whitespace-pre-line">{msg.text}</p>
              <div className="text-[10px] text-gray-400 text-right mt-0.5">
                {msg.timestamp.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                {msg.sender === 'user' && ' ✓✓'}
              </div>
              
              {msg.buttons && msg.buttons.length > 0 && (
                <div className="mt-2 space-y-1.5">
                  {msg.buttons.map((btn, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleAction(btn.action)}
                      className="w-full text-left bg-blue-50 hover:bg-blue-100 active:bg-blue-200 text-blue-700 px-3 py-2 rounded-lg text-[13px] font-medium transition-all active:scale-[0.97]"
                    >
                      {btn.text}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Translation hint */}
      {showTranslation && currentExercise && (
        <div className="px-4 py-2 bg-yellow-50 border-t border-yellow-200 text-center">
          <span className="text-xs text-yellow-800">💡 Ответ: <strong>{currentExercise.correctAnswer}</strong></span>
        </div>
      )}

      {/* Action buttons for exercises */}
      {isLessonActive && currentExercise && (
        <div className="px-3 py-2 bg-white border-t border-gray-100 flex gap-2">
          <button
            onClick={() => currentExercise && speakWord(currentExercise.word.english)}
            className={`flex-1 py-2 rounded-xl text-xs font-medium transition active:scale-95 ${isSpeaking ? 'bg-purple-100 text-purple-700 animate-pulse' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
          >
            {isSpeaking ? '🔊 ...' : '🔊 Слушать'}
          </button>
          <button
            onClick={() => setShowTranslation(!showTranslation)}
            className="flex-1 py-2 rounded-xl text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition active:scale-95"
          >
            {showTranslation ? '🙈 Скрыть' : '💡 Ответ'}
          </button>
          <button
            onClick={skipExercise}
            className="flex-1 py-2 rounded-xl text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition active:scale-95"
          >
            ⏭️ Далее
          </button>
        </div>
      )}

      {/* Text input for typing exercises */}
      {isLessonActive && currentExercise && !currentExercise.options && (
        <form onSubmit={handleSubmit} className="p-2.5 bg-white border-t border-gray-100 flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Введи ответ на английском..."
            className="flex-1 border border-gray-200 rounded-full px-4 py-2 text-sm focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition"
            autoFocus
            autoComplete="off"
            autoCorrect="off"
            spellCheck={false}
          />
          <button
            type="submit"
            disabled={!userInput.trim()}
            className="bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-blue-600 transition active:scale-90 disabled:opacity-50 disabled:active:scale-100 shadow-md"
          >
            ➤
          </button>
        </form>
      )}
    </div>
  );

  return (
    <div className="h-screen w-full flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
      <div className="w-full max-w-md h-full max-h-[100dvh] md:max-h-[750px] md:rounded-3xl md:shadow-2xl bg-white flex flex-col overflow-hidden relative border border-gray-200 md:border-0">
        {/* Header */}
        <div className="bg-gradient-to-r from-[#2AABEE] to-[#229ED9] text-white px-4 py-3 flex items-center gap-3 shadow-md z-10 shrink-0">
          <button
            onClick={goToMenu}
            className="text-white/80 hover:text-white transition text-lg"
          >
            ←
          </button>
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center text-xl backdrop-blur-sm">
            🤖
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="font-bold text-sm truncate">English Learning Bot</h1>
            <p className="text-[11px] opacity-80 truncate">
              {isLessonActive ? '🟢 Урок идёт...' : screen === 'progress' ? '📊 Статистика' : screen === 'grammar' ? '📖 Грамматика' : '⚡ online'}
            </p>
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            <div className="text-[10px] bg-white/20 backdrop-blur px-2 py-0.5 rounded-full font-bold">
              Lv.{progress.level}
            </div>
            <div className="text-[10px] bg-yellow-400/30 backdrop-blur px-2 py-0.5 rounded-full font-bold">
              ⭐{progress.totalXP}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          {screen === 'progress' && renderProgress()}
          {screen === 'grammar' && renderGrammar()}
          {(screen === 'welcome' || screen === 'menu' || screen === 'lesson') && renderChat()}
        </div>
      </div>
    </div>
  );
}

export default App;
