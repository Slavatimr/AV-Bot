from parsing.Api import Api
from parsing.Car import Car
from parsing.additional_funcs import *
from parsing.payloads import Payload


async def parse(payload: Payload, params: list, link="https://cars.av.by/filter"):
    api = Api(url=link, payload=payload)
    cars = await api.run()
    print(f"Найдено автомобилей по ссылке: {len(cars)}")
    car_handler = Car(cars=cars, url_base=api.url_base, params=params)
    await car_handler.run()
    list_by_ten_cars = proceed_messages_text(car_handler.text)
    return list_by_ten_cars


def get_info(payload=None, link="https://cars.av.by/filter"):

    with requests.Session() as session:
        soup = get_soup(link=link, session=session, payload=payload)
        cars_found = int(extract_number_from_string(soup.find('h3', class_='listing__title').text))
        waiting_time = (cars_found // 50) + cars_found / 12
        measurement = "сек"
        if waiting_time > 60:
            waiting_time = waiting_time / 60
            measurement = "мин"
            if waiting_time > 60:
                waiting_time = waiting_time / 60
                measurement = "часов"

    return cars_found, waiting_time, measurement
