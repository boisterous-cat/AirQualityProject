from Services.tgBot.lexicon.lexicon_ru import MENU_COMMANDS_RU
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создаем объекты инлайн-кнопок
github_button = InlineKeyboardButton(
    text=MENU_COMMANDS_RU['/project'],
    url="https://github.com/boisterous-cat/AirQualityProject/blob/main/README.md"
)

user_button = InlineKeyboardButton(
    text='Автор',
    url="tg://resolve?domain=boisterous_cat"
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[github_button],
                     [user_button]]
)

# Создаем объекты инлайн-кнопок
top_10 = InlineKeyboardButton(
    text='Топ 10',
    callback_data='top_10_pressed'
)

less_10 = InlineKeyboardButton(
    text='Худшие 10',
    callback_data='less_10_pressed'
)

# Создаем объект инлайн-клавиатуры
df_show_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[top_10],
                     [less_10]]
)
