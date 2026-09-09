import { useState } from 'react'

function App() {
  const [copied, setCopied] = useState(false)

  const setupCode = `#!/usr/bin/env python3
"""
ENGLISH LEARNING BOT — АВТОМАТИЧЕСКАЯ УСТАНОВКА

КАК ИСПОЛЬЗОВАТЬ:
1. Скопируй ВЕСЬ этот код
2. В PyCharm создай файл setup_all.py в корне проекта
3. Вставь код и сохрани
4. Запусти: python setup_all.py
5. Скрипт создаст все файлы автоматически!
"""

import os
from pathlib import Path


def create_file(filepath: str, content: str):
    """Создаёт файл с содержимым."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if path.exists() and path.stat().st_size > 0:
        print(f"⏭️  Пропущен: {filepath}")
        return
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Создан: {filepath}")


def setup():
    """Создаёт все файлы проекта."""
    
    print("=" * 60)
    print("🚀 English Learning Bot — Установка")
    print("=" * 60)
    print()
    
    # ... (весь код из файла setup_all.py)
    # Файл слишком большой для отображения здесь
    # Открой файл setup_all.py в этой среде и скопируй его
    
    print()
    print("=" * 60)
    print("✅ ВСЕ ФАЙЛЫ СОЗДАНЫ!")
    print("=" * 60)
    print()
    print("📋 Следующие шаги:")
    print()
    print("1. Установи зависимости:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Отредактируй .env:")
    print("   - Добавь BOT_TOKEN (от @BotFather)")
    print("   - Добавь GROQ_API_KEY (с https://console.groq.com/)")
    print()
    print("3. Запусти PostgreSQL:")
    print("   docker-compose up -d db")
    print()
    print("4. Импортируй словарь:")
    print("   python -m scripts.import_words data/words_sample.json")
    print()
    print("5. Запусти бота:")
    print("   python -m app.main")
    print()
    print("🎉 Готово!")


if __name__ == "__main__":
    setup()
`

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          🇬🇧 English Learning Bot
        </h1>
        <p className="text-xl text-slate-300 mb-8">Установка на компьютер через PyCharm</p>

        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-8">
          <p className="text-yellow-200">
            ⚠️ <strong>Важно:</strong> Файл <code className="bg-slate-800 px-2 py-1 rounded">setup_all.py</code> создан в этой среде. 
            Открой его в файловом дереве слева, скопируй ВЕСЬ код и создай файл на компьютере.
          </p>
        </div>

        <div className="space-y-6">
          <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold mb-4 text-blue-400">📋 Пошаговая инструкция</h2>
            
            <div className="space-y-4">
              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 1: Скопируй setup_all.py</h3>
                <p className="text-slate-300 text-sm">
                  В файловом дереве слева найди файл <code className="bg-slate-800 px-2 py-1 rounded">setup_all.py</code> → 
                  Открой его → Выдели всё (<span className="text-blue-400">Ctrl+A</span>) → 
                  Скопируй (<span className="text-blue-400">Ctrl+C</span>)
                </p>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 2: Создай файл в PyCharm</h3>
                <p className="text-slate-300 text-sm">
                  В PyCharm: <span className="text-blue-400">Файл → Новый файл</span> → 
                  Имя: <code className="bg-slate-800 px-2 py-1 rounded">setup_all.py</code> → 
                  Вставь код (<span className="text-blue-400">Ctrl+V</span>) → 
                  Сохрани (<span className="text-blue-400">Ctrl+S</span>)
                </p>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 3: Запусти скрипт</h3>
                <p className="text-slate-300 text-sm mb-2">Открой терминал в PyCharm (<span className="text-blue-400">Alt+F12</span>) и выполни:</p>
                <code className="block bg-slate-800 p-2 rounded text-green-400">python setup_all.py</code>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 4: Настрой .env</h3>
                <p className="text-slate-300 text-sm mb-2">Открой файл <code className="bg-slate-800 px-2 py-1 rounded">.env</code> и заполни:</p>
                <pre className="bg-slate-800 p-3 rounded text-sm overflow-x-auto">
{`BOT_TOKEN=твой_токен_от_BotFather
GROQ_API_KEY=gsk_твой_groq_ключ`}
                </pre>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 5: Установи зависимости</h3>
                <code className="block bg-slate-800 p-2 rounded text-green-400">pip install -r requirements.txt</code>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 6: Запусти PostgreSQL</h3>
                <code className="block bg-slate-800 p-2 rounded text-green-400">docker-compose up -d db</code>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 7: Импортируй словарь</h3>
                <code className="block bg-slate-800 p-2 rounded text-green-400">python -m scripts.import_words data/words_sample.json</code>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-green-400 mb-2">Шаг 8: Запусти бота</h3>
                <code className="block bg-slate-800 p-2 rounded text-green-400">python -m app.main</code>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold mb-4 text-purple-400">🔑 Где получить ключи</h2>
            
            <div className="space-y-4">
              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-blue-300 mb-2">Groq API (AI-собеседник) — БЕСПЛАТНО</h3>
                <ol className="list-decimal list-inside space-y-1 text-slate-300 text-sm">
                  <li>Зайди на <a href="https://console.groq.com/" className="text-blue-400 hover:underline" target="_blank">https://console.groq.com/</a></li>
                  <li>Войди через Google</li>
                  <li>"API Keys" → "Create API Key"</li>
                  <li>Скопируй ключ (начинается с <code className="bg-slate-800 px-1 rounded">gsk_...</code>)</li>
                </ol>
                <p className="text-green-400 text-sm mt-2">✅ Бесплатно: 14400 запросов/день</p>
              </div>

              <div className="bg-slate-900/50 rounded p-4">
                <h3 className="font-bold text-blue-300 mb-2">Telegram Bot Token</h3>
                <ol className="list-decimal list-inside space-y-1 text-slate-300 text-sm">
                  <li>Открой Telegram → найди @BotFather</li>
                  <li>Отправь <code className="bg-slate-800 px-1 rounded">/newbot</code></li>
                  <li>Придумай имя и username</li>
                  <li>Скопируй токен</li>
                </ol>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
            <h2 className="text-2xl font-bold mb-4 text-orange-400">📁 Созданные файлы</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
              {[
                'app/ai/providers.py',
                'app/speech/providers.py',
                'app/telegram/handlers/review.py',
                'app/telegram/handlers/dialogue.py',
                'app/telegram/handlers/progress.py',
                'scripts/import_words.py',
                'app/config.py',
                'app/main.py',
                'app/database/*',
                'app/repositories/*',
                'app/services/*',
                'requirements.txt',
                '.env',
                'docker-compose.yml',
              ].map(file => (
                <div key={file} className="bg-slate-900/50 px-3 py-2 rounded font-mono text-slate-300">
                  📄 {file}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-green-400">✅ Готово!</h2>
            <p className="text-slate-300">
              После выполнения всех шагов бот будет полностью работать с бесплатными решениями:
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-300 mt-3">
              <li>🤖 AI: Groq (Llama 3.3) — бесплатно</li>
              <li>🎤 TTS: edge-tts — бесплатно</li>
              <li>🎧 STT: Whisper — бесплатно</li>
              <li>💰 Итого: $0/месяц</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 text-center text-slate-500 text-sm">
          <p>Приятного изучения английского! 🇬🇧✨</p>
        </div>
      </div>
    </div>
  )
}

export default App
