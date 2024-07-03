from bs4 import BeautifulSoup
import requests


def get_soup(link, session=requests, payload=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    response = session.get(link, headers=headers, params=payload)
    print(response.status_code)
    print(BeautifulSoup(response.text, "html.parser"))


get_soup(link="https://av.by/")

