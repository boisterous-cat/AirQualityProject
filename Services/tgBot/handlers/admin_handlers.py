from aiogram.types import Message
from Services.tgBot.filters.is_admin import IsAdmin, admin_id
from Services.tgBot.lexicon.lexicon_ru import MENU_COMMANDS_RU
from aiogram import Router
from aiogram.filters import Command

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /stat
@router.message((IsAdmin(admin_id)), Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.reply(text=MENU_COMMANDS_RU['/stat'])
