from aiogram import Router, types

from functions import hello_builder

router = Router()


@router.message()
async def repl(message: types.Message):
    await message.answer(hello_builder(message.text))


