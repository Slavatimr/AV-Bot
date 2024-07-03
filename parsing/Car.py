from parsing.additional_funcs import *
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)


class Car:

    def __init__(self, cars, url_base, params):
        self.url_base = url_base
        self.cars = cars
        self.session = None
        self.text = ""
        self.acceleration = params[0]
        self.consumption = params[1]

    async def run(self):
        await self.proceed()

    async def proceed(self):
        """

        """
        tasks = []
        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session:
            for car in self.cars:
                tasks.append(asyncio.create_task(self.proceed_car(car, session)))
            await asyncio.gather(*tasks)

    async def proceed_car(self, car, session):
        soup = await async_get_soup(self.url_base + car.find('a', class_='listing-item__link').get('href'),
                                    session=session)
        try:
            link = soup.find('a', text='Все параметры').get('href')
            soup = await async_get_soup(link, session=session)
            acceler = soup.find('dt', class_='modification-list-label', text='Разгон до 100 км/ч')
            acceler_value = extract_number_from_string(acceler.find_next().text)
            consumpt = soup.find('dt', class_='modification-list-label',
                                 text='Расход топлива в городе на 100 км')
            consumpt_value = extract_number_from_string(consumpt.find_next().text)
            if acceler_value <= self.acceleration and consumpt_value <= self.consumption:
                self.text += (f"{car.find('span', class_='link-text').text.strip()}, "
                              f"разгон: {acceler_value}, расход: {consumpt_value} "
                              f"{self.url_base + car.find('a', class_='listing-item__link').get('href')} \n")
        except AttributeError:
            logging.log(msg=f"{car.find('span', class_='link-text').text.strip()} Не имеет раздела 'Все параметры'\n",
                        level=logging.WARNING)
        except TypeError:
            logging.log(msg=f"{car.find('span', class_='link-text').text.strip()} Не имеет характеристик\n",
                            level=logging.WARNING)
        except ValueError:
            logging.log(msg=f"{car.find('span', class_='link-text').text.strip()} Не имеет характеристик\n",
                        level=logging.WARNING)
