from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import *
from parsing.payloads import *
from filters.filters import *


router = Router()


@router.callback_query(F.data.in_(("year", "price", "engine_capacity")), ChooseFilter.year_price_capacity)
async def year(callback: CallbackQuery, state: FSMContext):
    """
    При выборе параметров год, цена, объём поападает сюда за счет состояния choosefilter после чего ожидает сообщения
    с параметрами 'от и до'
    :param callback:
    :param state:
    :return:
    """
    await state.update_data(filter=callback.data)
    await callback.message.edit_text(f"Введите {data[callback.data]} вида 'от//до'")
    await callback.answer()
    await state.set_state(ChooseFilter.min_max)


@router.message(ChooseFilter.min_max)
async def min_max_params(message: Message, state: FSMContext):
    """
    Обрабатывает принятое сообщение с параметрами "от и до" и возвращает сообщение с уже записанной информацией
    :param message:
    :param state:
    :return:
    """
    state_data = await state.get_data()
    try:
        from_, to = message.text.split("//")
        if from_ != "":
            from_ = int(from_)
        if to != "":
            to = int(to)
            if "" != from_ > to:
                raise ValueError
    except ValueError:
        await message.answer(f"Неккоректный ввод, введите {data[state_data['filter']]} вида 'от//до'")
        return
    match state_data['filter']:
        case "year":
            state_data["payload"].year_min, state_data["payload"].year_max = from_, to
        case "price":
            state_data["payload"].price_min, state_data["payload"].price_max = from_, to
        case "engine_capacity":
            state_data["payload"].capacity_min, state_data["payload"].capacity_max = from_, to
    await state.update_data(filter=None)
    await message.answer(f"Год: от {state_data['payload'].year_min} до {state_data['payload'].year_max}\n"
                         f"Цена: от {state_data['payload'].price_min} до {state_data['payload'].price_max}$\n"
                         f"Объём: от {state_data['payload'].capacity_min} до {state_data['payload'].capacity_max}мл.\n",
                         reply_markup=min_max_params_keyboard())
    await state.set_state(ChooseFilter.year_price_capacity)
