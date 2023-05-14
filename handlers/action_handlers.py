import time

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from functions import get_recipe, translator, message_builder, TranslatorApiError
from messages import GENERATION_ERROR_MESSAGE, SEARCH_ERROR_MESSAGE
from messages import STATES_MESSAGES as ST
from keyboards import swap_kb


class Searcher(StatesGroup):
    search = State()


class LastRequest:
    last_recipes = []


router = Router()


@router.message(Command('поиск'))
async def search(msg: types.Message, state: FSMContext):
    await msg.answer("@Введите ингредиенты.")
    await state.set_state(Searcher.search)


@router.message(Searcher.search)
async def search(msg: types.Message, state: FSMContext):
    start = time.time()
    await msg.answer(ST['check'])
    mes = msg.text
    mes = translator(mes, "en")
    result = get_recipe(mes.split())

    if result:
        print(f"|{msg.from_user.id} | {mes} | list_not_empty")
        await msg.answer(ST['get'])
        LastRequest.last_recipes = result
        try:
            ans = message_builder(result)
            print(f"|{msg.from_user.id} | {mes} | success | total time {int(time.time()-start)}")
            await msg.answer(ans, reply_markup=swap_kb(), parse_mode="HTML")
            await state.clear()
        except TranslatorApiError:
            print(f"|{msg.from_user.id} | {mes} | fail")
            await msg.answer(GENERATION_ERROR_MESSAGE)
            await state.clear()
    else:
        print(f"|{msg.from_user.id} | {mes} | list_empty")
        await msg.answer(SEARCH_ERROR_MESSAGE)
        await state.clear()


@router.callback_query(Text("random_recipe"))
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(ST['get'])
    try:
        await callback.message.answer(
            message_builder(LastRequest.last_recipes),
            reply_markup=swap_kb(), parse_mode="HTML"
        )
        await state.clear()
    except TranslatorApiError:
        await callback.message.answer(GENERATION_ERROR_MESSAGE)
        await state.clear()
