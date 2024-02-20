from datetime import datetime
import random
import pytest
from aiogram import Dispatcher
from aiogram.enums import ChatType
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, SendPhoto
from aiogram.methods.base import TelegramType
from aiogram.types import Message, Update, User, Chat
from aiogram.dispatcher.event.bases import UNHANDLED
from Services.tgBot.handlers.user_handlers import FSMFillForm
from Services.tgBot.tests.mocked_aiogram import MockedBot

user_id = 123456


def make_message(text: str) -> Message:
    user = User(id=user_id, first_name="User", is_bot=False)
    chat = Chat(id=user_id, type=ChatType.PRIVATE)
    return Message(message_id=1, from_user=user, chat=chat, date=datetime.now(), text=text)


@pytest.mark.asyncio
async def test_states_flow_orders(dp: Dispatcher, bot: MockedBot):

    # Получаем контекст FSM для текущего юзера
    fsm_context: FSMContext = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=user_id)
    await fsm_context.set_state(default_state)

    # Альтернативный вариант
    # fsm_storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    # # Очистка стейта
    # await dp.storage.set_state(fsm_storage_key, None)

    starting_messages = [
        make_message("/start"),
        make_message("/aqi")
    ]

    for message in starting_messages:
        bot.add_result_for(SendMessage, ok=True)
        await dp.feed_update(bot, Update(message=message, update_id=1))
        # Здесь и далее таким вызовом будем забирать
        # очередное сообщение бота из списка отправленных
        # Но пока что нас содержимое не интересует
        bot.get_request()

    # Проверяем стейт "ввод CO"
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_co

    # Отправляем некорректное значение у нас либо отрицательные числа, либо текст
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message("WTF"), update_id=1))
    bot.get_request()

    # Проверяем, что стейт не изменился
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_co

    # Отправляем корректное значение CO
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message(str(random.randint(1, 200))), update_id=1))
    bot.get_request()

    # Проверяем, что стейт изменился на "ввод NO"
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_no

    # Отправляем некорректное значение
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message("WTF"), update_id=1))
    bot.get_request()

    # Проверяем, что стейт не изменился
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_no

    # Отправляем корректное значение
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message(str(random.randint(1, 200))), update_id=1))

    # Проверяем, что стейт изменился на "ввод OZOne"
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_ozone

    # Отправляем некорректное значение
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message("WTF"), update_id=1))
    bot.get_request()

    # Проверяем, что стейт не изменился
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_ozone

    # Отправляем корректное значение
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message(str(random.randint(1, 200))), update_id=1))

    # Проверяем, что стейт изменился на "ввод PM2"
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_pm2

    # Отправляем некорректное значение
    bot.add_result_for(SendMessage, ok=True)
    await dp.feed_update(bot, Update(message=make_message("WTF"), update_id=1))
    bot.get_request()

    # Проверяем, что стейт не изменился
    current_state = await fsm_context.get_state()
    assert current_state == FSMFillForm.fill_pm2

    # Отправляем корректное значение
    bot.add_result_for(SendMessage, ok=True)
    bot.add_result_for(SendPhoto, ok=True)
    await dp.feed_update(bot, Update(message=make_message(str(random.randint(1, 500))), update_id=1))

    # Получаем отправленное ботом сообщение
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что бот написал правильно
    assert "Спасибо!" in outgoing_message.text

    # Проверяем, что стейт сбросился
    current_state = await fsm_context.get_state()
    assert current_state is None


# Тестируем состояние cancel
@pytest.mark.asyncio
async def test_cancel_command(dp, bot):
    # Подготавливаем нужный стейт
    fsm_context: FSMContext = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=user_id)
    await fsm_context.set_state(FSMFillForm.fill_pm2)
    bot.add_result_for(method=SendMessage, ok=True)

    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
          bot,
          Update(message=make_message("/cancel"), update_id=1)
        )

    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    current_state = await fsm_context.get_state()
    assert current_state is None
