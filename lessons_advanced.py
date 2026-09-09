"""
Уроки уровня B1-B2 (Pre-Intermediate → Intermediate)
20 уроков, 200 слов — разговорный английский
"""

from lessons import Word, Lesson


# ============================================================
# B1 — PRE-INTERMEDIATE (Уроки 27-36)
# ============================================================

# УРОК 27: Эмоции
LESSON_27 = Lesson(
    id="emotions",
    title="😊 Эмоции",
    description="Выражаем чувства",
    level=3,
    words=[
        Word("w261", "Excited", "Взволнованный", "/ɪkˈsaɪtɪd/", "I'm excited about the trip.", "Я взволнован перед поездкой.", "emotions", 3),
        Word("w262", "Nervous", "Нервный", "/ˈnɜːrvəs/", "I feel nervous before exams.", "Я нервничаю перед экзаменами.", "emotions", 3),
        Word("w263", "Proud", "Гордый", "/praʊd/", "I'm proud of you.", "Я горжусь тобой.", "emotions", 3),
        Word("w264", "Angry", "Злой", "/ˈæŋɡri/", "Don't be angry with me.", "Не злись на меня.", "emotions", 3),
        Word("w265", "Sad", "Грустный", "/sæd/", "I feel sad today.", "Мне грустно сегодня.", "emotions", 3),
        Word("w266", "Surprised", "Удивлённый", "/sərˈpraɪzd/", "I was surprised to see him.", "Я удивился, увидев его.", "emotions", 3),
        Word("w267", "Bored", "Скучающий", "/bɔːrd/", "I'm bored at home.", "Мне скучно дома.", "emotions", 3),
        Word("w268", "Worried", "Обеспокоенный", "/ˈwɜːrid/", "Don't be worried.", "Не беспокойся.", "emotions", 3),
        Word("w269", "Confused", "Смущённый", "/kənˈfjuːzd/", "I'm confused about this.", "Я в замешательстве.", "emotions", 3),
        Word("w270", "Disappointed", "Разочарованный", "/ˌdɪsəˈpɔɪntɪd/", "I'm disappointed in you.", "Я разочарован в тебе.", "emotions", 3),
    ]
)

# УРОК 28: Отношения
LESSON_28 = Lesson(
    id="relationships",
    title="💕 Отношения",
    description="Общаемся с людьми",
    level=3,
    words=[
        Word("w271", "Trust", "Доверять", "/trʌst/", "I trust you.", "Я тебе доверяю.", "relationships", 3),
        Word("w272", "Respect", "Уважать", "/rɪˈspekt/", "I respect my parents.", "Я уважаю родителей.", "relationships", 3),
        Word("w273", "Argue", "Спорить", "/ˈɑːrɡjuː/", "We argue sometimes.", "Мы иногда спорим.", "relationships", 3),
        Word("w274", "Forgive", "Прощать", "/fərˈɡɪv/", "Please forgive me.", "Пожалуйста, прости меня.", "relationships", 3),
        Word("w275", "Support", "Поддерживать", "/səˈpɔːrt/", "My friends support me.", "Друзья поддерживают меня.", "relationships", 3),
        Word("w276", "Care", "Заботиться", "/ker/", "I care about you.", "Я забочусь о тебе.", "relationships", 3),
        Word("w277", "Miss", "Скучать", "/mɪs/", "I miss my family.", "Я скучаю по семье.", "relationships", 3),
        Word("w278", "Appreciate", "Ценить", "/əˈpriːʃieɪt/", "I appreciate your help.", "Я ценю твою помощь.", "relationships", 3),
        Word("w279", "Agree", "Соглашаться", "/əˈɡriː/", "I agree with you.", "Я с тобой согласен.", "relationships", 3),
        Word("w280", "Disagree", "Не соглашаться", "/ˌdɪsəˈɡriː/", "I disagree with this.", "Я с этим не согласен.", "relationships", 3),
    ]
)

# УРОК 29: Технологии
LESSON_29 = Lesson(
    id="technology",
    title="💻 Технологии",
    description="Современный мир",
    level=3,
    words=[
        Word("w281", "Computer", "Компьютер", "/kəmˈpjuːtər/", "I work on a computer.", "Я работаю на компьютере.", "tech", 3),
        Word("w282", "Internet", "Интернет", "/ˈɪntərnet/", "The internet is slow.", "Интернет медленный.", "tech", 3),
        Word("w283", "Website", "Веб-сайт", "/ˈwebsaɪt/", "Visit our website.", "Посетите наш сайт.", "tech", 3),
        Word("w284", "Download", "Скачивать", "/ˈdaʊnloʊd/", "Download the app.", "Скачай приложение.", "tech", 3),
        Word("w285", "Password", "Пароль", "/ˈpæswɜːrd/", "Enter your password.", "Введите пароль.", "tech", 3),
        Word("w286", "Screen", "Экран", "/skriːn/", "The screen is broken.", "Экран сломан.", "tech", 3),
        Word("w287", "Battery", "Батарея", "/ˈbætəri/", "My battery is low.", "У меня низкий заряд.", "tech", 3),
        Word("w288", "Update", "Обновление", "/ˈʌpdeɪt/", "Update your software.", "Обнови программу.", "tech", 3),
        Word("w289", "File", "Файл", "/faɪl/", "Send me the file.", "Пришли мне файл.", "tech", 3),
        Word("w290", "Search", "Искать", "/sɜːrtʃ/", "Search on Google.", "Ищи в Google.", "tech", 3),
    ]
)

# УРОК 30: Соцсети
LESSON_30 = Lesson(
    id="social-media",
    title="📱 Соцсети",
    description="Общение онлайн",
    level=3,
    words=[
        Word("w291", "Post", "Пост/публикация", "/poʊst/", "I made a new post.", "Я сделал новый пост.", "social", 3),
        Word("w292", "Like", "Лайк", "/laɪk/", "I liked your photo.", "Мне понравилось твоё фото.", "social", 3),
        Word("w293", "Share", "Делиться", "/ʃer/", "Share this article.", "Поделись статьёй.", "social", 3),
        Word("w294", "Comment", "Комментарий", "/ˈkɑːment/", "Leave a comment.", "Оставь комментарий.", "social", 3),
        Word("w295", "Follow", "Подписываться", "/ˈfɑːloʊ/", "Follow me on Instagram.", "Подпишись на меня в Instagram.", "social", 3),
        Word("w296", "Subscribe", "Подписаться", "/səbˈskraɪb/", "Subscribe to my channel.", "Подпишись на мой канал.", "social", 3),
        Word("w297", "Profile", "Профиль", "/ˈproʊfaɪl/", "Check my profile.", "Посмотри мой профиль.", "social", 3),
        Word("w298", "Notification", "Уведомление", "/ˌnoʊtɪfɪˈkeɪʃn/", "I got a notification.", "Мне пришло уведомление.", "social", 3),
        Word("w299", "Online", "Онлайн", "/ˌɑːnˈlaɪn/", "Are you online?", "Ты онлайн?", "social", 3),
        Word("w300", "Offline", "Оффлайн", "/ˌɔːfˈlaɪn/", "I'm offline now.", "Я сейчас оффлайн.", "social", 3),
    ]
)

# УРОК 31: Образование
LESSON_31 = Lesson(
    id="education",
    title="🎓 Образование",
    description="Учёба и знания",
    level=3,
    words=[
        Word("w301", "Study", "Учиться", "/ˈstʌdi/", "I study English.", "Я учу английский.", "education", 3),
        Word("w302", "Learn", "Изучать", "/lɜːrn/", "I want to learn French.", "Я хочу учить французский.", "education", 3),
        Word("w303", "Teach", "Учить (кого-то)", "/tiːtʃ/", "She teaches math.", "Она преподаёт математику.", "education", 3),
        Word("w304", "Exam", "Экзамен", "/ɪɡˈzæm/", "I have an exam tomorrow.", "У меня завтра экзамен.", "education", 3),
        Word("w305", "Grade", "Оценка", "/ɡreɪd/", "I got a good grade.", "Я получил хорошую оценку.", "education", 3),
        Word("w306", "Homework", "Домашнее задание", "/ˈhoʊmwɜːrk/", "Do your homework.", "Сделай домашку.", "education", 3),
        Word("w307", "University", "Университет", "/ˌjuːnɪˈvɜːrsɪti/", "I study at university.", "Я учусь в университете.", "education", 3),
        Word("w308", "Degree", "Степень/диплом", "/dɪˈɡriː/", "I have a degree in physics.", "У меня степень по физике.", "education", 3),
        Word("w309", "Skill", "Навык", "/skɪl/", "I want to improve my skills.", "Я хочу улучшить навыки.", "education", 3),
        Word("w310", "Practice", "Практика", "/ˈpræktɪs/", "Practice makes perfect.", "Практика делает совершенным.", "education", 3),
    ]
)

# УРОК 32: Бизнес
LESSON_32 = Lesson(
    id="business",
    title="💰 Бизнес",
    description="Деловое общение",
    level=3,
    words=[
        Word("w311", "Company", "Компания", "/ˈkʌmpəni/", "I work for a big company.", "Я работаю в большой компании.", "business", 3),
        Word("w312", "Customer", "Клиент", "/ˈkʌstəmər/", "The customer is always right.", "Клиент всегда прав.", "business", 3),
        Word("w313", "Product", "Продукт", "/ˈprɑːdʌkt/", "Our product is new.", "Наш продукт новый.", "business", 3),
        Word("w314", "Service", "Услуга", "/ˈsɜːrvɪs/", "The service is excellent.", "Услуга отличная.", "business", 3),
        Word("w315", "Deal", "Сделка", "/diːl/", "We made a deal.", "Мы заключили сделку.", "business", 3),
        Word("w316", "Contract", "Контракт", "/ˈkɑːntrækt/", "Sign the contract.", "Подпиши контракт.", "business", 3),
        Word("w317", "Profit", "Прибыль", "/ˈprɑːfɪt/", "The profit is high.", "Прибыль высокая.", "business", 3),
        Word("w318", "Invest", "Инвестировать", "/ɪnˈvest/", "I invest in stocks.", "Я инвестирую в акции.", "business", 3),
        Word("w319", "Budget", "Бюджет", "/ˈbʌdʒɪt/", "We need a budget.", "Нам нужен бюджет.", "business", 3),
        Word("w320", "Negotiate", "Вести переговоры", "/nɪˈɡoʊʃieɪt/", "Let's negotiate the price.", "Давай обсудим цену.", "business", 3),
    ]
)

# УРОК 33: Новости
LESSON_33 = Lesson(
    id="news",
    title="📰 Новости",
    description="Медиа и информация",
    level=3,
    words=[
        Word("w321", "News", "Новости", "/nuːz/", "I read the news every day.", "Я читаю новости каждый день.", "media", 3),
        Word("w322", "Journalist", "Журналист", "/ˈdʒɜːrnəlɪst/", "The journalist writes articles.", "Журналист пишет статьи.", "media", 3),
        Word("w323", "Article", "Статья", "/ˈɑːrtɪkl/", "I read an interesting article.", "Я прочитал интересную статью.", "media", 3),
        Word("w324", "Report", "Сообщение/отчёт", "/rɪˈpɔːrt/", "The report is ready.", "Отчёт готов.", "media", 3),
        Word("w325", "Interview", "Интервью", "/ˈɪntərvjuː/", "I have an interview today.", "У меня сегодня интервью.", "media", 3),
        Word("w326", "Headline", "Заголовок", "/ˈhedlaɪn/", "Read the headline.", "Прочитай заголовок.", "media", 3),
        Word("w327", "Source", "Источник", "/sɔːrs/", "The source is reliable.", "Источник надёжный.", "media", 3),
        Word("w328", "Truth", "Правда", "/truːθ/", "Tell me the truth.", "Скажи мне правду.", "media", 3),
        Word("w329", "Fake", "Фейковый", "/feɪk/", "This is fake news.", "Это фейковые новости.", "media", 3),
        Word("w330", "Inform", "Информировать", "/ɪnˈfɔːrm/", "I need to inform you.", "Мне нужно вас проинформировать.", "media", 3),
    ]
)

# УРОК 34: Культура
LESSON_34 = Lesson(
    id="culture",
    title="🎭 Культура",
    description="Искусство и традиции",
    level=3,
    words=[
        Word("w331", "Art", "Искусство", "/ɑːrt/", "I love modern art.", "Я люблю современное искусство.", "culture", 3),
        Word("w332", "Museum", "Музей", "/mjuːˈziːəm/", "Let's visit the museum.", "Давай посетим музей.", "culture", 3),
        Word("w333", "Theater", "Театр", "/ˈθiːətər/", "We go to the theater.", "Мы ходим в театр.", "culture", 3),
        Word("w334", "Concert", "Концерт", "/ˈkɑːnsərt/", "The concert was amazing.", "Концерт был потрясающим.", "culture", 3),
        Word("w335", "Exhibition", "Выставка", "/ˌeksɪˈbɪʃn/", "The exhibition is interesting.", "Выставка интересная.", "culture", 3),
        Word("w336", "Tradition", "Традиция", "/trəˈdɪʃn/", "It's a family tradition.", "Это семейная традиция.", "culture", 3),
        Word("w337", "Custom", "Обычай", "/ˈkʌstəm/", "It's a local custom.", "Это местный обычай.", "culture", 3),
        Word("w338", "Festival", "Фестиваль", "/ˈfestɪvl/", "The festival is fun.", "Фестиваль весёлый.", "culture", 3),
        Word("w339", "Culture", "Культура", "/ˈkʌltʃər/", "I study Russian culture.", "Я изучаю русскую культуру.", "culture", 3),
        Word("w340", "History", "История", "/ˈhɪstəri/", "I love history.", "Я люблю историю.", "culture", 3),
    ]
)

# УРОК 35: Спорт
LESSON_35 = Lesson(
    id="sports",
    title="⚽ Спорт",
    description="Спорт и фитнес",
    level=3,
    words=[
        Word("w341", "Football", "Футбол", "/ˈfʊtbɔːl/", "I play football.", "Я играю в футбол.", "sports", 3),
        Word("w342", "Basketball", "Баскетбол", "/ˈbæskɪtbɔːl/", "Basketball is popular.", "Баскетбол популярен.", "sports", 3),
        Word("w343", "Swimming", "Плавание", "/ˈswɪmɪŋ/", "Swimming is healthy.", "Плавание полезно.", "sports", 3),
        Word("w344", "Running", "Бег", "/ˈrʌnɪŋ/", "I go running every morning.", "Я бегаю каждое утро.", "sports", 3),
        Word("w345", "Gym", "Тренажёрный зал", "/dʒɪm/", "I work out at the gym.", "Я тренируюсь в зале.", "sports", 3),
        Word("w346", "Coach", "Тренер", "/koʊtʃ/", "My coach is strict.", "Мой тренер строгий.", "sports", 3),
        Word("w347", "Team", "Команда", "/tiːm/", "Our team won.", "Наша команда победила.", "sports", 3),
        Word("w348", "Champion", "Чемпион", "/ˈtʃæmpiən/", "He is the champion.", "Он чемпион.", "sports", 3),
        Word("w349", "Score", "Счёт", "/skɔːr/", "What's the score?", "Какой счёт?", "sports", 3),
        Word("w350", "Win", "Побеждать", "/wɪn/", "We want to win.", "Мы хотим победить.", "sports", 3),
    ]
)

# УРОК 36: Экология
LESSON_36 = Lesson(
    id="ecology",
    title="🌍 Экология",
    description="Окружающий мир",
    level=3,
    words=[
        Word("w351", "Nature", "Природа", "/ˈneɪtʃər/", "I love nature.", "Я люблю природу.", "ecology", 3),
        Word("w352", "Forest", "Лес", "/ˈfɔːrɪst/", "The forest is beautiful.", "Лес красивый.", "ecology", 3),
        Word("w353", "Ocean", "Океан", "/ˈoʊʃn/", "The ocean is deep.", "Океан глубокий.", "ecology", 3),
        Word("w354", "Pollution", "Загрязнение", "/pəˈluːʃn/", "Air pollution is bad.", "Загрязнение воздуха плохое.", "ecology", 3),
        Word("w355", "Recycle", "Перерабатывать", "/riːˈsaɪkl/", "We should recycle.", "Мы должны перерабатывать.", "ecology", 3),
        Word("w356", "Energy", "Энергия", "/ˈenərdʒi/", "Save energy.", "Береги энергию.", "ecology", 3),
        Word("w357", "Protect", "Защищать", "/prəˈtekt/", "Protect the environment.", "Защищай окружающую среду.", "ecology", 3),
        Word("w358", "Climate", "Климат", "/ˈklaɪmɪt/", "Climate change is real.", "Изменение климата реально.", "ecology", 3),
        Word("w359", "Waste", "Отходы", "/weɪst/", "Don't waste food.", "Не выбрасывай еду.", "ecology", 3),
        Word("w360", "Earth", "Земля", "/ɜːrθ/", "We must save the Earth.", "Мы должны спасти Землю.", "ecology", 3),
    ]
)


# ============================================================
# B2 — INTERMEDIATE (Уроки 37-46)
# ============================================================

# УРОК 37: Фразовые глаголы 1
LESSON_37 = Lesson(
    id="phrasal-verbs-1",
    title="🔤 Фразовые глаголы 1",
    description="Самые частые фразовые глаголы",
    level=4,
    words=[
        Word("w361", "Look for", "Искать", "/lʊk fɔːr/", "I'm looking for my keys.", "Я ищу ключи.", "phrasal", 4),
        Word("w362", "Look after", "Заботиться", "/lʊk ˈæftər/", "Look after the children.", "Позаботься о детях.", "phrasal", 4),
        Word("w363", "Look forward to", "С нетерпением ждать", "/lʊk ˈfɔːrwərd tuː/", "I look forward to meeting you.", "С нетерпением жду встречи.", "phrasal", 4),
        Word("w364", "Give up", "Сдаваться", "/ɡɪv ʌp/", "Don't give up!", "Не сдавайся!", "phrasal", 4),
        Word("w365", "Give away", "Отдавать/дарить", "/ɡɪv əˈweɪ/", "She gave away her clothes.", "Она отдала одежду.", "phrasal", 4),
        Word("w366", "Turn on", "Включать", "/tɜːrn ɑːn/", "Turn on the light.", "Включи свет.", "phrasal", 4),
        Word("w367", "Turn off", "Выключать", "/tɜːrn ɔːf/", "Turn off the TV.", "Выключи ТВ.", "phrasal", 4),
        Word("w368", "Pick up", "Поднимать/забирать", "/pɪk ʌp/", "Pick up the phone.", "Подними трубку.", "phrasal", 4),
        Word("w369", "Put on", "Надевать", "/pʊt ɑːn/", "Put on your coat.", "Надень пальто.", "phrasal", 4),
        Word("w370", "Take off", "Снимать/взлетать", "/teɪk ɔːf/", "Take off your shoes.", "Сними обувь.", "phrasal", 4),
    ]
)

# УРОК 38: Фразовые глаголы 2
LESSON_38 = Lesson(
    id="phrasal-verbs-2",
    title="🔤 Фразовые глаголы 2",
    description="Ещё больше фразовых глаголов",
    level=4,
    words=[
        Word("w371", "Come up with", "Придумать", "/kʌm ʌp wɪð/", "Come up with an idea.", "Придумай идею.", "phrasal", 4),
        Word("w372", "Get along", "Ладить", "/ɡet əˈlɔːŋ/", "I get along with everyone.", "Я лажу со всеми.", "phrasal", 4),
        Word("w373", "Get over", "Пережить", "/ɡet ˈoʊvər/", "I'll get over it.", "Я переживу это.", "phrasal", 4),
        Word("w374", "Break down", "Ломаться", "/breɪk daʊn/", "My car broke down.", "Моя машина сломалась.", "phrasal", 4),
        Word("w375", "Bring up", "Поднимать тему", "/brɪŋ ʌp/", "Don't bring up that topic.", "Не поднимай эту тему.", "phrasal", 4),
        Word("w376", "Figure out", "Разобраться", "/ˈfɪɡər aʊt/", "I can't figure it out.", "Я не могу разобраться.", "phrasal", 4),
        Word("w377", "Run out of", "Заканчиваться", "/rʌn aʊt əv/", "We ran out of milk.", "У нас закончилось молоко.", "phrasal", 4),
        Word("w378", "Look up to", "Уважать/равняться", "/lʊk ʌp tuː/", "I look up to my dad.", "Я равняюсь на папу.", "phrasal", 4),
        Word("w379", "Put off", "Откладывать", "/pʊt ɔːf/", "Don't put it off.", "Не откладывай.", "phrasal", 4),
        Word("w380", "Work out", "Решать/тренироваться", "/wɜːrk aʊt/", "We need to work this out.", "Нам нужно это решить.", "phrasal", 4),
    ]
)

# УРОК 39: Идиомы 1
LESSON_39 = Lesson(
    id="idioms-1",
    title="💡 Идиомы 1",
    description="Популярные английские идиомы",
    level=4,
    words=[
        Word("w381", "Break the ice", "Разрядить обстановку", "/breɪk ðə aɪs/", "He broke the ice with a joke.", "Он разрядил обстановку шуткой.", "idioms", 4),
        Word("w382", "Hit the nail on the head", "В точку", "/hɪt ðə neɪl ɑːn ðə hed/", "You hit the nail on the head.", "Ты попал в точку.", "idioms", 4),
        Word("w383", "Piece of cake", "Легко/проще простого", "/piːs əv keɪk/", "The exam was a piece of cake.", "Экзамен был проще простого.", "idioms", 4),
        Word("w384", "Under the weather", "Плохо себя чувствовать", "/ˈʌndər ðə ˈweðər/", "I'm feeling under the weather.", "Я плохо себя чувствую.", "idioms", 4),
        Word("w385", "Cost an arm and a leg", "Очень дорого", "/kɑːst ən ɑːrm ənd ə leɡ/", "That car costs an arm and a leg.", "Та машина стоит целое состояние.", "idioms", 4),
        Word("w386", "Once in a blue moon", "Очень редко", "/wʌns ɪn ə bluː muːn/", "I go there once in a blue moon.", "Я хожу туда раз в сто лет.", "idioms", 4),
        Word("w387", "Kill two birds with one stone", "Убить двух зайцев", "/kɪl tuː bɜːrdz wɪð wʌn stoʊn/", "I killed two birds with one stone.", "Я убил двух зайцев.", "idioms", 4),
        Word("w388", "Spill the beans", "Проболтаться", "/spɪl ðə biːnz/", "Don't spill the beans.", "Не проболтайся.", "idioms", 4),
        Word("w389", "Let the cat out of the bag", "Проболтаться/раскрыть секрет", "/let ðə kæt aʊt əv ðə bæɡ/", "He let the cat out of the bag.", "Он проболтался.", "idioms", 4),
        Word("w390", "Bite the bullet", "Смириться/решиться", "/baɪt ðə ˈbʊlɪt/", "I had to bite the bullet.", "Мне пришлось собраться.", "idioms", 4),
    ]
)

# УРОК 40: Идиомы 2
LESSON_40 = Lesson(
    id="idioms-2",
    title="💡 Идиомы 2",
    description="Ещё больше идиом",
    level=4,
    words=[
        Word("w391", "Beat around the bush", "Ходить вокруг да около", "/biːt əˈraʊnd ðə bʊʃ/", "Stop beating around the bush.", "Хватит ходить вокруг да около.", "idioms", 4),
        Word("w392", "Cut corners", "Делать в спешке", "/kʌt ˈkɔːrnərz/", "Don't cut corners.", "Не халтурь.", "idioms", 4),
        Word("w393", "Get out of hand", "Выйти из-под контроля", "/ɡet aʊt əv hænd/", "The party got out of hand.", "Вечеринка вышла из-под контроля.", "idioms", 4),
        Word("w394", "Hang in there", "Держись", "/hæŋ ɪn ðer/", "Hang in there, it'll be fine.", "Держись, всё будет хорошо.", "idioms", 4),
        Word("w395", "Miss the boat", "Упустить возможность", "/mɪs ðə boʊt/", "I missed the boat on that deal.", "Я упустил возможность.", "idioms", 4),
        Word("w396", "On the same page", "Одного мнения", "/ɑːn ðə seɪm peɪdʒ/", "Are we on the same page?", "Мы одного мнения?", "idioms", 4),
        Word("w397", "See eye to eye", "Полностью соглашаться", "/siː aɪ tuː aɪ/", "We don't see eye to eye.", "Мы не во всём согласны.", "idioms", 4),
        Word("w398", "The ball is in your court", "Решение за тобой", "/ðə bɔːl ɪz ɪn jɔːr kɔːrt/", "The ball is in your court now.", "Теперь решение за тобой.", "idioms", 4),
        Word("w399", "Time flies", "Время летит", "/taɪm flaɪz/", "Time flies when you're having fun.", "Время летит, когда веселишься.", "idioms", 4),
        Word("w400", "When pigs fly", "Когда рак на горе свистнет", "/wen pɪɡz flaɪ/", "I'll do it when pigs fly.", "Я сделаю это, когда рак на горе свистнет.", "idioms", 4),
    ]
)

# УРОК 41: Деловое общение
LESSON_41 = Lesson(
    id="business-english",
    title="💼 Деловой английский",
    description="Профессиональная лексика",
    level=4,
    words=[
        Word("w401", "Deadline", "Дедлайн", "/ˈdedlaɪn/", "The deadline is tomorrow.", "Дедлайн завтра.", "business", 4),
        Word("w402", "Schedule", "Расписание", "/ˈskedʒuːl/", "Check the schedule.", "Проверь расписание.", "business", 4),
        Word("w403", "Agenda", "Повестка", "/əˈdʒendə/", "What's on the agenda?", "Что в повестке?", "business", 4),
        Word("w404", "Proposal", "Предложение", "/prəˈpoʊzl/", "I sent a proposal.", "Я отправил предложение.", "business", 4),
        Word("w405", "Feedback", "Обратная связь", "/ˈfiːdbæk/", "Give me some feedback.", "Дай мне обратную связь.", "business", 4),
        Word("w406", "Strategy", "Стратегия", "/ˈstrætədʒi/", "We need a new strategy.", "Нам нужна новая стратегия.", "business", 4),
        Word("w407", "Goal", "Цель", "/ɡoʊl/", "What's your goal?", "Какая у тебя цель?", "business", 4),
        Word("w408", "Achieve", "Достигать", "/əˈtʃiːv/", "I achieved my goal.", "Я достиг цели.", "business", 4),
        Word("w409", "Improve", "Улучшать", "/ɪmˈpruːv/", "We need to improve.", "Нам нужно улучшиться.", "business", 4),
        Word("w410", "Challenge", "Вызов/проблема", "/ˈtʃælɪndʒ/", "It's a big challenge.", "Это большой вызов.", "business", 4),
    ]
)

# УРОК 42: Мнения
LESSON_42 = Lesson(
    id="opinions",
    title="💭 Мнения",
    description="Выражаем своё мнение",
    level=4,
    words=[
        Word("w411", "In my opinion", "По моему мнению", "/ɪn maɪ əˈpɪnjən/", "In my opinion, it's wrong.", "По моему мнению, это неправильно.", "opinions", 4),
        Word("w412", "I think", "Я думаю", "/aɪ θɪŋk/", "I think you're right.", "Я думаю, ты прав.", "opinions", 4),
        Word("w413", "I believe", "Я считаю", "/aɪ bɪˈliːv/", "I believe in you.", "Я в тебя верю.", "opinions", 4),
        Word("w414", "I suppose", "Я полагаю", "/aɪ səˈpoʊz/", "I suppose you're right.", "Полагаю, ты прав.", "opinions", 4),
        Word("w415", "To be honest", "Честно говоря", "/tuː bi ˈɑːnɪst/", "To be honest, I don't like it.", "Честно говоря, мне не нравится.", "opinions", 4),
        Word("w416", "Actually", "На самом деле", "/ˈæktʃuəli/", "Actually, I disagree.", "На самом деле, я не согласен.", "opinions", 4),
        Word("w417", "Obviously", "Очевидно", "/ˈɑːbviəsli/", "Obviously, he's wrong.", "Очевидно, он не прав.", "opinions", 4),
        Word("w418", "Probably", "Вероятно", "/ˈprɑːbəbli/", "It'll probably rain.", "Вероятно, будет дождь.", "opinions", 4),
        Word("w419", "Definitely", "Определённо", "/ˈdefɪnɪtli/", "I definitely agree.", "Я определённо согласен.", "opinions", 4),
        Word("w420", "Somehow", "Как-нибудь", "/ˈsʌmhaʊ/", "We'll fix it somehow.", "Мы как-нибудь это исправим.", "opinions", 4),
    ]
)

# УРОК 43: Путешествия продвинуто
LESSON_43 = Lesson(
    id="travel-advanced",
    title="🌍 Путешествия продвинуто",
    description="Сложные ситуации в поездках",
    level=4,
    words=[
        Word("w421", "Delay", "Задержка", "/dɪˈleɪ/", "The flight is delayed.", "Рейс задерживается.", "travel", 4),
        Word("w422", "Cancel", "Отменять", "/ˈkænsl/", "They cancelled the flight.", "Они отменили рейс.", "travel", 4),
        Word("w423", "Complaint", "Жалоба", "/kəmˈpleɪnt/", "I have a complaint.", "У меня жалоба.", "travel", 4),
        Word("w424", "Refund", "Возврат", "/ˈriːfʌnd/", "I want a refund.", "Я хочу возврат.", "travel", 4),
        Word("w425", "Insurance", "Страховка", "/ɪnˈʃʊrəns/", "Do you have insurance?", "У тебя есть страховка?", "travel", 4),
        Word("w426", "Embassy", "Посольство", "/ˈembəsi/", "Go to the embassy.", "Иди в посольство.", "travel", 4),
        Word("w427", "Currency", "Валюта", "/ˈkɜːrənsi/", "What's the local currency?", "Какая местная валюта?", "travel", 4),
        Word("w428", "Exchange", "Обменивать", "/ɪksˈtʃeɪndʒ/", "Where can I exchange money?", "Где можно обменять деньги?", "travel", 4),
        Word("w429", "Destination", "Место назначения", "/ˌdestɪˈneɪʃn/", "Our destination is Paris.", "Наше место назначения — Париж.", "travel", 4),
        Word("w430", "Adventure", "Приключение", "/ədˈventʃər/", "It was a great adventure.", "Это было отличное приключение.", "travel", 4),
    ]
)

# УРОК 44: Сленг
LESSON_44 = Lesson(
    id="slang",
    title="🗣️ Сленг",
    description="Неформальный английский",
    level=4,
    words=[
        Word("w431", "Cool", "Круто", "/kuːl/", "That's cool!", "Это круто!", "slang", 4),
        Word("w432", "Awesome", "Потрясающе", "/ˈɔːsəm/", "Awesome job!", "Потрясающая работа!", "slang", 4),
        Word("w433", "Chill", "Расслабляться", "/tʃɪl/", "Let's chill tonight.", "Давай расслабимся сегодня.", "slang", 4),
        Word("w434", "Buddy", "Дружок", "/ˈbʌdi/", "Hey, buddy!", "Привет, дружок!", "slang", 4),
        Word("w435", "Gonna", "Собираться (going to)", "/ˈɡɒnə/", "I'm gonna sleep.", "Я собираюсь спать.", "slang", 4),
        Word("w436", "Wanna", "Хотеть (want to)", "/ˈwɑːnə/", "I wanna go home.", "Я хочу домой.", "slang", 4),
        Word("w437", "Dude", "Чувак", "/duːd/", "Hey, dude!", "Привет, чувак!", "slang", 4),
        Word("w438", "Freak out", "Паниковать", "/friːk aʊt/", "Don't freak out.", "Не паникуй.", "slang", 4),
        Word("w439", "Hang out", "Тусоваться", "/hæŋ aʊt/", "Let's hang out.", "Давай потусуемся.", "slang", 4),
        Word("w440", "No way!", "Не может быть!", "/noʊ weɪ/", "No way! Really?", "Не может быть! Серьёзно?", "slang", 4),
    ]
)

# УРОК 45: Дебаты
LESSON_45 = Lesson(
    id="debates",
    title="🗯️ Дебаты",
    description="Аргументируем позицию",
    level=4,
    words=[
        Word("w441", "Advantage", "Преимущество", "/ədˈvæntɪdʒ/", "The advantage is clear.", "Преимущество очевидно.", "debates", 4),
        Word("w442", "Disadvantage", "Недостаток", "/ˌdɪsədˈvæntɪdʒ/", "There's a disadvantage.", "Есть недостаток.", "debates", 4),
        Word("w443", "Therefore", "Поэтому", "/ˈðerfɔːr/", "Therefore, we must act.", "Поэтому мы должны действовать.", "debates", 4),
        Word("w444", "However", "Однако", "/haʊˈevər/", "However, I disagree.", "Однако, я не согласен.", "debates", 4),
        Word("w445", "Furthermore", "Более того", "/ˈfɜːrðərmɔːr/", "Furthermore, it's expensive.", "Более того, это дорого.", "debates", 4),
        Word("w446", "Consequently", "Следовательно", "/ˈkɑːnsɪkwentli/", "Consequently, we failed.", "Следовательно, мы провалились.", "debates", 4),
        Word("w447", "Although", "Хотя", "/ɔːlˈðoʊ/", "Although it's hard, I'll try.", "Хотя это сложно, я попробую.", "debates", 4),
        Word("w448", "Despite", "Несмотря на", "/dɪˈspaɪt/", "Despite the rain, we went.", "Несмотря на дождь, мы пошли.", "debates", 4),
        Word("w449", "Moreover", "Кроме того", "/mɔːrˈoʊvər/", "Moreover, it's free.", "Кроме того, это бесплатно.", "debates", 4),
        Word("w450", "In conclusion", "В заключение", "/ɪn kənˈkluːʒn/", "In conclusion, I agree.", "В заключение, я согласен.", "debates", 4),
    ]
)

# УРОК 46: Юмор
LESSON_46 = Lesson(
    id="humor",
    title="😄 Юмор",
    description="Шутки и забавные фразы",
    level=4,
    words=[
        Word("w451", "Joke", "Шутка", "/dʒoʊk/", "That's a good joke.", "Это хорошая шутка.", "humor", 4),
        Word("w452", "Funny", "Смешной", "/ˈfʌni/", "You're funny!", "Ты смешной!", "humor", 4),
        Word("w453", "Laugh", "Смеяться", "/læf/", "Make me laugh.", "Рассмеши меня.", "humor", 4),
        Word("w454", "Smile", "Улыбаться", "/smaɪl/", "She smiled at me.", "Она улыбнулась мне.", "humor", 4),
        Word("w455", "Comedy", "Комедия", "/ˈkɑːmɪdi/", "I love comedy.", "Я люблю комедии.", "humor", 4),
        Word("w456", "Pun", "Игра слов", "/pʌn/", "That's a clever pun.", "Это остроумная игра слов.", "humor", 4),
        Word("w457", "Sarcasm", "Сарказм", "/ˈsɑːrkæzəm/", "His sarcasm is funny.", "Его сарказм смешной.", "humor", 4),
        Word("w458", "Tease", "Дразнить", "/tiːz/", "Don't tease me.", "Не дразни меня.", "humor", 4),
        Word("w459", "Prank", "Розыгрыш", "/præŋk/", "It was just a prank.", "Это был просто розыгрыш.", "humor", 4),
        Word("w460", "Hilarious", "Уморительный", "/hɪˈleriəs/", "That's hilarious!", "Это уморительно!", "humor", 4),
    ]
)


# Список всех уроков B1-B2
ALL_LESSONS_B1_B2 = [
    LESSON_27, LESSON_28, LESSON_29, LESSON_30, LESSON_31,
    LESSON_32, LESSON_33, LESSON_34, LESSON_35, LESSON_36,
    LESSON_37, LESSON_38, LESSON_39, LESSON_40, LESSON_41,
    LESSON_42, LESSON_43, LESSON_44, LESSON_45, LESSON_46,
]
