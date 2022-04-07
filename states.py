from aiogram.dispatcher.filters.state import StatesGroup, State


class Actions(StatesGroup):
    english_quiz_question_1 = State()
    english_quiz_question_2 = State()
    english_quiz_question_3 = State()
    english_quiz_question_4 = State()
    english_quiz_question_5 = State()

    make_up_word_state = State()
    make_up_word_state_check = State()

