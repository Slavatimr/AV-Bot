from bs4 import BeautifulSoup
import requests


HEADERS = {'user-agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',}


def get_soup(link, session=requests, payload=None):
    response = session.get(link, headers=HEADERS, params=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def extract_number_from_string(string):

    number = ""
    for char in string:
        if char.isdigit():
            number += char
        elif char == "." or char == ",":
            number += char
        elif char == " ":
            continue

    return float(number)


async def async_get_soup(link, session):
    async with session.get(link, headers=HEADERS) as response:
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        return soup


def proceed_messages_text(final_cars):
    list_by_ten_cars = []
    list_of_all_cars = final_cars.splitlines()
    cars = ""
    for i in range(1, len(list_of_all_cars) + 1):
        cars += list_of_all_cars[i - 1] + "\n"
        if i % 10 == 0:
            list_by_ten_cars.append(cars)
            cars = ""
    if len(list_of_all_cars) % 10 != 0:
        list_by_ten_cars.append(cars)
    return list_by_ten_cars
