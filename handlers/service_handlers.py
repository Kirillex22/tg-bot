from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functions import from_old_to_new, image_handler, get_rand_cat
from messages import GUIDE_MESSAGE, WELCOME_MESSAGE, INPUT_ERROR_MESSAGE, FOX_ERROR_MESSAGE, STATES_MESSAGES
from keyboards import main_menu_kb, contacts_kb, parses_kb


class Calculator(StatesGroup):
    enter = State()


class FoxException(Exception):
    pass

class Service:
    start_counter = 0
    type_i = "default"


router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    if Service.start_counter == 0:
        Service.start_counter = 1
        await message.answer(
            WELCOME_MESSAGE,
            reply_markup=main_menu_kb(),
            parse_mode= "HTML"
        )
    else:
        await message.answer(
            "Любопытный факт: вы тут уже были.",
            reply_markup=main_menu_kb()
        )


@router.message(Command('контакты'))
async def cmd_inline_url(message: types.Message, bot: Bot):
    await message.answer(
        '@Нужна <b>помощь?</b> Вам',
        reply_markup=contacts_kb(),
        parse_mode= "HTML"
    )


@router.message(Command('гайд'))
async def guide(message: types.Message):
    await message.answer(GUIDE_MESSAGE, parse_mode= "HTML")


@router.message(Command('парсер'))
async def parser(message: types.Message):
    await message.answer(
        "@Выберите нужный парс.",
        reply_markup=parses_kb()
    )


@router.message(Command('унции->ложки'))
async def parser(message: types.Message, state: FSMContext):
    Service.type_i = "унций(я)"
    await message.answer("@Введите количество унций.")
    await state.set_state(Calculator.enter)


@router.message(Command('фунты->мг'))
async def parser(message: types.Message, state: FSMContext):
    Service.type_i = "фунт(ов)"
    await message.answer("@Введите количество фунтов.")
    await state.set_state(Calculator.enter)


@router.message(Command('пинты->мл'))
async def parser(message: types.Message, state: FSMContext):
    Service.type_i = "пинт(а)"
    await message.answer("@Введите количество пинт.")
    await state.set_state(Calculator.enter)


@router.message(Calculator.enter)
async def parser(message: types.Message, state: FSMContext):
    mes = message.text
    try:
        ans = from_old_to_new(int(mes), Service.type_i)
        await message.answer(f"{mes} {Service.type_i} - {ans[0]} {ans[1]}")
        await state.clear()
    except:
        await message.answer(INPUT_ERROR_MESSAGE)
        await state.clear()


@router.message(Command('получить->лису'))
async def cat(message: types.Message):
    await message.answer(STATES_MESSAGES['get'])
    try:
        await message.answer_photo(
            photo = image_handler(get_rand_cat())
        )
    except Exception:
        await message.answer(FOX_ERROR_MESSAGE)
        raise FoxException('Photo API error')
