import aiohttp
from parsing.additional_funcs import *
from tqdm import tqdm


class Api:

    def __init__(self, url, payload):
        self.url = url
        self.url_base = "https://cars.av.by"
        self.cars = None
        self.cars_found = None
        self.button = None
        self.session = None
        self.payload = payload

    async def __add_cars(self):
        """
        function returns cars from current page, also creates self.button
        :return: ResultSet of bs4 which represents cars
        """
        if not self.button:
            soup = get_soup(link=self.url, payload=self.payload)
            self.cars_found = extract_number_from_string(soup.find('h3', class_='listing__title').text)
        else:
            self.url = self.url_base + self.button.get('href')
            soup = await async_get_soup(link=self.url, session=self.session)
        self.button = soup.find('a', class_='button button--default', text="Показать ещё")
        cars = soup.find_all('div', class_='listing-item__wrap')
        return cars

    async def run(self):
        """
        function creates object ResultSet of bs4 which represents cars and writes it to self.cars
        """
        async with aiohttp.ClientSession() as session:
            self.session = session
            self.cars = await self.__add_cars()
            self.cars_found = int(self.cars_found // 25)
            for _ in tqdm(range(self.cars_found), desc="Collecting cars...", colour="Red"):
                try:
                    self.cars += await self.__add_cars()
                except Exception as exc:
                    print(exc.args)
                    break

        return self.cars
