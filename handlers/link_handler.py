from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import *
from filters.filters import *

router = Router()


@router.callback_query(F.data == "get_link")
async def get_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ссылку")
    await state.set_state(ChooseFilter.via_link)


@router.callback_query(F.data == "step_back" and ChooseFilter.via_link)
async def step_back_via_link(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    link = state_data['link']
    await callback.message.edit_text(f"Ваша ссылка: {link}", reply_markup=via_link_keyboard())


@router.message(ChooseFilter.via_link)
async def via_link(message: Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    await message.answer(f"Ваша ссылка: {link}", reply_markup=via_link_keyboard())
