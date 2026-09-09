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

# Импортируем уроки из дополнительных файлов
try:
    from lessons_basic import ALL_LESSONS_A1_A2
    from lessons_advanced import ALL_LESSONS_B1_B2
    ALL_LESSONS = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5, LESSON_6] + ALL_LESSONS_A1_A2 + ALL_LESSONS_B1_B2
except ImportError:
    # Если дополнительные файлы не найдены, используем только базовые уроки
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
    GrammarRule(
        id="g7",
        title="Present Perfect",
        level=3,
        explanation="Действие произошло в прошлом, но результат важен сейчас.\n\nФормула: have/has + V3 (третья форма глагола)\n\nИспользуем с: already, just, never, ever, yet",
        examples=[
            {"english": "I have finished my work.", "russian": "Я закончил работу."},
            {"english": "She has never been to Paris.", "russian": "Она никогда не была в Париже."},
            {"english": "Have you ever seen a lion?", "russian": "Ты когда-нибудь видел льва?"},
        ]
    ),
    GrammarRule(
        id="g8",
        title="Past Continuous",
        level=3,
        explanation="Действие происходило в определённый момент в прошлом.\n\nФормула: was/were + глагол + ing",
        examples=[
            {"english": "I was reading at 8 PM.", "russian": "Я читал в 8 вечера."},
            {"english": "They were playing football.", "russian": "Они играли в футбол."},
            {"english": "What were you doing?", "russian": "Что ты делал?"},
        ]
    ),
    GrammarRule(
        id="g9",
        title="Сравнительные степени",
        level=2,
        explanation="Сравниваем предметы и людей.\n\n• Короткие прилагательные: + er (tall → taller)\n• Длинные: more (beautiful → more beautiful)\n• Неправильные: good → better, bad → worse",
        examples=[
            {"english": "She is taller than me.", "russian": "Она выше меня."},
            {"english": "This book is more interesting.", "russian": "Эта книга интереснее."},
            {"english": "He is the best student.", "russian": "Он лучший студент."},
        ]
    ),
    GrammarRule(
        id="g10",
        title="Артикли (a/an/the)",
        level=1,
        explanation="• a/an — неопределённый (один из многих)\n  • a — перед согласным звуком\n  • an — перед гласным звуком\n• the — определённый (конкретный предмет)",
        examples=[
            {"english": "I have a cat.", "russian": "У меня есть кошка."},
            {"english": "She is an engineer.", "russian": "Она инженер."},
            {"english": "The book is on the table.", "russian": "Книга на столе (конкретная)."},
        ]
    ),
    GrammarRule(
        id="g11",
        title="Множественное число",
        level=1,
        explanation="Большинство слов: + s (book → books)\nОкончания -s, -sh, -ch, -x: + es (bus → buses)\nОкончание -y после согласной: -y → -ies (city → cities)\nНеправильные: man → men, child → children",
        examples=[
            {"english": "Two dogs, three cats.", "russian": "Две собаки, три кошки."},
            {"english": "Five buses, ten boxes.", "russian": "Пять автобусов, десять коробок."},
            {"english": "Many children, some men.", "russian": "Много детей, несколько мужчин."},
        ]
    ),
    GrammarRule(
        id="g12",
        title="Отрицания",
        level=1,
        explanation="• am/is/are + not\n• do/does + not + глагол (Present Simple)\n• did + not + глагол (Past Simple)\n• will + not (won't) (Future Simple)",
        examples=[
            {"english": "I am not tired.", "russian": "Я не устал."},
            {"english": "She doesn't like coffee.", "russian": "Она не любит кофе."},
            {"english": "They didn't come.", "russian": "Они не пришли."},
        ]
    ),
    GrammarRule(
        id="g13",
        title="Вопросы",
        level=1,
        explanation="Общий вопрос: Do/Does/Did + subject + verb?\nС вопросом к глаголу to be: Am/Is/Are + subject?\nСпециальные вопросы: What, Where, When, Why, How + вспом. глагол",
        examples=[
            {"english": "Do you like music?", "russian": "Ты любишь музыку?"},
            {"english": "Where do you live?", "russian": "Где ты живёшь?"},
            {"english": "What did you do?", "russian": "Что ты сделал?"},
        ]
    ),
    GrammarRule(
        id="g14",
        title="Предлоги времени (in/on/at)",
        level=2,
        explanation="• at — точное время (at 5 o'clock, at night)\n• on — дни и даты (on Monday, on May 5th)\n• in — месяцы, годы, части дня (in May, in 2024, in the morning)",
        examples=[
            {"english": "I wake up at 7.", "russian": "Я просыпаюсь в 7."},
            {"english": "We meet on Fridays.", "russian": "Мы встречаемся по пятницам."},
            {"english": "She was born in 1990.", "russian": "Она родилась в 1990."},
        ]
    ),
    GrammarRule(
        id="g15",
        title="Предлоги места (in/on/at)",
        level=2,
        explanation="• at — конкретное место (at the door, at school)\n• on — поверхность (on the table, on the wall)\n• in — внутри (in the room, in the box)",
        examples=[
            {"english": "I'm at home.", "russian": "Я дома."},
            {"english": "The book is on the table.", "russian": "Книга на столе."},
            {"english": "She is in the kitchen.", "russian": "Она на кухне."},
        ]
    ),
    GrammarRule(
        id="g16",
        title="Conditionals (Zero & First)",
        level=3,
        explanation="Zero: If + Present Simple, Present Simple (факты)\nFirst: If + Present Simple, will + verb (реальное будущее)\n\nПеревод: Если..., то...",
        examples=[
            {"english": "If you heat water, it boils.", "russian": "Если нагреть воду, она кипит."},
            {"english": "If it rains, I will stay home.", "russian": "Если пойдёт дождь, я останусь дома."},
            {"english": "If you study, you will pass.", "russian": "Если будешь учиться, сдашь."},
        ]
    ),
    GrammarRule(
        id="g17",
        title="Passive Voice",
        level=4,
        explanation="Страдательный залог — действие направлено на предмет.\n\nФормула: be + V3\n\nPresent: is/are + V3\nPast: was/were + V3\nFuture: will be + V3",
        examples=[
            {"english": "The book was written by Tolstoy.", "russian": "Книга написана Толстым."},
            {"english": "English is spoken worldwide.", "russian": "На английском говорят по всему миру."},
            {"english": "The work will be done tomorrow.", "russian": "Работа будет сделана завтра."},
        ]
    ),
    GrammarRule(
        id="g18",
        title="Reported Speech",
        level=4,
        explanation="Косвенная речь — передаём чужие слова.\n\n• Present Simple → Past Simple\n• will → would\n• can → could\n• today → that day",
        examples=[
            {"english": "He said he was tired.", "russian": "Он сказал, что устал."},
            {"english": "She told me she would come.", "russian": "Она сказала, что придёт."},
            {"english": "They said they could help.", "russian": "Они сказали, что могут помочь."},
        ]
    ),
    GrammarRule(
        id="g19",
        title="Герундий vs Инфинитив",
        level=3,
        explanation="После некоторых глаголов используем -ing (герундий):\n• enjoy, avoid, finish, mind, suggest\n\nПосле других — to + глагол (инфинитив):\n• want, need, decide, hope, plan",
        examples=[
            {"english": "I enjoy reading.", "russian": "Мне нравится читать."},
            {"english": "She wants to travel.", "russian": "Она хочет путешествовать."},
            {"english": "He decided to stay.", "russian": "Он решил остаться."},
        ]
    ),
    GrammarRule(
        id="g20",
        title="Used to / Would",
        level=4,
        explanation="Используем для привычек в прошлом.\n\n• used to + глагол — раньше делал (но больше нет)\n• would + глагол — часто делал в прошлом",
        examples=[
            {"english": "I used to smoke.", "russian": "Я раньше курил."},
            {"english": "She used to live in Paris.", "russian": "Она раньше жила в Париже."},
            {"english": "We would play in the park.", "russian": "Мы играли в парке (регулярно)."},
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
