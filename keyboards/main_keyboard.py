from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def go_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="Год", callback_data="year"),
        InlineKeyboardButton(text="Цена", callback_data="price"),
        InlineKeyboardButton(text="Объём", callback_data="engine_capacity")
    )
    kb.row(InlineKeyboardButton(text="Поиск по ссылке", callback_data="get_link"))
    return kb.as_markup()


def min_max_params_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="Год", callback_data="year"),
        InlineKeyboardButton(text="Цена", callback_data="price"),
        InlineKeyboardButton(text="Объём", callback_data="engine_capacity")
    )
    kb.row(InlineKeyboardButton(text="Подтвердить", callback_data="accept"))
    return kb.as_markup()


def accept_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="Начать поиск", callback_data="start_search"),
        InlineKeyboardButton(text="Вернуться назад", callback_data="step_back")
    )
    kb.row(InlineKeyboardButton(text="Добавить параметры", callback_data="add_params"))
    return kb.as_markup()


def via_link_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="Подтвердить", callback_data="accept"),
        InlineKeyboardButton(text="Изменить", callback_data="get_link")
    )
    return kb.as_markup()
