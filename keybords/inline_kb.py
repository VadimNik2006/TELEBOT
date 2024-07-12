from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram import Router
from aiogram.filters import Command


def create_start_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня", callback_data="молодец")
    )
    return builder.as_markup()
