"""
Уроки уровня A1-A2 (Beginner → Elementary)
20 уроков, 200 слов — базовый разговорный английский
"""

from lessons import Word, Lesson


# ============================================================
# A1 — BEGINNER (Уроки 7-16)
# ============================================================

# УРОК 7: Числа, даты, время
LESSON_7 = Lesson(
    id="numbers-time",
    title="🔢 Числа и время",
    description="Считаем и говорим о времени",
    level=1,
    words=[
        Word("w61", "One", "Один", "/wʌn/", "I have one brother.", "У меня один брат.", "numbers", 1),
        Word("w62", "Two", "Два", "/tuː/", "I have two cats.", "У меня две кошки.", "numbers", 1),
        Word("w63", "Three", "Три", "/θriː/", "There are three books.", "Там три книги.", "numbers", 1),
        Word("w64", "Ten", "Десять", "/ten/", "I wait ten minutes.", "Я жду десять минут.", "numbers", 1),
        Word("w65", "Hundred", "Сто", "/ˈhʌndrəd/", "It costs one hundred dollars.", "Это стоит сто долларов.", "numbers", 1),
        Word("w66", "Today", "Сегодня", "/təˈdeɪ/", "Today is Monday.", "Сегодня понедельник.", "time", 1),
        Word("w67", "Clock", "Часы", "/klɑːk/", "What time is it on the clock?", "Который час на часах?", "time", 1),
        Word("w68", "Hour", "Час", "/aʊər/", "The movie is two hours long.", "Фильм длится два часа.", "time", 1),
        Word("w69", "Minute", "Минута", "/ˈmɪnɪt/", "Wait five minutes, please.", "Подождите пять минут.", "time", 1),
        Word("w70", "Week", "Неделя", "/wiːk/", "I work five days a week.", "Я работаю пять дней в неделю.", "time", 1),
    ]
)

# УРОК 8: Семья
LESSON_8 = Lesson(
    id="family",
    title="👨‍👩‍👧 Семья",
    description="Рассказываем о семье",
    level=1,
    words=[
        Word("w71", "Mother", "Мама", "/ˈmʌðər/", "My mother is a teacher.", "Моя мама — учитель.", "family", 1),
        Word("w72", "Father", "Папа", "/ˈfɑːðər/", "My father works in a bank.", "Мой папа работает в банке.", "family", 1),
        Word("w73", "Sister", "Сестра", "/ˈsɪstər/", "I have one sister.", "У меня одна сестра.", "family", 1),
        Word("w74", "Brother", "Брат", "/ˈbrʌðər/", "My brother is older.", "Мой брат старше.", "family", 1),
        Word("w75", "Son", "Сын", "/sʌn/", "Their son is five years old.", "Их сыну пять лет.", "family", 1),
        Word("w76", "Daughter", "Дочь", "/ˈdɔːtər/", "She has a daughter.", "У неё есть дочь.", "family", 1),
        Word("w77", "Husband", "Муж", "/ˈhʌzbənd/", "Her husband is tall.", "Её муж высокий.", "family", 1),
        Word("w78", "Wife", "Жена", "/waɪf/", "His wife is kind.", "Его жена добрая.", "family", 1),
        Word("w79", "Grandmother", "Бабушка", "/ˈɡrænmʌðər/", "My grandmother cooks well.", "Моя бабушка хорошо готовит.", "family", 1),
        Word("w80", "Grandfather", "Дедушка", "/ˈɡrænfɑːðər/", "My grandfather is 80.", "Моему дедушке 80.", "family", 1),
    ]
)

# УРОК 9: Дом
LESSON_9 = Lesson(
    id="home",
    title="🏠 Дом",
    description="Комнаты и мебель",
    level=1,
    words=[
        Word("w81", "Kitchen", "Кухня", "/ˈkɪtʃɪn/", "Mom is in the kitchen.", "Мама на кухне.", "rooms", 1),
        Word("w82", "Bedroom", "Спальня", "/ˈbedruːm/", "My bedroom is small.", "Моя спальня маленькая.", "rooms", 1),
        Word("w83", "Bathroom", "Ванная", "/ˈbɑːθruːm/", "The bathroom is clean.", "Ванная чистая.", "rooms", 1),
        Word("w84", "Living room", "Гостиная", "/ˈlɪvɪŋ ruːm/", "We watch TV in the living room.", "Мы смотрим ТВ в гостиной.", "rooms", 1),
        Word("w85", "Table", "Стол", "/ˈteɪbl/", "The book is on the table.", "Книга на столе.", "furniture", 1),
        Word("w86", "Chair", "Стул", "/tʃer/", "Sit on the chair.", "Сядь на стул.", "furniture", 1),
        Word("w87", "Bed", "Кровать", "/bed/", "I go to bed at 11.", "Я ложусь спать в 11.", "furniture", 1),
        Word("w88", "Door", "Дверь", "/dɔːr/", "Close the door, please.", "Закрой дверь, пожалуйста.", "furniture", 1),
        Word("w89", "Window", "Окно", "/ˈwɪndoʊ/", "Open the window.", "Открой окно.", "furniture", 1),
        Word("w90", "Key", "Ключ", "/kiː/", "Where are my keys?", "Где мои ключи?", "furniture", 1),
    ]
)

# УРОК 10: Еда и напитки
LESSON_10 = Lesson(
    id="food-drinks",
    title="🍕 Еда и напитки",
    description="Что мы едим и пьём",
    level=1,
    words=[
        Word("w91", "Bread", "Хлеб", "/bred/", "I buy bread every day.", "Я покупаю хлеб каждый день.", "food", 1),
        Word("w92", "Milk", "Молоко", "/mɪlk/", "Children drink milk.", "Дети пьют молоко.", "drinks", 1),
        Word("w93", "Coffee", "Кофе", "/ˈkɔːfi/", "I drink coffee in the morning.", "Я пью кофе утром.", "drinks", 1),
        Word("w94", "Tea", "Чай", "/tiː/", "Would you like some tea?", "Хотите чаю?", "drinks", 1),
        Word("w95", "Apple", "Яблоко", "/ˈæpl/", "An apple a day keeps the doctor away.", "Яблоко в день — и доктор не нужен.", "food", 1),
        Word("w96", "Meat", "Мясо", "/miːt/", "I don't eat meat.", "Я не ем мясо.", "food", 1),
        Word("w97", "Fish", "Рыба", "/fɪʃ/", "Fish is healthy.", "Рыба полезная.", "food", 1),
        Word("w98", "Sugar", "Сахар", "/ˈʃʊɡər/", "No sugar, please.", "Без сахара, пожалуйста.", "food", 1),
        Word("w99", "Salt", "Соль", "/sɔːlt/", "Pass me the salt.", "Передай мне соль.", "food", 1),
        Word("w100", "Breakfast", "Завтрак", "/ˈbrekfəst/", "Breakfast is at 8.", "Завтрак в 8.", "meals", 1),
    ]
)

# УРОК 11: Одежда и цвета
LESSON_11 = Lesson(
    id="clothes-colors",
    title="👕 Одежда и цвета",
    description="Что мы носим",
    level=1,
    words=[
        Word("w101", "Shirt", "Рубашка", "/ʃɜːrt/", "He wears a white shirt.", "Он носит белую рубашку.", "clothes", 1),
        Word("w102", "Pants", "Брюки", "/pænts/", "These pants are new.", "Эти брюки новые.", "clothes", 1),
        Word("w103", "Dress", "Платье", "/dres/", "She has a beautiful dress.", "У неё красивое платье.", "clothes", 1),
        Word("w104", "Shoes", "Обувь", "/ʃuːz/", "New shoes are expensive.", "Новая обувь дорогая.", "clothes", 1),
        Word("w105", "Jacket", "Куртка", "/ˈdʒækɪt/", "It's cold, wear a jacket.", "Холодно, надень куртку.", "clothes", 1),
        Word("w106", "Red", "Красный", "/red/", "The car is red.", "Машина красная.", "colors", 1),
        Word("w107", "Blue", "Синий", "/bluː/", "The sky is blue.", "Небо синее.", "colors", 1),
        Word("w108", "Green", "Зелёный", "/ɡriːn/", "Grass is green.", "Трава зелёная.", "colors", 1),
        Word("w109", "Black", "Чёрный", "/blæk/", "I like black coffee.", "Я люблю чёрный кофе.", "colors", 1),
        Word("w110", "White", "Белый", "/waɪt/", "Snow is white.", "Снег белый.", "colors", 1),
    ]
)

# УРОК 12: Тело
LESSON_12 = Lesson(
    id="body",
    title="🦵 Тело",
    description="Части тела",
    level=1,
    words=[
        Word("w111", "Head", "Голова", "/hed/", "My head hurts.", "У меня болит голова.", "body", 1),
        Word("w112", "Hand", "Рука (кисть)", "/hænd/", "Wash your hands.", "Помой руки.", "body", 1),
        Word("w113", "Eye", "Глаз", "/aɪ/", "She has blue eyes.", "У неё голубые глаза.", "body", 1),
        Word("w114", "Ear", "Ухо", "/ɪr/", "I hear with my ears.", "Я слышу ушами.", "body", 1),
        Word("w115", "Mouth", "Рот", "/maʊθ/", "Open your mouth.", "Открой рот.", "body", 1),
        Word("w116", "Leg", "Нога", "/leɡ/", "My leg is tired.", "Моя нога устала.", "body", 1),
        Word("w117", "Heart", "Сердце", "/hɑːrt/", "My heart beats fast.", "Моё сердце бьётся быстро.", "body", 1),
        Word("w118", "Hair", "Волосы", "/her/", "She has long hair.", "У неё длинные волосы.", "body", 1),
        Word("w119", "Face", "Лицо", "/feɪs/", "Wash your face.", "Умой лицо.", "body", 1),
        Word("w120", "Finger", "Палец", "/ˈfɪŋɡər/", "I cut my finger.", "Я порезал палец.", "body", 1),
    ]
)

# УРОК 13: Погода
LESSON_13 = Lesson(
    id="weather",
    title="☀️ Погода",
    description="Говорим о погоде",
    level=1,
    words=[
        Word("w121", "Sun", "Солнце", "/sʌn/", "The sun is shining.", "Солнце светит.", "weather", 1),
        Word("w122", "Rain", "Дождь", "/reɪn/", "It's going to rain.", "Собирается дождь.", "weather", 1),
        Word("w123", "Snow", "Снег", "/snoʊ/", "Children love snow.", "Дети любят снег.", "weather", 1),
        Word("w124", "Cold", "Холодный", "/koʊld/", "It's cold outside.", "На улице холодно.", "weather", 1),
        Word("w125", "Hot", "Горячий/жаркий", "/hɑːt/", "It's hot today.", "Сегодня жарко.", "weather", 1),
        Word("w126", "Wind", "Ветер", "/wɪnd/", "The wind is strong.", "Ветер сильный.", "weather", 1),
        Word("w127", "Cloud", "Облако", "/klaʊd/", "There are many clouds.", "Много облаков.", "weather", 1),
        Word("w128", "Spring", "Весна", "/sprɪŋ/", "Spring is my favorite season.", "Весна — моё любимое время года.", "seasons", 1),
        Word("w129", "Summer", "Лето", "/ˈsʌmər/", "I love summer.", "Я люблю лето.", "seasons", 1),
        Word("w130", "Winter", "Зима", "/ˈwɪntər/", "Winter is cold.", "Зима холодная.", "seasons", 1),
    ]
)

# УРОК 14: Животные
LESSON_14 = Lesson(
    id="animals",
    title="🐾 Животные",
    description="Наши друзья — животные",
    level=1,
    words=[
        Word("w131", "Dog", "Собака", "/dɔːɡ/", "My dog is friendly.", "Моя собака дружелюбная.", "animals", 1),
        Word("w132", "Cat", "Кошка", "/kæt/", "The cat is sleeping.", "Кошка спит.", "animals", 1),
        Word("w133", "Bird", "Птица", "/bɜːrd/", "The bird can fly.", "Птица умеет летать.", "animals", 1),
        Word("w134", "Fish", "Рыба", "/fɪʃ/", "Fish live in water.", "Рыбы живут в воде.", "animals", 1),
        Word("w135", "Horse", "Лошадь", "/hɔːrs/", "The horse is fast.", "Лошадь быстрая.", "animals", 1),
        Word("w136", "Cow", "Корова", "/kaʊ/", "The cow gives milk.", "Корова даёт молоко.", "animals", 1),
        Word("w137", "Chicken", "Курица", "/ˈtʃɪkɪn/", "We have chickens.", "У нас есть куры.", "animals", 1),
        Word("w138", "Lion", "Лев", "/ˈlaɪən/", "The lion is strong.", "Лев сильный.", "animals", 1),
        Word("w139", "Elephant", "Слон", "/ˈelɪfənt/", "Elephants are big.", "Слоны большие.", "animals", 1),
        Word("w140", "Bear", "Медведь", "/ber/", "The bear is in the forest.", "Медведь в лесу.", "animals", 1),
    ]
)

# УРОК 15: Мой день
LESSON_15 = Lesson(
    id="daily-routine",
    title="🌅 Мой день",
    description="Повседневная рутина",
    level=1,
    words=[
        Word("w141", "Wake up", "Просыпаться", "/weɪk ʌp/", "I wake up at 7.", "Я просыпаюсь в 7.", "routine", 1),
        Word("w142", "Get up", "Вставать", "/ɡet ʌp/", "I get up early.", "Я встаю рано.", "routine", 1),
        Word("w143", "Brush teeth", "Чистить зубы", "/brʌʃ tiːθ/", "I brush my teeth twice a day.", "Я чищу зубы дважды в день.", "routine", 1),
        Word("w144", "Take a shower", "Принимать душ", "/teɪk ə ˈʃaʊər/", "I take a shower every morning.", "Я принимаю душ каждое утро.", "routine", 1),
        Word("w145", "Go to work", "Идти на работу", "/ɡoʊ tuː wɜːrk/", "I go to work by bus.", "Я еду на работу на автобусе.", "routine", 1),
        Word("w146", "Come home", "Приходить домой", "/kʌm hoʊm/", "I come home at 6.", "Я прихожу домой в 6.", "routine", 1),
        Word("w147", "Cook dinner", "Готовить ужин", "/kʊk ˈdɪnər/", "I cook dinner for my family.", "Я готовлю ужин для семьи.", "routine", 1),
        Word("w148", "Watch TV", "Смотреть ТВ", "/wɑːtʃ tiːˈviː/", "We watch TV in the evening.", "Мы смотрим ТВ вечером.", "routine", 1),
        Word("w149", "Read a book", "Читать книгу", "/riːd ə bʊk/", "I read a book before bed.", "Я читаю книгу перед сном.", "routine", 1),
        Word("w150", "Go to sleep", "Ложиться спать", "/ɡoʊ tuː sliːp/", "I go to sleep at 11.", "Я ложусь спать в 11.", "routine", 1),
    ]
)

# УРОК 16: В городе
LESSON_16 = Lesson(
    id="city",
    title="🏙️ В городе",
    description="Места в городе",
    level=2,
    words=[
        Word("w151", "Street", "Улица", "/striːt/", "I live on this street.", "Я живу на этой улице.", "city", 2),
        Word("w152", "Shop", "Магазин", "/ʃɑːp/", "The shop is open.", "Магазин открыт.", "city", 2),
        Word("w153", "Bank", "Банк", "/bæŋk/", "The bank is near here.", "Банк рядом.", "city", 2),
        Word("w154", "Hospital", "Больница", "/ˈhɑːspɪtl/", "The hospital is big.", "Больница большая.", "city", 2),
        Word("w155", "School", "Школа", "/skuːl/", "Children go to school.", "Дети ходят в школу.", "city", 2),
        Word("w156", "Park", "Парк", "/pɑːrk/", "Let's walk in the park.", "Давай погуляем в парке.", "city", 2),
        Word("w157", "Library", "Библиотека", "/ˈlaɪbreri/", "I read at the library.", "Я читаю в библиотеке.", "city", 2),
        Word("w158", "Market", "Рынок", "/ˈmɑːrkɪt/", "We buy fruit at the market.", "Мы покупаем фрукты на рынке.", "city", 2),
        Word("w159", "Station", "Станция", "/ˈsteɪʃn/", "The station is far.", "Станция далеко.", "city", 2),
        Word("w160", "Bridge", "Мост", "/brɪdʒ/", "The bridge is old.", "Мост старый.", "city", 2),
    ]
)


# ============================================================
# A2 — ELEMENTARY (Уроки 17-26)
# ============================================================

# УРОК 17: Транспорт
LESSON_17 = Lesson(
    id="transport",
    title="🚌 Транспорт",
    description="Как мы передвигаемся",
    level=2,
    words=[
        Word("w161", "Car", "Машина", "/kɑːr/", "I drive a car.", "Я вожу машину.", "transport", 2),
        Word("w162", "Bicycle", "Велосипед", "/ˈbaɪsɪkl/", "I ride a bicycle.", "Я катаюсь на велосипеде.", "transport", 2),
        Word("w163", "Subway", "Метро", "/ˈsʌbweɪ/", "I take the subway.", "Я еду на метро.", "transport", 2),
        Word("w164", "Airplane", "Самолёт", "/ˈerpleɪn/", "The airplane is fast.", "Самолёт быстрый.", "transport", 2),
        Word("w165", "Ship", "Корабль", "/ʃɪp/", "The ship is big.", "Корабль большой.", "transport", 2),
        Word("w166", "Driver", "Водитель", "/ˈdraɪvər/", "The driver is polite.", "Водитель вежливый.", "transport", 2),
        Word("w167", "Passenger", "Пассажир", "/ˈpæsɪndʒər/", "There are many passengers.", "Много пассажиров.", "transport", 2),
        Word("w168", "Ticket", "Билет", "/ˈtɪkɪt/", "Buy a ticket.", "Купи билет.", "transport", 2),
        Word("w169", "Road", "Дорога", "/roʊd/", "The road is long.", "Дорога длинная.", "transport", 2),
        Word("w170", "Traffic", "Движение", "/ˈtræfɪk/", "There is heavy traffic.", "Плотное движение.", "transport", 2),
    ]
)

# УРОК 18: Покупки
LESSON_18 = Lesson(
    id="shopping",
    title="🛍️ Покупки",
    description="Ходим по магазинам",
    level=2,
    words=[
        Word("w171", "Buy", "Покупать", "/baɪ/", "I want to buy a gift.", "Я хочу купить подарок.", "shopping", 2),
        Word("w172", "Sell", "Продавать", "/sel/", "They sell fresh fruit.", "Они продают свежие фрукты.", "shopping", 2),
        Word("w173", "Price", "Цена", "/praɪs/", "What is the price?", "Какая цена?", "shopping", 2),
        Word("w174", "Cheap", "Дешёвый", "/tʃiːp/", "This shirt is cheap.", "Эта рубашка дешёвая.", "shopping", 2),
        Word("w175", "Expensive", "Дорогой", "/ɪkˈspensɪv/", "The watch is expensive.", "Часы дорогие.", "shopping", 2),
        Word("w176", "Money", "Деньги", "/ˈmʌni/", "I don't have money.", "У меня нет денег.", "shopping", 2),
        Word("w177", "Cash", "Наличные", "/kæʃ/", "Do you pay in cash?", "Вы платите наличными?", "shopping", 2),
        Word("w178", "Card", "Карта", "/kɑːrd/", "I pay by card.", "Я плачу картой.", "shopping", 2),
        Word("w179", "Size", "Размер", "/saɪz/", "What size do you need?", "Какой размер вам нужен?", "shopping", 2),
        Word("w180", "Receipt", "Чек", "/rɪˈsiːt/", "Keep the receipt.", "Сохраните чек.", "shopping", 2),
    ]
)

# УРОК 19: В ресторане
LESSON_19 = Lesson(
    id="restaurant",
    title="🍽️ В ресторане",
    description="Заказываем еду",
    level=2,
    words=[
        Word("w181", "Menu", "Меню", "/ˈmenjuː/", "Can I see the menu?", "Можно меню?", "restaurant", 2),
        Word("w182", "Order", "Заказывать", "/ˈɔːrdər/", "I'd like to order.", "Я бы хотел заказать.", "restaurant", 2),
        Word("w183", "Waiter", "Официант", "/ˈweɪtər/", "The waiter is friendly.", "Официант дружелюбный.", "restaurant", 2),
        Word("w184", "Bill", "Счёт", "/bɪl/", "Can I have the bill?", "Можно счёт?", "restaurant", 2),
        Word("w185", "Tip", "Чаевые", "/tɪp/", "Leave a tip.", "Оставь чаевые.", "restaurant", 2),
        Word("w186", "Delicious", "Вкусный", "/dɪˈlɪʃəs/", "The food is delicious.", "Еда вкусная.", "restaurant", 2),
        Word("w187", "Hungry", "Голодный", "/ˈhʌŋɡri/", "I am hungry.", "Я голодный.", "restaurant", 2),
        Word("w188", "Thirsty", "Жаждущий", "/ˈθɜːrsti/", "I am thirsty.", "Я хочу пить.", "restaurant", 2),
        Word("w189", "Table", "Столик", "/ˈteɪbl/", "A table for two, please.", "Столик на двоих, пожалуйста.", "restaurant", 2),
        Word("w190", "Reservation", "Бронь", "/ˌrezərˈveɪʃn/", "I have a reservation.", "У меня есть бронь.", "restaurant", 2),
    ]
)

# УРОК 20: Путешествия
LESSON_20 = Lesson(
    id="travel",
    title="✈️ Путешествия",
    description="Слова для поездки",
    level=2,
    words=[
        Word("w191", "Luggage", "Багаж", "/ˈlʌɡɪdʒ/", "My luggage is heavy.", "Мой багаж тяжёлый.", "travel", 2),
        Word("w192", "Suitcase", "Чемодан", "/ˈsuːtkeɪs/", "Pack your suitcase.", "Собери чемодан.", "travel", 2),
        Word("w193", "Flight", "Рейс", "/flaɪt/", "The flight is delayed.", "Рейс задерживается.", "travel", 2),
        Word("w194", "Border", "Граница", "/ˈbɔːrdər/", "We crossed the border.", "Мы пересекли границу.", "travel", 2),
        Word("w195", "Tourist", "Турист", "/ˈtʊrɪst/", "I am a tourist.", "Я турист.", "travel", 2),
        Word("w196", "Guide", "Гид", "/ɡaɪd/", "The guide knows everything.", "Гид всё знает.", "travel", 2),
        Word("w197", "Beach", "Пляж", "/biːtʃ/", "Let's go to the beach.", "Пойдём на пляж.", "travel", 2),
        Word("w198", "Mountain", "Гора", "/ˈmaʊntən/", "The mountain is high.", "Гора высокая.", "travel", 2),
        Word("w199", "Country", "Страна", "/ˈkʌntri/", "I want to visit Japan.", "Я хочу посетить Японию.", "travel", 2),
        Word("w200", "Abroad", "За границей", "/əˈbrɔːd/", "I work abroad.", "Я работаю за границей.", "travel", 2),
    ]
)

# УРОК 21: Работа
LESSON_21 = Lesson(
    id="work",
    title="💼 Работа",
    description="Профессии и офис",
    level=2,
    words=[
        Word("w201", "Job", "Работа", "/dʒɑːb/", "I have a new job.", "У меня новая работа.", "work", 2),
        Word("w202", "Boss", "Начальник", "/bɔːs/", "My boss is strict.", "Мой начальник строгий.", "work", 2),
        Word("w203", "Colleague", "Коллега", "/ˈkɑːliːɡ/", "My colleague is nice.", "Мой коллега приятный.", "work", 2),
        Word("w204", "Office", "Офис", "/ˈɔːfɪs/", "I work in an office.", "Я работаю в офисе.", "work", 2),
        Word("w205", "Meeting", "Встреча", "/ˈmiːtɪŋ/", "We have a meeting at 3.", "У нас встреча в 3.", "work", 2),
        Word("w206", "Salary", "Зарплата", "/ˈsæləri/", "The salary is good.", "Зарплата хорошая.", "work", 2),
        Word("w207", "Manager", "Менеджер", "/ˈmænɪdʒər/", "She is a manager.", "Она менеджер.", "work", 2),
        Word("w208", "Doctor", "Врач", "/ˈdɑːktər/", "The doctor helps people.", "Врач помогает людям.", "professions", 2),
        Word("w209", "Teacher", "Учитель", "/ˈtiːtʃər/", "My teacher is kind.", "Мой учитель добрый.", "professions", 2),
        Word("w210", "Engineer", "Инженер", "/ˌendʒɪˈnɪr/", "He is an engineer.", "Он инженер.", "professions", 2),
    ]
)

# УРОК 22: Хобби
LESSON_22 = Lesson(
    id="hobbies",
    title="🎨 Хобби",
    description="Чем мы увлекаемся",
    level=2,
    words=[
        Word("w211", "Hobby", "Хобби", "/ˈhɑːbi/", "My hobby is painting.", "Моё хобби — рисование.", "hobbies", 2),
        Word("w212", "Music", "Музыка", "/ˈmjuːzɪk/", "I love music.", "Я люблю музыку.", "hobbies", 2),
        Word("w213", "Sport", "Спорт", "/spɔːrt/", "I play sport every day.", "Я занимаюсь спортом каждый день.", "hobbies", 2),
        Word("w214", "Game", "Игра", "/ɡeɪm/", "Let's play a game.", "Давай поиграем.", "hobbies", 2),
        Word("w215", "Movie", "Фильм", "/ˈmuːvi/", "I watch movies on weekends.", "Я смотрю фильмы по выходным.", "hobbies", 2),
        Word("w216", "Photo", "Фото", "/ˈfoʊtoʊ/", "I take photos.", "Я делаю фото.", "hobbies", 2),
        Word("w217", "Dance", "Танцевать", "/dæns/", "She likes to dance.", "Она любит танцевать.", "hobbies", 2),
        Word("w218", "Sing", "Петь", "/sɪŋ/", "I sing in the shower.", "Я пою в душе.", "hobbies", 2),
        Word("w219", "Draw", "Рисовать", "/drɔː/", "I draw pictures.", "Я рисую картинки.", "hobbies", 2),
        Word("w220", "Travel", "Путешествовать", "/ˈtrævl/", "I love to travel.", "Я люблю путешествовать.", "hobbies", 2),
    ]
)

# УРОК 23: Телефон и общение
LESSON_23 = Lesson(
    id="phone",
    title="📱 Телефон",
    description="Говорим по телефону",
    level=2,
    words=[
        Word("w221", "Call", "Звонить", "/kɔːl/", "I'll call you later.", "Я перезвоню позже.", "phone", 2),
        Word("w222", "Message", "Сообщение", "/ˈmesɪdʒ/", "Send me a message.", "Пришли мне сообщение.", "phone", 2),
        Word("w223", "Answer", "Отвечать", "/ˈænsər/", "Answer the phone.", "Ответь на телефон.", "phone", 2),
        Word("w224", "Ring", "Звонить (звонок)", "/rɪŋ/", "My phone is ringing.", "Мой телефон звонит.", "phone", 2),
        Word("w225", "Speak", "Говорить", "/spiːk/", "Can I speak to Anna?", "Можно Анну?", "phone", 2),
        Word("w226", "Listen", "Слушать", "/ˈlɪsn/", "Listen to me.", "Послушай меня.", "communication", 2),
        Word("w227", "Talk", "Разговаривать", "/tɔːk/", "Let's talk about it.", "Давай поговорим об этом.", "communication", 2),
        Word("w228", "Ask", "Спрашивать", "/æsk/", "Can I ask a question?", "Можно задать вопрос?", "communication", 2),
        Word("w229", "Tell", "Рассказывать", "/tel/", "Tell me about yourself.", "Расскажи о себе.", "communication", 2),
        Word("w230", "Write", "Писать", "/raɪt/", "Write me an email.", "Напиши мне email.", "communication", 2),
    ]
)

# УРОК 24: Здоровье
LESSON_24 = Lesson(
    id="health",
    title="🏥 Здоровье",
    description="У врача",
    level=2,
    words=[
        Word("w231", "Sick", "Больной", "/sɪk/", "I feel sick.", "Мне плохо.", "health", 2),
        Word("w232", "Pain", "Боль", "/peɪn/", "I have pain in my back.", "У меня болит спина.", "health", 2),
        Word("w233", "Medicine", "Лекарство", "/ˈmedɪsn/", "Take this medicine.", "Прими это лекарство.", "health", 2),
        Word("w234", "Temperature", "Температура", "/ˈtemprətʃər/", "I have a temperature.", "У меня температура.", "health", 2),
        Word("w235", "Cough", "Кашель", "/kɔːf/", "I have a bad cough.", "У меня сильный кашель.", "health", 2),
        Word("w236", "Headache", "Головная боль", "/ˈhedeɪk/", "I have a headache.", "У меня головная боль.", "health", 2),
        Word("w237", "Tired", "Уставший", "/ˈtaɪərd/", "I am tired.", "Я устал.", "health", 2),
        Word("w238", "Better", "Лучше", "/ˈbetər/", "I feel better now.", "Мне сейчас лучше.", "health", 2),
        Word("w239", "Rest", "Отдыхать", "/rest/", "You need to rest.", "Тебе нужно отдохнуть.", "health", 2),
        Word("w240", "Exercise", "Упражнение", "/ˈeksərsaɪz/", "Exercise is good for health.", "Упражнения полезны для здоровья.", "health", 2),
    ]
)

# УРОК 25: Праздники
LESSON_25 = Lesson(
    id="holidays",
    title="🎉 Праздники",
    description="Поздравления и праздники",
    level=2,
    words=[
        Word("w241", "Birthday", "День рождения", "/ˈbɜːrθdeɪ/", "Happy birthday!", "С днём рождения!", "holidays", 2),
        Word("w242", "Gift", "Подарок", "/ɡɪft/", "This is a gift for you.", "Это подарок для тебя.", "holidays", 2),
        Word("w243", "Party", "Вечеринка", "/ˈpɑːrti/", "We have a party tonight.", "Сегодня у нас вечеринка.", "holidays", 2),
        Word("w244", "Holiday", "Праздник/каникулы", "/ˈhɑːlədeɪ/", "Happy holidays!", "С праздниками!", "holidays", 2),
        Word("w245", "New Year", "Новый год", "/nuː jɪr/", "Happy New Year!", "С Новым годом!", "holidays", 2),
        Word("w246", "Christmas", "Рождество", "/ˈkrɪsməs/", "Merry Christmas!", "С Рождеством!", "holidays", 2),
        Word("w247", "Wedding", "Свадьба", "/ˈwedɪŋ/", "The wedding is beautiful.", "Свадьба красивая.", "holidays", 2),
        Word("w248", "Congratulations", "Поздравления", "/kənˌɡrætʃuˈleɪʃnz/", "Congratulations on your success!", "Поздравляю с успехом!", "holidays", 2),
        Word("w249", "Celebrate", "Праздновать", "/ˈselɪbreɪt/", "Let's celebrate!", "Давай отпразднуем!", "holidays", 2),
        Word("w250", "Invite", "Приглашать", "/ɪnˈvaɪt/", "I invite you to my party.", "Я приглашаю тебя на вечеринку.", "holidays", 2),
    ]
)

# УРОК 26: Направления
LESSON_26 = Lesson(
    id="directions",
    title="🧭 Направления",
    description="Как пройти?",
    level=2,
    words=[
        Word("w251", "Left", "Налево", "/left/", "Turn left.", "Поверни налево.", "directions", 2),
        Word("w252", "Right", "Направо", "/raɪt/", "Turn right.", "Поверни направо.", "directions", 2),
        Word("w253", "Straight", "Прямо", "/streɪt/", "Go straight.", "Иди прямо.", "directions", 2),
        Word("w254", "Near", "Рядом", "/nɪr/", "The shop is near.", "Магазин рядом.", "directions", 2),
        Word("w255", "Far", "Далеко", "/fɑːr/", "Is it far from here?", "Это далеко отсюда?", "directions", 2),
        Word("w256", "Between", "Между", "/bɪˈtwiːn/", "It's between the shops.", "Это между магазинами.", "directions", 2),
        Word("w257", "Behind", "За/позади", "/bɪˈhaɪnd/", "The car is behind the house.", "Машина за домом.", "directions", 2),
        Word("w258", "Next to", "Рядом с", "/nekst tuː/", "The bank is next to the cafe.", "Банк рядом с кафе.", "directions", 2),
        Word("w259", "Across", "Напротив", "/əˈkrɔːs/", "The park is across the street.", "Парк напротив улицы.", "directions", 2),
        Word("w260", "Lost", "Потерянный", "/lɔːst/", "I am lost.", "Я потерялся.", "directions", 2),
    ]
)


# Список всех уроков A1-A2
ALL_LESSONS_A1_A2 = [
    LESSON_7, LESSON_8, LESSON_9, LESSON_10, LESSON_11,
    LESSON_12, LESSON_13, LESSON_14, LESSON_15, LESSON_16,
    LESSON_17, LESSON_18, LESSON_19, LESSON_20, LESSON_21,
    LESSON_22, LESSON_23, LESSON_24, LESSON_25, LESSON_26,
]
