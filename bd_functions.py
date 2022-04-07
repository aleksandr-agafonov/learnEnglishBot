import aiosqlite


db = 'english_dictionary_db'  # название БД


class DbFunctions:

    # возвращаем словарь с четырьмя парами "слово - перевод"
    async def get_question(language):
        async with aiosqlite.connect(db) as connection:
            result_dict = dict()  # складываем реузльтаты в список
            cursor = await connection.cursor()

            if language == 'english':
                query = f'''
                        SELECT
                            english,
                            russian
                        FROM er_dictionary ed
                        ORDER BY RANDOM()
                        LIMIT 4
                '''
            else:
                query = f'''
                        SELECT
                            russian,
                            english
                        FROM er_dictionary ed
                        ORDER BY RANDOM()
                        LIMIT 4
                '''

            await cursor.execute(query)
            result = await cursor.fetchall()

            for pair in result:
                result_dict[pair[0]] = pair[1]

        return result_dict



# import asyncio
# loop = asyncio.get_event_loop()
# a = loop.run_until_complete(DB_Functions.get_question())
# print(a)
