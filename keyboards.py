from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram import types

def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="/контакты"), types.KeyboardButton(text="/гайд"))
    builder.row(types.KeyboardButton(text="/поиск"))
    builder.row(types.KeyboardButton(text="/парсер"))
    builder.row(types.KeyboardButton(text="/получить->лису"))
    return builder.as_markup()


def contacts_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Сюда ->", url='https://vk.com/moongook')
    )
    builder.row(types.InlineKeyboardButton(
        text="Или сюда ->",
        url="https://vk.com/id450950495")
    )
    return builder.as_markup()


def parses_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="/унции->ложки"))
    builder.row(types.KeyboardButton(text="/фунты->мг"))
    builder.row(types.KeyboardButton(text="/пинты->мл"))
    builder.row(types.KeyboardButton(text="/start"))
    return builder.as_markup()


def swap_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Поменять рецепты",
        callback_data="random_recipe")
    )
    return builder.as_markup()

