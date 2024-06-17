import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename = "log.log", filemode='a')
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TOKEN')
# Объект бота
bot = Bot(token=TOKEN)

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logger.info(f'{user_name} {user_id} запустил бота')
    await message.answer(f'Привет, {user_name}! Я создан, чтобы перевести твои ФИО на латиницу.')


# Обработка всех сообщений, проверка на правильность ввода и транслитрация на латиницу
@dp.message()
async def send_message(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    answer_for_user = translit_message(text)
    logger.info(f'{user_name} {user_id}: {text}')
    await message.answer(text=answer_for_user)


# Заменяем все символы, которые не являются буквами латиницы, на пустую строку
import re
def remove_non_letters(text):
    return re.sub(r'[^а-яА-Я]', '', text)

# Проверяем, что все символы являются буквами русского алфавита
def is_russian_letters_only(text):
    return all('А' <= char <= 'я' or char == 'ё' or char == 'Ё' for char in text)

def translit_message(text: str) -> str:
    list_russian_letters = [
    "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", 
    "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", 
    "Х", "Ц", "Ч", "Ш", "Щ", "Ы", "Ъ", "Э", "Ю", "Я"
]
    list_translit_letter = [
    "A", "B", "V", "G", "D", "E", "E", "ZH", "Z", "I", "I", 
    "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "F", 
    "KH", "TS", "CH", "SH", "SHCH", "Y", "IE", "E", "IU", "IA"
]
    list_fio = text.upper().split()
    new_list_fio = []
    for el in list_fio:
        remove_non_letters(el)
        if not is_russian_letters_only(el):
            return "Введите ФИО корректно"
            break
        else:
            for char in el:
                index = list_russian_letters.index(char)
                el = el.replace(char, list_translit_letter[index])
        new_list_fio.append(el)
    return ' '.join(new_list_fio)


# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)

    

