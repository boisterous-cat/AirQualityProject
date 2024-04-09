from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.keyboards import keyboard, df_show_keyboard
from filters.is_admin import IsAdmin, admin_id
import operator
from data import work_with_data
from typing import Union
import pandas as pd
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramNotFound

# Инициализируем роутер уровня модуля
router = Router()
# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()
# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, Union[int, float, None]]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_co = State()  # Состояние ожидания ввода co
    fill_no = State()  # Состояние ожидания ввода no
    fill_ozone = State()  # Состояние ожидания ozone
    fill_pm2 = State()  # Состояние ожидания pm2


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы отменили запись значений\n\n'
             'Чтобы снова перейти к заполнению - '
             'отправьте команду /aqi'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /aqi
# и переводить бота в состояние ожидания ввода имени
@router.message(Command(commands='aqi'), StateFilter(default_state))
async def process_aqi_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите уровень CO')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_co)


# Этот хэндлер будет срабатывать, если введен корректный co
# и переводить в состояние no
@router.message(StateFilter(FSMFillForm.fill_co),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200)
async def process_co_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "co"
    await state.update_data(co=message.text)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите уровень NO')
    # Устанавливаем состояние ожидания NO
    await state.set_state(FSMFillForm.fill_no)


# Этот хэндлер будет срабатывать, если введен корректный no
# и переводить в состояние ozone
@router.message(StateFilter(FSMFillForm.fill_no),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200)
async def process_no_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "co"
    await state.update_data(no=message.text)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите уровень Ozone')
    # Устанавливаем состояние ожидания NO
    await state.set_state(FSMFillForm.fill_ozone)


# Этот хэндлер будет срабатывать, если во время ввода no или CO
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_co))
@router.message(StateFilter(FSMFillForm.fill_no))
async def warning_not_no(message: Message):
    await message.answer(
        text='Некорректный ввод. Показатель должен быть целым числом от 0 до 200\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение данных - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если введен корректный ozone
# и переводить в состояние pm2
@router.message(StateFilter(FSMFillForm.fill_ozone),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 300)
async def process_ozone_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "co"
    await state.update_data(ozone=message.text)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите уровень PM2.5')
    # Устанавливаем состояние ожидания NO
    await state.set_state(FSMFillForm.fill_pm2)


# Этот хэндлер будет срабатывать, если во время ввода ozone
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_ozone))
async def warning_not_ozone(message: Message):
    await message.answer(
        text='Уровень Ozone должен быть целым числом от 0 до 300\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение данных - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если введен корректный pm
# и выводить из машины состояний
@router.message(StateFilter(FSMFillForm.fill_pm2),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 500)
async def process_pm_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "co"
    await state.update_data(pm=message.text)
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    user_data = user_dict[message.from_user.id]
    df = pd.DataFrame([[user_data['co'], user_data['no'], user_data['ozone'], user_data['pm']]],
                      columns=['CO AQI Value', 'NO2 AQI Value', 'Ozone AQI Value', 'PM2.5 AQI Value'])
    # Завершаем машину состояний
    await state.clear()
    res, cat, img_link = work_with_data.predict_model(df)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text=f'Спасибо!\n\nИндекс = {res}\n\n'
             f'Категория качества = {cat}')
    await message.answer_photo(FSInputFile(path=img_link))


# Этот хэндлер будет срабатывать, если во время ввода pm
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_pm2))
async def warning_not_pm(message: Message):
    await message.answer(
        text='Уровень PM2.5 должен быть целым числом от 0 до 500\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение данных - отправьте команду /cancel'
    )


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/project"
@router.message(Command(commands='project'))
async def process_project_command(message: Message):
    await message.answer(
        text='Перейти на страницу проекта в gitHub или связаться с автором🤔',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на команду "/top"
@router.message(Command(commands='top'))
async def process_top_command(message: Message):
    await message.answer(
        text='Выберите какие города показать',
        reply_markup=df_show_keyboard
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'top_10_pressed'
@router.callback_query(F.data == 'top_10_pressed')
async def process_top_10_press(callback: CallbackQuery):
    res = work_with_data.top_10()
    await callback.message.answer(
        text=f"Топ 10 лучших городов:\n<pre>{res}</pre>",
        parse_mode='HTML')


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'less_10_pressed'
@router.callback_query(F.data == 'less_10_pressed')
async def process_less_10_press(callback: CallbackQuery):
    await callback.message.answer(
        text=f"Топ 10 худших городов:\n<pre>{work_with_data.less_10()}</pre>",
        parse_mode='HTML')


not_admin = operator.not_(IsAdmin(admin_id))


# Этот хэндлер срабатывает на команду /stat
@router.message(~(IsAdmin(admin_id)), Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.reply(text=LEXICON_RU['not admin'])


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    try:
        await message.reply(text=LEXICON_RU['no_echo'])
    except TelegramNotFound:
        print("chat, message, user, etc. not found")
        return
