from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# клавиатура и кнопки верхнего уровня
english_quiz_button = InlineKeyboardButton('Слова на английском', callback_data='english_words')
russian_quiz_button = InlineKeyboardButton('Слова на русском', callback_data='russian_words')
make_up_word_button = InlineKeyboardButton('Составить слово', callback_data='make_up_word')

main_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(english_quiz_button, russian_quiz_button)
main_keyboard.add(make_up_word_button)


# клавиатура да / нет
yes_button = InlineKeyboardButton('А давай :)', callback_data='yes_button')
no_button = InlineKeyboardButton('Не хочу :(', callback_data='no_button')

yes_or_no_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
yes_or_no_keyboard.add(yes_button, no_button)
