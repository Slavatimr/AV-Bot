from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from parsing.payloads import *
from filters.filters import *
from keyboards.main_keyboard import *


router = Router()


# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет, я помогу тебе быстренько найти авто с av.by по параметрам,"
                         " отправляй мне комманду /go чтобы начать или /help чтобы ппрочитать инструкцию")


@router.message(Command("go"))
async def cmd_go(message: Message, state: FSMContext):
    """
    Сбрасывает все параметры и состояние и запускает процесс выбора параметров
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await state.set_state(ChooseFilter.year_price_capacity)
    payload = Payload()
    link = "https://cars.av.by/filter"
    await state.update_data(payload=payload, link=link)
    await message.answer("Выбери параметр", reply_markup=go_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Чтобы начать поиск отправляй комманду /go. Выбери любой из параметров для поиска по "
                         "параметрам (пока что доступны год, цена и объем) или выбирай поиск по ссылке и вводи "
                         "ссылку на страницу av.by с отфильтрованными авто по твоим запросам, далее выбирай добавить"
                         " параметры чтобы выбрать авто по разгону и расходу. Чтобы начать новый поиск отправляй /go."
                         " Вот и все пока")
