from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import *
from parsing.parse import get_info
from filters.filters import *


router = Router()


@router.callback_query(F.data == "accept")
async def accept(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    payload = state_data['payload'].payload()
    link = state_data['link']
    cars_found, waiting_time, measurement = get_info(link=link, payload=payload)
    await callback.message.edit_text(f"Найдено автомобилей: {cars_found}\n"
                                     f"Примерное время ожидания: {waiting_time:.{3}f} {measurement}\n",
                                     reply_markup=accept_keyboard())
    await state.update_data(cars_found=cars_found)
    if link == "https://cars.av.by/filter":
        await state.set_state(ChooseFilter.min_max)
    else:
        await state.set_state(ChooseFilter.via_link)


@router.callback_query(F.data == "step_back" and ChooseFilter.min_max)
async def step_back_min_max(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await callback.message.edit_text(f"Год: от {state_data['payload'].year_min} до {state_data['payload'].year_max}\n"
                                     f"Цена: от {state_data['payload'].price_min}"
                                     f" до {state_data['payload'].price_max}$\n"
                                     f"Объём: от {state_data['payload'].capacity_min}"
                                     f" до {state_data['payload'].capacity_max} мл.\n",
                                     reply_markup=min_max_params_keyboard())
    await state.set_state(ChooseFilter.year_price_capacity)


@router.callback_query(F.data == "add_params")
async def add_params(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите параметры разгона и расхода в виде 'разгон//расход'")
    await state.set_state(ChooseFilter.add_params)


@router.message(ChooseFilter.add_params)
async def get_add_params(message: Message, state: FSMContext):
    try:
        acceleration, consumption = message.text.split("//")
        acceleration = acceleration
        consumption = consumption
    except Exception:
        await message.answer(f"Неккоректный ввод, введите параметры разгона и расхода в виде 'разгон//расход'")
        return
    await state.update_data(acceleration=acceleration, consumption=consumption)
    state_data = await state.get_data()
    payload = state_data['payload'].payload()
    link = state_data['link']
    cars_found, waiting_time, measurement = get_info(link=link, payload=payload)
    await message.answer(f"Найдено автомобилей: {cars_found}\n"
                         f"Примерное время ожидания: {waiting_time:.{3}f} {measurement}\n"
                         f"Разгон до {acceleration}, расход до {consumption}",
                         reply_markup=accept_keyboard())
    await state.update_data(cars_found=cars_found)
    if link == "https://cars.av.by/filter":
        await state.set_state(ChooseFilter.min_max)
    else:
        await state.set_state(ChooseFilter.via_link)
