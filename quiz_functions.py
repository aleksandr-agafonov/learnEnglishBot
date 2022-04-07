from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bd_functions import DbFunctions

import asyncio
import nest_asyncio
import random


class QuizFunctions:
    # создаем клавиатуру с вариантами ответа и возвращаем tuple с клавиатурой и самим словарем
    async def create_question(language):
        english_quiz_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        question_func = await DbFunctions.get_question(language)

        for key, values in question_func.items():
            option_button = InlineKeyboardButton(values, callback_data=key + '_answer')
            english_quiz_keyboard.add(option_button)

        return english_quiz_keyboard, question_func

    # генерирует вопрос и клавиатуру с ответами
    async def run_async_functions(language):  # ассинхронная обработка функции
        nest_asyncio.apply()
        loop = asyncio.get_running_loop()
        run_func = loop.create_task(QuizFunctions.create_question(language))
        loop.run_until_complete(run_func)
        result = run_func.result()

        options_keyboard = result[0]  # клавиатура для теста
        quiz_options = result[1]  # словарь с вариантами ответа
        quiz_word = random.choice(list(quiz_options.keys()))  # загадываемое слово

        result_dict = dict()
        result_dict['options_keyboard'] = options_keyboard
        result_dict['quiz_options'] = quiz_options
        result_dict['quiz_word'] = quiz_word

        return result_dict

    # проверяем ответ пользователя
    async def check_answer(user_answer, right_answer, score, translation):
        result_dict = dict()

        if right_answer == user_answer.replace('_answer', ''):
            score += 1
            message_text = f'Верно!\nВаш счет: {score}'
            result_dict['score'] = score
            result_dict['message_text'] = message_text
        else:
            message_text = f'Неверно!\nПравильный ответ: {translation}\nВаш счет: {score}'
            result_dict['score'] = score
            result_dict['message_text'] = message_text

        return result_dict

    # генерируем вопрос для make up word
    async def create_make_up_word(language):
        question_func = await DbFunctions.get_question(language)
        quiz_list = list(random.choice(list(question_func.items())))
        new_elem = list(quiz_list[1])
        random.shuffle(new_elem)
        new_elem = ' '.join(new_elem)
        quiz_list.append(new_elem)
        return quiz_list


# loop = asyncio.get_event_loop()
# a = loop.run_until_complete(QuizFunctions.create_make_up_word('russian'))
# print(a)
