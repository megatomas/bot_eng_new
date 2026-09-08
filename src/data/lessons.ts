export interface Word {
  id: string;
  english: string;
  russian: string;
  transcription: string;
  example: string;
  exampleTranslation: string;
  category: string;
  level: number;
}

export interface Lesson {
  id: string;
  title: string;
  description: string;
  level: number;
  words: Word[];
  type: 'vocabulary' | 'phrases' | 'grammar' | 'listening' | 'speaking';
}

export const lessons: Lesson[] = [
  {
    id: 'basics-1',
    title: '🔤 Базовые слова',
    description: 'Самые важные слова для начала',
    level: 1,
    type: 'vocabulary',
    words: [
      { id: 'w1', english: 'Hello', russian: 'Привет', transcription: '/həˈloʊ/', example: 'Hello, how are you?', exampleTranslation: 'Привет, как дела?', category: 'greetings', level: 1 },
      { id: 'w2', english: 'Goodbye', russian: 'До свидания', transcription: '/ɡʊdˈbaɪ/', example: 'Goodbye, see you tomorrow!', exampleTranslation: 'До свидания, увидимся завтра!', category: 'greetings', level: 1 },
      { id: 'w3', english: 'Thank you', russian: 'Спасибо', transcription: '/θæŋk juː/', example: 'Thank you very much!', exampleTranslation: 'Большое спасибо!', category: 'greetings', level: 1 },
      { id: 'w4', english: 'Please', russian: 'Пожалуйста', transcription: '/pliːz/', example: 'Please help me.', exampleTranslation: 'Пожалуйста, помоги мне.', category: 'greetings', level: 1 },
      { id: 'w5', english: 'Yes', russian: 'Да', transcription: '/jes/', example: 'Yes, I agree.', exampleTranslation: 'Да, я согласен.', category: 'basics', level: 1 },
      { id: 'w6', english: 'No', russian: 'Нет', transcription: '/noʊ/', example: 'No, thank you.', exampleTranslation: 'Нет, спасибо.', category: 'basics', level: 1 },
      { id: 'w7', english: 'Water', russian: 'Вода', transcription: '/ˈwɔːtər/', example: 'Can I have some water?', exampleTranslation: 'Можно мне воды?', category: 'food', level: 1 },
      { id: 'w8', english: 'Food', russian: 'Еда', transcription: '/fuːd/', example: 'The food is delicious.', exampleTranslation: 'Еда вкусная.', category: 'food', level: 1 },
      { id: 'w9', english: 'Home', russian: 'Дом', transcription: '/hoʊm/', example: 'I want to go home.', exampleTranslation: 'Я хочу пойти домой.', category: 'places', level: 1 },
      { id: 'w10', english: 'Work', russian: 'Работа', transcription: '/wɜːrk/', example: 'I go to work every day.', exampleTranslation: 'Я хожу на работу каждый день.', category: 'places', level: 1 },
    ]
  },
  {
    id: 'basics-2',
    title: '👤 О себе',
    description: 'Расскажи о себе',
    level: 1,
    type: 'vocabulary',
    words: [
      { id: 'w11', english: 'I am', russian: 'Я есть', transcription: '/aɪ æm/', example: 'I am a student.', exampleTranslation: 'Я студент.', category: 'pronouns', level: 1 },
      { id: 'w12', english: 'My name is', russian: 'Меня зовут', transcription: '/maɪ neɪm ɪz/', example: 'My name is John.', exampleTranslation: 'Меня зовут Джон.', category: 'pronouns', level: 1 },
      { id: 'w13', english: 'I like', russian: 'Мне нравится', transcription: '/aɪ laɪk/', example: 'I like music.', exampleTranslation: 'Мне нравится музыка.', category: 'verbs', level: 1 },
      { id: 'w14', english: 'I want', russian: 'Я хочу', transcription: '/aɪ wɑːnt/', example: 'I want to learn English.', exampleTranslation: 'Я хочу учить английский.', category: 'verbs', level: 1 },
      { id: 'w15', english: 'I have', russian: 'У меня есть', transcription: '/aɪ hæv/', example: 'I have a cat.', exampleTranslation: 'У меня есть кошка.', category: 'verbs', level: 1 },
      { id: 'w16', english: 'I can', russian: 'Я могу', transcription: '/aɪ kæn/', example: 'I can speak English.', exampleTranslation: 'Я могу говорить по-английски.', category: 'verbs', level: 1 },
      { id: 'w17', english: 'Friend', russian: 'Друг', transcription: '/frend/', example: 'He is my best friend.', exampleTranslation: 'Он мой лучший друг.', category: 'people', level: 1 },
      { id: 'w18', english: 'Family', russian: 'Семья', transcription: '/ˈfæmɪli/', example: 'I love my family.', exampleTranslation: 'Я люблю свою семью.', category: 'people', level: 1 },
      { id: 'w19', english: 'Happy', russian: 'Счастливый', transcription: '/ˈhæpi/', example: 'I am very happy today.', exampleTranslation: 'Я очень счастлив сегодня.', category: 'emotions', level: 1 },
      { id: 'w20', english: 'Good', russian: 'Хороший', transcription: '/ɡʊd/', example: 'This is a good idea.', exampleTranslation: 'Это хорошая идея.', category: 'adjectives', level: 1 },
    ]
  },
  {
    id: 'daily-1',
    title: '🏠 Повседневная жизнь',
    description: 'Слова для ежедневного общения',
    level: 2,
    type: 'vocabulary',
    words: [
      { id: 'w21', english: 'Morning', russian: 'Утро', transcription: '/ˈmɔːrnɪŋ/', example: 'Good morning!', exampleTranslation: 'Доброе утро!', category: 'time', level: 2 },
      { id: 'w22', english: 'Evening', russian: 'Вечер', transcription: '/ˈiːvnɪŋ/', example: 'Good evening, everyone.', exampleTranslation: 'Добрый вечер, все.', category: 'time', level: 2 },
      { id: 'w23', english: 'Today', russian: 'Сегодня', transcription: '/təˈdeɪ/', example: 'Today is a beautiful day.', exampleTranslation: 'Сегодня прекрасный день.', category: 'time', level: 2 },
      { id: 'w24', english: 'Tomorrow', russian: 'Завтра', transcription: '/təˈmɑːroʊ/', example: 'See you tomorrow.', exampleTranslation: 'Увидимся завтра.', category: 'time', level: 2 },
      { id: 'w25', english: 'Yesterday', russian: 'Вчера', transcription: '/ˈjestərdeɪ/', example: 'I was busy yesterday.', exampleTranslation: 'Я был занят вчера.', category: 'time', level: 2 },
      { id: 'w26', english: 'Always', russian: 'Всегда', transcription: '/ˈɔːlweɪz/', example: 'I always drink coffee.', exampleTranslation: 'Я всегда пью кофе.', category: 'frequency', level: 2 },
      { id: 'w27', english: 'Never', russian: 'Никогда', transcription: '/ˈnevər/', example: 'I never give up.', exampleTranslation: 'Я никогда не сдаюсь.', category: 'frequency', level: 2 },
      { id: 'w28', english: 'Sometimes', russian: 'Иногда', transcription: '/ˈsʌmtaɪmz/', example: 'Sometimes I read books.', exampleTranslation: 'Иногда я читаю книги.', category: 'frequency', level: 2 },
      { id: 'w29', english: 'Quickly', russian: 'Быстро', transcription: '/ˈkwɪkli/', example: 'He runs quickly.', exampleTranslation: 'Он бегает быстро.', category: 'adverbs', level: 2 },
      { id: 'w30', english: 'Slowly', russian: 'Медленно', transcription: '/ˈsloʊli/', example: 'Please speak slowly.', exampleTranslation: 'Пожалуйста, говорите медленно.', category: 'adverbs', level: 2 },
    ]
  },
  {
    id: 'travel-1',
    title: '✈️ Путешествия',
    description: 'Слова для путешествий',
    level: 2,
    type: 'vocabulary',
    words: [
      { id: 'w31', english: 'Airport', russian: 'Аэропорт', transcription: '/ˈerpɔːrt/', example: 'The airport is far from here.', exampleTranslation: 'Аэропорт далеко отсюда.', category: 'travel', level: 2 },
      { id: 'w32', english: 'Hotel', russian: 'Отель', transcription: '/hoʊˈtel/', example: 'The hotel is very nice.', exampleTranslation: 'Отель очень хороший.', category: 'travel', level: 2 },
      { id: 'w33', english: 'Ticket', russian: 'Билет', transcription: '/ˈtɪkɪt/', example: 'I need a ticket.', exampleTranslation: 'Мне нужен билет.', category: 'travel', level: 2 },
      { id: 'w34', english: 'Passport', russian: 'Паспорт', transcription: '/ˈpæspɔːrt/', example: 'Where is my passport?', exampleTranslation: 'Где мой паспорт?', category: 'travel', level: 2 },
      { id: 'w35', english: 'Map', russian: 'Карта', transcription: '/mæp/', example: 'Do you have a map?', exampleTranslation: 'У вас есть карта?', category: 'travel', level: 2 },
      { id: 'w36', english: 'Train', russian: 'Поезд', transcription: '/treɪn/', example: 'The train arrives at 5.', exampleTranslation: 'Поезд прибывает в 5.', category: 'transport', level: 2 },
      { id: 'w37', english: 'Bus', russian: 'Автобус', transcription: '/bʌs/', example: 'Take the bus to the center.', exampleTranslation: 'Сядь на автобус до центра.', category: 'transport', level: 2 },
      { id: 'w38', english: 'Taxi', russian: 'Такси', transcription: '/ˈtæksi/', example: 'Call me a taxi, please.', exampleTranslation: 'Вызовите мне такси, пожалуйста.', category: 'transport', level: 2 },
      { id: 'w39', english: 'Restaurant', russian: 'Ресторан', transcription: '/ˈrestərɑːnt/', example: 'Let\'s go to a restaurant.', exampleTranslation: 'Давай пойдём в ресторан.', category: 'places', level: 2 },
      { id: 'w40', english: 'Museum', russian: 'Музей', transcription: '/mjuːˈziːəm/', example: 'The museum is closed today.', exampleTranslation: 'Музей закрыт сегодня.', category: 'places', level: 2 },
    ]
  },
  {
    id: 'phrases-1',
    title: '💬 Полезные фразы',
    description: 'Фразы для общения',
    level: 2,
    type: 'phrases',
    words: [
      { id: 'w41', english: 'How are you?', russian: 'Как дела?', transcription: '/haʊ ɑːr juː/', example: 'Hi! How are you doing?', exampleTranslation: 'Привет! Как у тебя дела?', category: 'greetings', level: 2 },
      { id: 'w42', english: 'Nice to meet you', russian: 'Приятно познакомиться', transcription: '/naɪs tuː miːt juː/', example: 'Nice to meet you, I\'m Anna.', exampleTranslation: 'Приятно познакомиться, я Анна.', category: 'greetings', level: 2 },
      { id: 'w43', english: 'I don\'t understand', russian: 'Я не понимаю', transcription: '/aɪ doʊnt ˌʌndərˈstænd/', example: 'Sorry, I don\'t understand.', exampleTranslation: 'Извините, я не понимаю.', category: 'communication', level: 2 },
      { id: 'w44', english: 'Can you help me?', russian: 'Можете помочь?', transcription: '/kæn juː help miː/', example: 'Can you help me, please?', exampleTranslation: 'Можете мне помочь, пожалуйста?', category: 'communication', level: 2 },
      { id: 'w45', english: 'Where is...?', russian: 'Где...?', transcription: '/wer ɪz/', example: 'Where is the bathroom?', exampleTranslation: 'Где туалет?', category: 'questions', level: 2 },
      { id: 'w46', english: 'How much?', russian: 'Сколько стоит?', transcription: '/haʊ mʌtʃ/', example: 'How much does it cost?', exampleTranslation: 'Сколько это стоит?', category: 'shopping', level: 2 },
      { id: 'w47', english: 'I\'m sorry', russian: 'Извините', transcription: '/aɪm ˈsɑːri/', example: 'I\'m sorry for being late.', exampleTranslation: 'Извините за опоздание.', category: 'communication', level: 2 },
      { id: 'w48', english: 'Excuse me', russian: 'Простите', transcription: '/ɪkˈskjuːz miː/', example: 'Excuse me, where is the station?', exampleTranslation: 'Простите, где вокзал?', category: 'communication', level: 2 },
      { id: 'w49', english: 'Of course', russian: 'Конечно', transcription: '/əv kɔːrs/', example: 'Of course, I can help!', exampleTranslation: 'Конечно, я могу помочь!', category: 'communication', level: 2 },
      { id: 'w50', english: 'No problem', russian: 'Нет проблем', transcription: '/noʊ ˈprɑːbləm/', example: 'No problem, take your time.', exampleTranslation: 'Нет проблем, не торопись.', category: 'communication', level: 2 },
    ]
  },
  {
    id: 'advanced-1',
    title: '🧠 Продвинутый уровень',
    description: 'Сложные слова и выражения',
    level: 3,
    type: 'vocabulary',
    words: [
      { id: 'w51', english: 'Achievement', russian: 'Достижение', transcription: '/əˈtʃiːvmənt/', example: 'It was a great achievement.', exampleTranslation: 'Это было великое достижение.', category: 'abstract', level: 3 },
      { id: 'w52', english: 'Opportunity', russian: 'Возможность', transcription: '/ˌɑːpərˈtuːnɪti/', example: 'This is a great opportunity.', exampleTranslation: 'Это отличная возможность.', category: 'abstract', level: 3 },
      { id: 'w53', english: 'Experience', russian: 'Опыт', transcription: '/ɪkˈspɪriəns/', example: 'I have a lot of experience.', exampleTranslation: 'У меня много опыта.', category: 'abstract', level: 3 },
      { id: 'w54', english: 'Knowledge', russian: 'Знание', transcription: '/ˈnɑːlɪdʒ/', example: 'Knowledge is power.', exampleTranslation: 'Знание — сила.', category: 'abstract', level: 3 },
      { id: 'w55', english: 'Environment', russian: 'Окружение/среда', transcription: '/ɪnˈvaɪrənmənt/', example: 'We must protect the environment.', exampleTranslation: 'Мы должны защищать окружающую среду.', category: 'nature', level: 3 },
      { id: 'w56', english: 'Development', russian: 'Развитие', transcription: '/dɪˈveləpmənt/', example: 'The development was successful.', exampleTranslation: 'Развитие было успешным.', category: 'abstract', level: 3 },
      { id: 'w57', english: 'Relationship', russian: 'Отношения', transcription: '/rɪˈleɪʃnʃɪp/', example: 'They have a good relationship.', exampleTranslation: 'У них хорошие отношения.', category: 'people', level: 3 },
      { id: 'w58', english: 'Responsibility', russian: 'Ответственность', transcription: '/rɪˌspɑːnsəˈbɪlɪti/', example: 'It\'s your responsibility.', exampleTranslation: 'Это твоя ответственность.', category: 'abstract', level: 3 },
      { id: 'w59', english: 'Communication', russian: 'Общение', transcription: '/kəˌmjuːnɪˈkeɪʃn/', example: 'Communication is very important.', exampleTranslation: 'Общение очень важно.', category: 'abstract', level: 3 },
      { id: 'w60', english: 'Independent', russian: 'Независимый', transcription: '/ˌɪndɪˈpendənt/', example: 'She is very independent.', exampleTranslation: 'Она очень независимая.', category: 'adjectives', level: 3 },
    ]
  }
];

export const grammarRules = [
  {
    id: 'g1',
    title: 'To Be (am/is/are)',
    level: 1,
    explanation: 'Глагол "to be" используется для описания состояния.',
    examples: [
      { english: 'I am a student.', russian: 'Я студент.' },
      { english: 'She is happy.', russian: 'Она счастлива.' },
      { english: 'They are friends.', russian: 'Они друзья.' },
    ]
  },
  {
    id: 'g2',
    title: 'Present Simple',
    level: 1,
    explanation: 'Используется для регулярных действий и фактов.',
    examples: [
      { english: 'I work every day.', russian: 'Я работаю каждый день.' },
      { english: 'He plays football.', russian: 'Он играет в футбол.' },
      { english: 'We live in Moscow.', russian: 'Мы живём в Москве.' },
    ]
  },
  {
    id: 'g3',
    title: 'Present Continuous',
    level: 2,
    explanation: 'Действие происходит прямо сейчас.',
    examples: [
      { english: 'I am reading a book.', russian: 'Я читаю книгу (сейчас).' },
      { english: 'She is cooking dinner.', russian: 'Она готовит ужин.' },
      { english: 'They are playing games.', russian: 'Они играют в игры.' },
    ]
  },
  {
    id: 'g4',
    title: 'Past Simple',
    level: 2,
    explanation: 'Действие произошло в прошлом.',
    examples: [
      { english: 'I worked yesterday.', russian: 'Я работал вчера.' },
      { english: 'She visited her friend.', russian: 'Она навестила друга.' },
      { english: 'We went to the park.', russian: 'Мы ходили в парк.' },
    ]
  }
];
