import asyncio
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from time import time
import logging


from parsing.parse import parse


logging.basicConfig(level=logging.INFO)
router = Router()


@router.callback_query(F.data == "start_search")
async def start_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выполняю поиск...")
    start_time = time()
    state_data = await state.get_data()
    payload = state_data['payload'].payload()
    link = state_data['link']
    cars_found = state_data['cars_found']
    try:
        acceleration = float(state_data['acceleration'])
    except Exception:
        acceleration = 100
    try:
        consumption = float(state_data['consumption'])
    except Exception:
        consumption = 100
    try:
        tasks = [asyncio.create_task(renew(callback, cars_found)),
                 asyncio.create_task(async_parse(link=link, payload=payload, params=[acceleration, consumption],
                                                 state=state))]
        await asyncio.gather(*tasks)
        state_data = await state.get_data()
        list_by_ten_cars = state_data['list_by_ten_cars']
    except Exception as exc:
        await callback.message.edit_text(f"Ошибка: {exc}\n"
                                         f"Попробуй еще раз")
    if list_by_ten_cars:
        for ten_cars in list_by_ten_cars:
            await callback.message.answer(ten_cars)
    else:
        await callback.message.answer("Нет подходящих автомобилей:(")
    logging.log(msg=(time() - start_time), level=logging.INFO)
    await callback.message.edit_text(text=f"Поиск занял: {(time() - start_time):.3f}")
    await state.clear()


async def async_parse(link, payload, params, state: FSMContext):
    list_by_ten_cars = await parse(link=link, payload=payload, params=params)
    await state.update_data(list_by_ten_cars=list_by_ten_cars)


async def renew(callback: CallbackQuery, cars_found):

    waiting_time = (cars_found // 50) + (cars_found / 12)
    for five_sec in range(int(waiting_time/5)):
        print(waiting_time)
        await callback.message.edit_text(f"Выполняется поиск...\n"
                                         f"Осталось примерно {waiting_time:.3f}сек.")
        waiting_time -= 5
        await asyncio.sleep(5)
