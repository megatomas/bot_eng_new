import { useState } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'setup' | 'commands' | 'features'>('overview')
  const [copiedCmd, setCopiedCmd] = useState('')

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedCmd(id)
    setTimeout(() => setCopiedCmd(''), 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-black/20">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-xl">
              🤖
            </div>
            <div>
              <h1 className="font-bold text-lg">English Learning Bot</h1>
              <p className="text-xs text-blue-300">Telegram • Python • AI</p>
            </div>
          </div>
          <a
            href="https://core.telegram.org/bots"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium transition-colors"
          >
            Telegram Bot API →
          </a>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-4 py-16 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 text-sm mb-6">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
          Python 3.10+ • Полностью автономный
        </div>
        <h2 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-white via-blue-200 to-cyan-200 bg-clip-text text-transparent">
          Telegram-бот для изучения<br />английского языка
        </h2>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
          60+ слов, голосовое озвучивание, 5 типов упражнений, адаптивное обучение
          с интервальным повторением и системой прогресса.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10">
            <span>🔊</span><span className="text-sm">Голосовое TTS</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10">
            <span>🧠</span><span className="text-sm">Адаптивное обучение</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10">
            <span>📊</span><span className="text-sm">Система прогресса</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10">
            <span>🔄</span><span className="text-sm">Интервальный повтор</span>
          </div>
        </div>
      </section>

      {/* Bot Preview */}
      <section className="max-w-6xl mx-auto px-4 pb-16">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Phone mockup */}
          <div className="relative">
            <div className="bg-[#17212b] rounded-3xl overflow-hidden shadow-2xl shadow-blue-500/10 border border-white/10 max-w-sm mx-auto">
              {/* Telegram header */}
              <div className="bg-[#242f3d] px-4 py-3 flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-sm">
                  🤖
                </div>
                <div>
                  <div className="font-medium text-sm">English Learning Bot</div>
                  <div className="text-xs text-blue-400">online</div>
                </div>
              </div>
              {/* Messages */}
              <div className="p-4 space-y-3 bg-[#0e1621] min-h-[400px]">
                <div className="bg-[#2b5278] rounded-xl rounded-tl-sm p-3 max-w-[85%]">
                  <p className="text-sm">🎓 <b>Привет!</b> Я твой репетитор английского!</p>
                  <p className="text-xs text-blue-300 mt-1">12:00</p>
                </div>
                <div className="bg-[#2b5278] rounded-xl rounded-tl-sm p-3 max-w-[85%]">
                  <p className="text-sm">📖 <b>Новое слово!</b></p>
                  <p className="text-sm mt-1">🇬🇧 <b>Hello</b> /həˈloʊ/</p>
                  <p className="text-sm">🇷🇺 Привет</p>
                </div>
                <div className="flex justify-center">
                  <div className="bg-[#2b5278]/50 rounded-full px-4 py-2 flex items-center gap-2">
                    <span className="text-lg">🔊</span>
                    <span className="text-xs text-blue-300">0:02</span>
                  </div>
                </div>
                <div className="bg-[#2b5278] rounded-xl rounded-tl-sm p-3 max-w-[85%]">
                  <p className="text-sm">🇬🇧 ➜ 🇷🇺 Выбери перевод:</p>
                  <p className="text-sm font-bold mt-1">«Hello»</p>
                </div>
                <div className="space-y-1.5 pl-2">
                  {['Привет ✅', 'До свидания', 'Спасибо', 'Пожалуйста'].map((opt, i) => (
                    <div key={i} className={`px-3 py-2 rounded-lg text-sm ${i === 0 ? 'bg-green-500/20 border border-green-500/30 text-green-300' : 'bg-white/5 border border-white/10'}`}>
                      {opt}
                    </div>
                  ))}
                </div>
                <div className="bg-[#2b5278] rounded-xl rounded-tl-sm p-3 max-w-[85%]">
                  <p className="text-sm">✅ <b>Правильно!</b> 🎉</p>
                  <p className="text-xs text-yellow-300 mt-1">+12 XP 🔥 Серия: 3</p>
                </div>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold mb-6">Возможности бота</h3>
            {[
              { icon: '🔊', title: 'Голосовое озвучивание', desc: 'Каждое слово и пример произносится через Google TTS. Можно замедлить для лучшего восприятия.' },
              { icon: '🎯', title: '5 типов упражнений', desc: 'Перевод, выбор из вариантов, аудирование, набор текста, соединение пар — для полного усвоения.' },
              { icon: '🧠', title: 'Адаптивное обучение', desc: 'Бот отслеживает ошибки и автоматически добавляет сложные слова в очередь повторения.' },
              { icon: '📈', title: 'Система мотивации', desc: 'XP, уровни, серии правильных ответов — всё как в Duolingo, но прямо в Telegram.' },
              { icon: '📝', title: 'Грамматика', desc: '6 грамматических правил с примерами и аудио-произношением каждого примера.' },
              { icon: '💾', title: 'Сохранение прогресса', desc: 'SQLite база данных хранит прогресс каждого пользователя. Ничего не потеряется.' },
            ].map((feature, i) => (
              <div key={i} className="flex gap-4 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
                <div className="text-2xl flex-shrink-0">{feature.icon}</div>
                <div>
                  <h4 className="font-semibold">{feature.title}</h4>
                  <p className="text-sm text-slate-400 mt-1">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tabs section */}
      <section className="max-w-6xl mx-auto px-4 pb-16">
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'overview' as const, label: '📋 Обзор', },
            { id: 'setup' as const, label: '⚙️ Установка' },
            { id: 'commands' as const, label: '⌨️ Команды' },
            { id: 'features' as const, label: '🎮 Фичи' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-white/5 text-slate-400 hover:bg-white/10'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h3 className="text-2xl font-bold">📋 Структура проекта</h3>
              <div className="bg-black/30 rounded-xl p-4 font-mono text-sm overflow-x-auto">
                <pre>{`english-telegram-bot/
├── bot.py              # Главный файл бота (обработчики, логика)
├── lessons.py          # Данные: 60 слов, 6 уроков, грамматика
├── speech.py           # Google TTS — генерация аудио
├── progress.py         # SQLite — сохранение прогресса
├── requirements.txt    # Зависимости Python
└── README.md           # Документация`}</pre>
              </div>
              
              <h4 className="text-lg font-bold mt-8">📦 Зависимости</h4>
              <div className="grid md:grid-cols-3 gap-4">
                {[
                  { name: 'python-telegram-bot', desc: 'Telegram Bot API', version: '21.6' },
                  { name: 'gTTS', desc: 'Google Text-to-Speech', version: '2.5.4' },
                  { name: 'aiosqlite', desc: 'Async SQLite', version: '0.20.0' },
                ].map((dep, i) => (
                  <div key={i} className="p-4 rounded-xl bg-black/20 border border-white/10">
                    <div className="font-mono text-blue-300 font-bold">{dep.name}</div>
                    <div className="text-xs text-slate-500 mt-1">v{dep.version}</div>
                    <div className="text-sm text-slate-400 mt-2">{dep.desc}</div>
                  </div>
                ))}
              </div>

              <h4 className="text-lg font-bold mt-8">📊 Статистика контента</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { num: '60+', label: 'Слов', icon: '📝' },
                  { num: '6', label: 'Уроков', icon: '📖' },
                  { num: '5', label: 'Типов упражнений', icon: '🎯' },
                  { num: '6', label: 'Правил грамматики', icon: '📝' },
                ].map((stat, i) => (
                  <div key={i} className="text-center p-4 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20">
                    <div className="text-2xl mb-1">{stat.icon}</div>
                    <div className="text-2xl font-bold text-blue-300">{stat.num}</div>
                    <div className="text-xs text-slate-400">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'setup' && (
            <div className="space-y-6">
              <h3 className="text-2xl font-bold">⚙️ Установка и запуск</h3>
              
              <div className="space-y-4">
                {[
                  {
                    step: 1,
                    title: 'Получите токен бота',
                    desc: 'Откройте @BotFather в Telegram, отправьте /newbot и следуйте инструкциям.',
                    code: null,
                  },
                  {
                    step: 2,
                    title: 'Установите зависимости',
                    desc: 'Убедитесь, что у вас Python 3.10+',
                    code: 'pip install -r requirements.txt',
                  },
                  {
                    step: 3,
                    title: 'Установите токен',
                    desc: 'Замените YOUR_TOKEN на токен от @BotFather',
                    code: 'export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"',
                  },
                  {
                    step: 4,
                    title: 'Запустите бота',
                    desc: 'Бот готов к работе!',
                    code: 'python bot.py',
                  },
                ].map((step, i) => (
                  <div key={i} className="flex gap-4">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-bold text-sm">
                      {step.step}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold">{step.title}</h4>
                      <p className="text-sm text-slate-400 mt-1">{step.desc}</p>
                      {step.code && (
                        <div className="mt-2 relative group">
                          <div className="bg-black/40 rounded-lg p-3 font-mono text-sm text-green-300 overflow-x-auto">
                            <code>$ {step.code}</code>
                          </div>
                          <button
                            onClick={() => copyToClipboard(step.code!, `step-${i}`)}
                            className="absolute top-2 right-2 px-2 py-1 rounded text-xs bg-white/10 hover:bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity"
                          >
                            {copiedCmd === `step-${i}` ? '✓' : '📋'}
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 p-4 rounded-xl bg-yellow-500/10 border border-yellow-500/20">
                <h4 className="font-semibold text-yellow-300">💡 Совет</h4>
                <p className="text-sm text-slate-400 mt-1">
                  Для постоянной работы используйте <code className="bg-black/30 px-1 rounded">systemd</code> или <code className="bg-black/30 px-1 rounded">pm2</code> для автозапуска.
                  Бот также создаёт папку <code className="bg-black/30 px-1 rounded">bot_data/</code> для SQLite базы и <code className="bg-black/30 px-1 rounded">audio_cache/</code> для временных аудиофайлов.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'commands' && (
            <div className="space-y-6">
              <h3 className="text-2xl font-bold">⌨️ Команды бота</h3>
              <div className="space-y-3">
                {[
                  { cmd: '/start', desc: 'Приветствие и главное меню с навигацией', icon: '🏠' },
                  { cmd: '/learn', desc: 'Начать новый урок с голосовым озвучиванием слов', icon: '📖' },
                  { cmd: '/practice', desc: 'Практика — 5 упражнений с разными типами', icon: '🏋️' },
                  { cmd: '/vocab', desc: 'Просмотр изученных слов с транскрипцией', icon: '📚' },
                  { cmd: '/grammar', desc: 'Грамматические правила с примерами и аудио', icon: '📝' },
                  { cmd: '/stats', desc: 'Статистика: уровень, XP, точность, серии', icon: '📊' },
                  { cmd: '/reset', desc: 'Сбросить весь прогресс (с подтверждением)', icon: '🔄' },
                ].map((command, i) => (
                  <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-black/20 border border-white/10 hover:bg-black/30 transition-colors">
                    <span className="text-2xl">{command.icon}</span>
                    <div className="flex-1">
                      <code className="text-blue-300 font-mono font-bold">{command.cmd}</code>
                      <p className="text-sm text-slate-400 mt-1">{command.desc}</p>
                    </div>
                    <button
                      onClick={() => copyToClipboard(command.cmd, command.cmd)}
                      className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs transition-colors"
                    >
                      {copiedCmd === command.cmd ? '✓ Скопировано' : '📋 Копировать'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'features' && (
            <div className="space-y-6">
              <h3 className="text-2xl font-bold">🎮 Система обучения</h3>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-bold text-lg mb-3">🎯 5 типов упражнений</h4>
                  <div className="space-y-2">
                    {[
                      { type: 'translate_to_english', name: 'Перевод на английский', desc: 'Пишешь английский по русскому слову' },
                      { type: 'translate_to_russian', name: 'Выбор перевода', desc: 'Выбираешь из 4 вариантов' },
                      { type: 'listen_and_choose', name: 'Аудирование', desc: 'Слушаешь аудио и выбираешь слово' },
                      { type: 'type_word', name: 'Набор текста', desc: 'Пишешь слово с подсказкой' },
                      { type: 'match_pairs', name: 'Соединение пар', desc: 'Соединяешь слово с переводом' },
                    ].map((ex, i) => (
                      <div key={i} className="p-3 rounded-lg bg-black/20 border border-white/10">
                        <div className="font-medium text-sm">{ex.name}</div>
                        <div className="text-xs text-slate-500">{ex.desc}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-bold text-lg mb-3">📈 Система XP</h4>
                  <div className="space-y-3">
                    <div className="p-4 rounded-xl bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/20">
                      <div className="text-sm text-slate-400">За правильный ответ</div>
                      <div className="text-2xl font-bold text-blue-300">+10 XP</div>
                    </div>
                    <div className="p-4 rounded-xl bg-gradient-to-r from-orange-500/10 to-yellow-500/10 border border-orange-500/20">
                      <div className="text-sm text-slate-400">Бонус за серию</div>
                      <div className="text-2xl font-bold text-orange-300">+2 XP × streak</div>
                      <div className="text-xs text-slate-500 mt-1">(макс. +20)</div>
                    </div>
                    <div className="p-4 rounded-xl bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20">
                      <div className="text-sm text-slate-400">Новый уровень</div>
                      <div className="text-2xl font-bold text-purple-300">каждые 100 XP</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-bold text-lg mb-3">🔄 Интервальное повторение</h4>
                <div className="p-4 rounded-xl bg-black/20 border border-white/10">
                  <p className="text-sm text-slate-400">
                    Когда пользователь отвечает неправильно, слово автоматически добавляется в список на повторение.
                    Бот предложит повторить эти слова при следующем запуске <code className="bg-black/30 px-1 rounded">/practice</code>.
                    Это обеспечивает эффективное запоминание по принципу интервального повторения.
                  </p>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-bold text-lg mb-3">🔊 Голосовое озвучивание</h4>
                <div className="p-4 rounded-xl bg-black/20 border border-white/10">
                  <p className="text-sm text-slate-400">
                    Используется <b>Google Text-to-Speech (gTTS)</b>. Каждое слово автоматически озвучивается при показе.
                    Также доступны кнопки:
                  </p>
                  <div className="flex gap-3 mt-3">
                    <span className="px-3 py-1.5 rounded-lg bg-blue-500/20 text-blue-300 text-sm">🔊 Нормальная скорость</span>
                    <span className="px-3 py-1.5 rounded-lg bg-green-500/20 text-green-300 text-sm">🐢 Замедленная</span>
                    <span className="px-3 py-1.5 rounded-lg bg-purple-500/20 text-purple-300 text-sm">💬 Пример</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Lessons preview */}
      <section className="max-w-6xl mx-auto px-4 pb-16">
        <h3 className="text-2xl font-bold mb-6">📚 Уроки</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { title: '🔤 Базовые слова', desc: 'Hello, Goodbye, Thank you...', level: 1, words: 10 },
            { title: '👤 О себе', desc: 'I am, My name is, I like...', level: 1, words: 10 },
            { title: '🏠 Повседневная жизнь', desc: 'Morning, Today, Always...', level: 2, words: 10 },
            { title: '✈️ Путешествия', desc: 'Airport, Hotel, Ticket...', level: 2, words: 10 },
            { title: '💬 Полезные фразы', desc: 'How are you?, Excuse me...', level: 2, words: 10 },
            { title: '🧠 Продвинутый', desc: 'Achievement, Opportunity...', level: 3, words: 10 },
          ].map((lesson, i) => (
            <div key={i} className="p-5 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-blue-500/30 transition-all group">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-bold">{lesson.title}</h4>
                <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300">
                  {'⭐'.repeat(lesson.level)}
                </span>
              </div>
              <p className="text-sm text-slate-400 mb-3">{lesson.desc}</p>
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>📝 {lesson.words} слов</span>
                <span className="group-hover:text-blue-400 transition-colors">Уровень {lesson.level} →</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 text-center text-sm text-slate-500">
        <p>English Learning Telegram Bot • Python 3.10+ • python-telegram-bot + gTTS</p>
        <p className="mt-2">Создано для быстрого и эффективного изучения английского 🇬🇧</p>
      </footer>
    </div>
  )
}

export default App
