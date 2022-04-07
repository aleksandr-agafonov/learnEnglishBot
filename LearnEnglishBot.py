from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Actions

# импорт клавиатур
from keyboards import main_keyboard, yes_or_no_keyboard

# импорт внутренних функций
from quiz_functions import QuizFunctions

# импорт других иблиотек
import nest_asyncio
import re


#token = '1938283222:AAEe7C80RbtpAjW7BVBzt6qISW8VnzIpg0A'  # токен для теста
token = '5240835692:AAHyCfFYzcfzd7tl7DNivBzPGEw46_fkqcI'  # боевой токен
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
nest_asyncio.apply()  # для добавления задач в ассинхрон


@dp.message_handler(commands=['start'], state='*')
async def greetings(message: types.Message, state: FSMContext):
    await state.reset_state()
    message_text = 'Привет, давай поучим английский? :)'
    await bot.send_message(message.from_user.id, message_text, reply_markup=main_keyboard)


# выбираем квиз на английском
@dp.callback_query_handler(lambda c: c.data == 'english_words')
async def choose_english_quiz(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['guess_word_language'] = 'english'

    message_text = 'Я буду давать тебе слова на английском языке,\n' \
                   'а ты должен выбрать перевод\n' \
                   'Нужно ответить на 5 вопросов'
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=yes_or_no_keyboard)


# выбираем квиз на русском
@dp.callback_query_handler(lambda c: c.data == 'russian_words')
async def choose_russian_quiz(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['guess_word_language'] = 'russian'

    message_text = 'Я буду давать тебе слова на русском языке,\n' \
                   'а ты должен выбрать перевод\n' \
                   'Нужно ответить на 5 вопросов'
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=yes_or_no_keyboard)


# нажали на кнопку "назад"
@dp.callback_query_handler(lambda c: c.data == 'no_button', state='*')
async def get_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state()
    message_text = 'Привет, давай поучим английский? :)'
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=main_keyboard)


# согласились пройти тест
@dp.callback_query_handler(lambda c: c.data == 'yes_button')
async def start_quiz(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    message_text = 'Что ж, давай приступим'
    await bot.send_message(callback_query.from_user.id, message_text)

    # добавляем задачу ассинхронно, передаем выбранный язык и сохраняем ответ
    async with state.proxy() as data:
        result_dict = await QuizFunctions.run_async_functions(data['guess_word_language'])
        data['answer'] = result_dict['quiz_word']
        data['translation'] = result_dict['quiz_options'][result_dict['quiz_word']]
        data['score'] = 0

    quiz_text = f'Выберете верный вариант перевода:\n{data["answer"]}'
    await bot.send_message(callback_query.from_user.id, quiz_text, reply_markup=result_dict['options_keyboard'])
    await Actions.english_quiz_question_1.set()


# обработка первого ответа
@dp.callback_query_handler(lambda c: re.search('.*_answer', c.data), state=Actions.english_quiz_question_1)
async def english_first_question(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        # проверяем правильность ответа
        check_answer = await QuizFunctions.check_answer(callback_query.data,
                                                        data['answer'], data['score'], data['translation'])
        data['score'] = check_answer['score']
        await bot.send_message(callback_query.from_user.id, check_answer['message_text'])

    # сохраняем ответ
    async with state.proxy() as data:
        result_dict = await QuizFunctions.run_async_functions(data['guess_word_language'])
        data['answer'] = result_dict['quiz_word']
        data['translation'] = result_dict['quiz_options'][result_dict['quiz_word']]

    quiz_text = f'Выберете верный вариант перевода:\n{data["answer"]}'
    await bot.send_message(callback_query.from_user.id, quiz_text, reply_markup=result_dict['options_keyboard'])
    await bot.answer_callback_query(callback_query.id)
    await Actions.english_quiz_question_2.set()


# обработка второго ответа
@dp.callback_query_handler(lambda c: re.search('.*_answer', c.data), state=Actions.english_quiz_question_2)
async def english_second_question(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # проверяем правильность ответа
        check_answer = await QuizFunctions.check_answer(callback_query.data,
                                                        data['answer'], data['score'], data['translation'])
        data['score'] = check_answer['score']
    await bot.send_message(callback_query.from_user.id, check_answer['message_text'])

    # сохраняем ответ
    async with state.proxy() as data:
        result_dict = await QuizFunctions.run_async_functions(data['guess_word_language'])
        data['answer'] = result_dict['quiz_word']
        data['translation'] = result_dict['quiz_options'][result_dict['quiz_word']]

    quiz_text = f'Выберете верный вариант перевода:\n{data["answer"]}'
    await bot.send_message(callback_query.from_user.id, quiz_text, reply_markup=result_dict['options_keyboard'])
    await bot.answer_callback_query(callback_query.id)
    await Actions.english_quiz_question_3.set()


# обработка третьего ответа
@dp.callback_query_handler(lambda c: re.search('.*_answer', c.data), state=Actions.english_quiz_question_3)
async def english_third_question(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # проверяем правильность ответа
        check_answer = await QuizFunctions.check_answer(callback_query.data,
                                                        data['answer'], data['score'], data['translation'])
        data['score'] = check_answer['score']
    await bot.send_message(callback_query.from_user.id, check_answer['message_text'])

    # сохраняем ответ
    async with state.proxy() as data:
        result_dict = await QuizFunctions.run_async_functions(data['guess_word_language'])
        data['answer'] = result_dict['quiz_word']
        data['translation'] = result_dict['quiz_options'][result_dict['quiz_word']]

    quiz_text = f'Выберете верный вариант перевода:\n{data["answer"]}'
    await bot.send_message(callback_query.from_user.id, quiz_text, reply_markup=result_dict['options_keyboard'])
    await bot.answer_callback_query(callback_query.id)
    await Actions.english_quiz_question_4.set()


# обработка четвертого ответа
@dp.callback_query_handler(lambda c: re.search('.*_answer', c.data), state=Actions.english_quiz_question_4)
async def english_forth_question(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # проверяем правильность ответа
        check_answer = await QuizFunctions.check_answer(callback_query.data,
                                                        data['answer'], data['score'], data['translation'])
        data['score'] = check_answer['score']
    await bot.send_message(callback_query.from_user.id, check_answer['message_text'])

    # сохраняем ответ
    async with state.proxy() as data:
        result_dict = await QuizFunctions.run_async_functions(data['guess_word_language'])
        data['answer'] = result_dict['quiz_word']
        data['translation'] = result_dict['quiz_options'][result_dict['quiz_word']]

    quiz_text = f'Выберете верный вариант перевода:\n{data["answer"]}'
    await bot.send_message(callback_query.from_user.id, quiz_text, reply_markup=result_dict['options_keyboard'])
    await bot.answer_callback_query(callback_query.id)
    await Actions.english_quiz_question_5.set()


# обработка пятого ответа
@dp.callback_query_handler(lambda c: re.search('.*_answer', c.data), state=Actions.english_quiz_question_5)
async def english_fifth_question(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # проверяем правильность ответа
        check_answer = await QuizFunctions.check_answer(callback_query.data, data['answer'], data['score'], data['translation'])
        data['score'] = check_answer['score']
    await bot.send_message(callback_query.from_user.id, check_answer['message_text'])

    # обнбнуляем состояние
    message_text = f'Поздравляю!\nВаш счет: {data["score"]} из 5'
    await bot.send_message(callback_query.from_user.id, message_text)
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state()

    message_text = 'Поиграем еще?'
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=main_keyboard)


# выбираем составить слово из букв
@dp.callback_query_handler(lambda c: c.data == 'make_up_word')
async def choose_make_up_word(callback_query: types.CallbackQuery, state: FSMContext):
    message_text = 'Я дам тебе набор букв, \n'\
                   'из которых нужно составить слово на английском,\n'\
                   'В качестве подсказки я дам тебе его перевод'
    await bot.answer_callback_query(callback_query.id)
    await Actions.make_up_word_state.set()
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=yes_or_no_keyboard)


# согласились составить слово из букв
@dp.callback_query_handler(lambda c: c.data == 'yes_button', state=Actions.make_up_word_state)
async def start_make_up_word(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    message_text = 'Что ж, давай приступим'
    await bot.send_message(callback_query.from_user.id, message_text)
    result_list = await QuizFunctions.create_make_up_word('russian')

    async with state.proxy() as data:
        data['right answer'] = result_list[1]  # записываем правильный ответ

    message_text = f'Составьте из этих букв слово:\n\n' \
                   f'{result_list[2]}\n\n' \
                   f'Это слово означает "{result_list[0]}"\n' \
                   f'Введите ваш ответ'

    await Actions.make_up_word_state_check.set()
    await bot.send_message(callback_query.from_user.id, message_text)


@dp.message_handler(state=Actions.make_up_word_state_check)
async def make_up_word_check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == data['right answer']:
            message_text = 'Верно!'
        else:
            message_text = 'Не угадали!\n' \
                           f'Правильный ответ: {data["right answer"]}'
    await state.reset_state()
    await bot.send_message(message.from_user.id, message_text, reply_markup=main_keyboard)


executor.start_polling(dp, skip_updates=True)
# сделать ветку с собиранием слов из перемешанных букв
