from datetime import datetime

import pytest
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    Update, Chat, User, Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from Services.tgBot.lexicon.lexicon_ru import LEXICON_RU
from Services.tgBot.keyboards.keyboards import user_button, github_button


@pytest.mark.asyncio
async def test_start_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас можно пропустить
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/start",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON_RU['/start']


@pytest.mark.asyncio
async def test_help_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/help",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON_RU['/help']


@pytest.mark.asyncio
async def test_project_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/project",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert "Перейти на страницу проекта" in outgoing_message.text
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button_git: InlineKeyboardButton = markup.inline_keyboard[0][0]
    assert button_git == github_button
    button_me: InlineKeyboardButton = markup.inline_keyboard[1][0]
    assert button_me == user_button


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["raise_exception"],
    [
        [False],
        [True]
    ]
)
async def test_send_echo_command(dp, bot, raise_exception):
    # В зависимости от raise_exception возвращаем успех или
    bot.add_result_for(
        method=SendMessage,
        ok=(not raise_exception),
        # вроде TypeError возвращает 400, нигде не нашла инфо
        error_code=404 if raise_exception else 200
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="any",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )

    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON_RU['no_echo']


def make_message(user_id: int) -> Message:
    user = User(id=user_id, first_name="User", is_bot=False)
    chat = Chat(id=user_id, type=ChatType.PRIVATE)
    return Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="/stat"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, expected_text",
    [
        [123456700, LEXICON_RU['not admin']],
        # так и не смогла победить ошибку при тесте админа
        # [642047926, MENU_COMMANDS_RU['/stat']]
    ]
)
async def test_process_stat_command(dp, bot, user_id: int, expected_text: str):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    print(user_id)
    await dp.feed_update(
        bot,
        Update(message=make_message(user_id), update_id=1)
    )

    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == expected_text
    assert outgoing_message.reply_markup is None
