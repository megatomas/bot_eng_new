"""
Данные уроков для бота обучения английскому языку.
Содержит слова, фразы и грамматические правила.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Word:
    id: str
    english: str
    russian: str
    transcription: str
    example: str
    example_translation: str
    category: str
    level: int


@dataclass
class Lesson:
    id: str
    title: str
    description: str
    level: int
    words: List[Word] = field(default_factory=list)
    lesson_type: str = "vocabulary"  # vocabulary, phrases, grammar


@dataclass
class GrammarRule:
    id: str
    title: str
    level: int
    explanation: str
    examples: List[dict]  # [{"english": "...", "russian": "..."}]


# ============================================================
# УРОК 1: Базовые слова
# ============================================================
LESSON_1 = Lesson(
    id="basics-1",
    title="🔤 Базовые слова",
    description="Самые важные слова для начала",
    level=1,
    words=[
        Word("w1", "Hello", "Привет", "/həˈloʊ/", "Hello, how are you?", "Привет, как дела?", "greetings", 1),
        Word("w2", "Goodbye", "До свидания", "/ɡʊdˈbaɪ/", "Goodbye, see you tomorrow!", "До свидания, увидимся завтра!", "greetings", 1),
        Word("w3", "Thank you", "Спасибо", "/θæŋk juː/", "Thank you very much!", "Большое спасибо!", "greetings", 1),
        Word("w4", "Please", "Пожалуйста", "/pliːz/", "Please help me.", "Пожалуйста, помоги мне.", "greetings", 1),
        Word("w5", "Yes", "Да", "/jes/", "Yes, I agree.", "Да, я согласен.", "basics", 1),
        Word("w6", "No", "Нет", "/noʊ/", "No, thank you.", "Нет, спасибо.", "basics", 1),
        Word("w7", "Water", "Вода", "/ˈwɔːtər/", "Can I have some water?", "Можно мне воды?", "food", 1),
        Word("w8", "Food", "Еда", "/fuːd/", "The food is delicious.", "Еда вкусная.", "food", 1),
        Word("w9", "Home", "Дом", "/hoʊm/", "I want to go home.", "Я хочу пойти домой.", "places", 1),
        Word("w10", "Work", "Работа", "/wɜːrk/", "I go to work every day.", "Я хожу на работу каждый день.", "places", 1),
    ]
)

# ============================================================
# УРОК 2: О себе
# ============================================================
LESSON_2 = Lesson(
    id="basics-2",
    title="👤 О себе",
    description="Расскажи о себе",
    level=1,
    words=[
        Word("w11", "I am", "Я есть", "/aɪ æm/", "I am a student.", "Я студент.", "pronouns", 1),
        Word("w12", "My name is", "Меня зовут", "/maɪ neɪm ɪz/", "My name is John.", "Меня зовут Джон.", "pronouns", 1),
        Word("w13", "I like", "Мне нравится", "/aɪ laɪk/", "I like music.", "Мне нравится музыка.", "verbs", 1),
        Word("w14", "I want", "Я хочу", "/aɪ wɑːnt/", "I want to learn English.", "Я хочу учить английский.", "verbs", 1),
        Word("w15", "I have", "У меня есть", "/aɪ hæv/", "I have a cat.", "У меня есть кошка.", "verbs", 1),
        Word("w16", "I can", "Я могу", "/aɪ kæn/", "I can speak English.", "Я могу говорить по-английски.", "verbs", 1),
        Word("w17", "Friend", "Друг", "/frend/", "He is my best friend.", "Он мой лучший друг.", "people", 1),
        Word("w18", "Family", "Семья", "/ˈfæmɪli/", "I love my family.", "Я люблю свою семью.", "people", 1),
        Word("w19", "Happy", "Счастливый", "/ˈhæpi/", "I am very happy today.", "Я очень счастлив сегодня.", "emotions", 1),
        Word("w20", "Good", "Хороший", "/ɡʊd/", "This is a good idea.", "Это хорошая идея.", "adjectives", 1),
    ]
)

# ============================================================
# УРОК 3: Повседневная жизнь
# ============================================================
LESSON_3 = Lesson(
    id="daily-1",
    title="🏠 Повседневная жизнь",
    description="Слова для ежедневного общения",
    level=2,
    words=[
        Word("w21", "Morning", "Утро", "/ˈmɔːrnɪŋ/", "Good morning!", "Доброе утро!", "time", 2),
        Word("w22", "Evening", "Вечер", "/ˈiːvnɪŋ/", "Good evening, everyone.", "Добрый вечер, все.", "time", 2),
        Word("w23", "Today", "Сегодня", "/təˈdeɪ/", "Today is a beautiful day.", "Сегодня прекрасный день.", "time", 2),
        Word("w24", "Tomorrow", "Завтра", "/təˈmɑːroʊ/", "See you tomorrow.", "Увидимся завтра.", "time", 2),
        Word("w25", "Yesterday", "Вчера", "/ˈjestərdeɪ/", "I was busy yesterday.", "Я был занят вчера.", "time", 2),
        Word("w26", "Always", "Всегда", "/ˈɔːlweɪz/", "I always drink coffee.", "Я всегда пью кофе.", "frequency", 2),
        Word("w27", "Never", "Никогда", "/ˈnevər/", "I never give up.", "Я никогда не сдаюсь.", "frequency", 2),
        Word("w28", "Sometimes", "Иногда", "/ˈsʌmtaɪmz/", "Sometimes I read books.", "Иногда я читаю книги.", "frequency", 2),
        Word("w29", "Quickly", "Быстро", "/ˈkwɪkli/", "He runs quickly.", "Он бегает быстро.", "adverbs", 2),
        Word("w30", "Slowly", "Медленно", "/ˈsloʊli/", "Please speak slowly.", "Пожалуйста, говорите медленно.", "adverbs", 2),
    ]
)

# ============================================================
# УРОК 4: Путешествия
# ============================================================
LESSON_4 = Lesson(
    id="travel-1",
    title="✈️ Путешествия",
    description="Слова для путешествий",
    level=2,
    words=[
        Word("w31", "Airport", "Аэропорт", "/ˈerpɔːrt/", "The airport is far from here.", "Аэропорт далеко отсюда.", "travel", 2),
        Word("w32", "Hotel", "Отель", "/hoʊˈtel/", "The hotel is very nice.", "Отель очень хороший.", "travel", 2),
        Word("w33", "Ticket", "Билет", "/ˈtɪkɪt/", "I need a ticket.", "Мне нужен билет.", "travel", 2),
        Word("w34", "Passport", "Паспорт", "/ˈpæspɔːrt/", "Where is my passport?", "Где мой паспорт?", "travel", 2),
        Word("w35", "Map", "Карта", "/mæp/", "Do you have a map?", "У вас есть карта?", "travel", 2),
        Word("w36", "Train", "Поезд", "/treɪn/", "The train arrives at 5.", "Поезд прибывает в 5.", "transport", 2),
        Word("w37", "Bus", "Автобус", "/bʌs/", "Take the bus to the center.", "Сядь на автобус до центра.", "transport", 2),
        Word("w38", "Taxi", "Такси", "/ˈtæksi/", "Call me a taxi, please.", "Вызовите мне такси, пожалуйста.", "transport", 2),
        Word("w39", "Restaurant", "Ресторан", "/ˈrestərɑːnt/", "Let's go to a restaurant.", "Давай пойдём в ресторан.", "places", 2),
        Word("w40", "Museum", "Музей", "/mjuːˈziːəm/", "The museum is closed today.", "Музей закрыт сегодня.", "places", 2),
    ]
)

# ============================================================
# УРОК 5: Полезные фразы
# ============================================================
LESSON_5 = Lesson(
    id="phrases-1",
    title="💬 Полезные фразы",
    description="Фразы для общения",
    level=2,
    lesson_type="phrases",
    words=[
        Word("w41", "How are you?", "Как дела?", "/haʊ ɑːr juː/", "Hi! How are you doing?", "Привет! Как у тебя дела?", "greetings", 2),
        Word("w42", "Nice to meet you", "Приятно познакомиться", "/naɪs tuː miːt juː/", "Nice to meet you, I'm Anna.", "Приятно познакомиться, я Анна.", "greetings", 2),
        Word("w43", "I don't understand", "Я не понимаю", "/aɪ doʊnt ˌʌndərˈstænd/", "Sorry, I don't understand.", "Извините, я не понимаю.", "communication", 2),
        Word("w44", "Can you help me?", "Можете помочь?", "/kæn juː help miː/", "Can you help me, please?", "Можете мне помочь, пожалуйста?", "communication", 2),
        Word("w45", "Where is?", "Где?", "/wer ɪz/", "Where is the bathroom?", "Где туалет?", "questions", 2),
        Word("w46", "How much?", "Сколько стоит?", "/haʊ mʌtʃ/", "How much does it cost?", "Сколько это стоит?", "shopping", 2),
        Word("w47", "I'm sorry", "Извините", "/aɪm ˈsɑːri/", "I'm sorry for being late.", "Извините за опоздание.", "communication", 2),
        Word("w48", "Excuse me", "Простите", "/ɪkˈskjuːz miː/", "Excuse me, where is the station?", "Простите, где вокзал?", "communication", 2),
        Word("w49", "Of course", "Конечно", "/əv kɔːrs/", "Of course, I can help!", "Конечно, я могу помочь!", "communication", 2),
        Word("w50", "No problem", "Нет проблем", "/noʊ ˈprɑːbləm/", "No problem, take your time.", "Нет проблем, не торопись.", "communication", 2),
    ]
)

# ============================================================
# УРОК 6: Продвинутый уровень
# ============================================================
LESSON_6 = Lesson(
    id="advanced-1",
    title="🧠 Продвинутый уровень",
    description="Сложные слова и выражения",
    level=3,
    words=[
        Word("w51", "Achievement", "Достижение", "/əˈtʃiːvmənt/", "It was a great achievement.", "Это было великое достижение.", "abstract", 3),
        Word("w52", "Opportunity", "Возможность", "/ˌɑːpərˈtuːnɪti/", "This is a great opportunity.", "Это отличная возможность.", "abstract", 3),
        Word("w53", "Experience", "Опыт", "/ɪkˈspɪriəns/", "I have a lot of experience.", "У меня много опыта.", "abstract", 3),
        Word("w54", "Knowledge", "Знание", "/ˈnɑːlɪdʒ/", "Knowledge is power.", "Знание — сила.", "abstract", 3),
        Word("w55", "Environment", "Окружение/среда", "/ɪnˈvaɪrənmənt/", "We must protect the environment.", "Мы должны защищать окружающую среду.", "nature", 3),
        Word("w56", "Development", "Развитие", "/dɪˈveləpmənt/", "The development was successful.", "Развитие было успешным.", "abstract", 3),
        Word("w57", "Relationship", "Отношения", "/rɪˈleɪʃnʃɪp/", "They have a good relationship.", "У них хорошие отношения.", "people", 3),
        Word("w58", "Responsibility", "Ответственность", "/rɪˌspɑːnsəˈbɪlɪti/", "It's your responsibility.", "Это твоя ответственность.", "abstract", 3),
        Word("w59", "Communication", "Общение", "/kəˌmjuːnɪˈkeɪʃn/", "Communication is very important.", "Общение очень важно.", "abstract", 3),
        Word("w60", "Independent", "Независимый", "/ˌɪndɪˈpendənt/", "She is very independent.", "Она очень независимая.", "adjectives", 3),
    ]
)

# Все уроки
ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5, LESSON_6]

# Все слова (плоский список)
ALL_WORDS = [word for lesson in ALL_LESSONS for word in lesson.words]

# ============================================================
# ГРАММАТИЧЕСКИЕ ПРАВИЛА
# ============================================================
GRAMMAR_RULES = [
    GrammarRule(
        id="g1",
        title="To Be (am/is/are)",
        level=1,
        explanation="Глагол 'to be' используется для описания состояния, профессии, местоположения.\n\n• I → am\n• He/She/It → is\n• You/We/They → are",
        examples=[
            {"english": "I am a student.", "russian": "Я студент."},
            {"english": "She is happy.", "russian": "Она счастлива."},
            {"english": "They are friends.", "russian": "Они друзья."},
        ]
    ),
    GrammarRule(
        id="g2",
        title="Present Simple",
        level=1,
        explanation="Используется для регулярных действий, привычек и фактов.\n\n• I/You/We/They + глагол\n• He/She/It + глагол + s/es",
        examples=[
            {"english": "I work every day.", "russian": "Я работаю каждый день."},
            {"english": "He plays football.", "russian": "Он играет в футбол."},
            {"english": "We live in Moscow.", "russian": "Мы живём в Москве."},
        ]
    ),
    GrammarRule(
        id="g3",
        title="Present Continuous",
        level=2,
        explanation="Действие происходит прямо сейчас, в момент речи.\n\nФормула: am/is/are + глагол + ing",
        examples=[
            {"english": "I am reading a book.", "russian": "Я читаю книгу (сейчас)."},
            {"english": "She is cooking dinner.", "russian": "Она готовит ужин."},
            {"english": "They are playing games.", "russian": "Они играют в игры."},
        ]
    ),
    GrammarRule(
        id="g4",
        title="Past Simple",
        level=2,
        explanation="Действие произошло в прошлом и завершено.\n\n• Правильные: глагол + ed\n• Неправильные: особая форма (went, saw, did...)",
        examples=[
            {"english": "I worked yesterday.", "russian": "Я работал вчера."},
            {"english": "She visited her friend.", "russian": "Она навестила друга."},
            {"english": "We went to the park.", "russian": "Мы ходили в парк."},
        ]
    ),
    GrammarRule(
        id="g5",
        title="Future Simple (will)",
        level=2,
        explanation="Используется для спонтанных решений, предсказаний и обещаний.\n\nФормула: will + глагол (без изменений)",
        examples=[
            {"english": "I will help you.", "russian": "Я помогу тебе."},
            {"english": "It will rain tomorrow.", "russian": "Завтра будет дождь."},
            {"english": "She will call you.", "russian": "Она тебе позвонит."},
        ]
    ),
    GrammarRule(
        id="g6",
        title="Модальные глаголы (can, must, should)",
        level=3,
        explanation="Модальные глаголы выражают возможность, обязанность, совет.\n\n• can — могу, умею\n• must — должен\n• should — следует, стоит",
        examples=[
            {"english": "I can swim.", "russian": "Я умею плавать."},
            {"english": "You must study hard.", "russian": "Ты должен усердно учиться."},
            {"english": "You should rest.", "russian": "Тебе стоит отдохнуть."},
        ]
    ),
]


def get_lesson_by_id(lesson_id: str) -> Lesson | None:
    """Получить урок по ID."""
    for lesson in ALL_LESSONS:
        if lesson.id == lesson_id:
            return lesson
    return None


def get_word_by_id(word_id: str) -> Word | None:
    """Получить слово по ID."""
    for word in ALL_WORDS:
        if word.id == word_id:
            return word
    return None


def get_words_for_level(level: int) -> list[Word]:
    """Получить все слова для определённого уровня."""
    return [w for w in ALL_WORDS if w.level <= level]
