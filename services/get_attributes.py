import requests
import os
from typing import NoReturn, Union

from dotenv import load_dotenv

load_dotenv()

cookies = {
    'Cookie': os.getenv('COOKIE')
}


class Attributes:

    def __init__(self, article: str) -> NoReturn:
        self.article = article.rstrip().lstrip()

    def get_response(self):
        url = f"{os.getenv('LINK')}{self.article}"
        response = requests.get(url=url, cookies=cookies)
        return response

    def get_json(self) -> dict:
        return self.get_response().json()['recently'][0]

    def get_title(self) -> str:
        return f"""<b>{self.get_json()['title']} {self.get_json()['brand']['title']}</b>"""

    def get_image(self) -> str:
        return f"https://a.lmcdn.ru/img600x866{self.get_json()['gallery'][0]}"

    def get_url(self) -> str:
        return f"""https://www.lamoda.ru/p/{self.article}/{self.get_json()['seo_tail']}"""

    def get_api_url(self) -> str:
        return self.get_response().url

    def get_prices(self) -> Union[tuple[int, Union[int, None]]]:
        try:
            price = self.get_json()['old_price']
            sale_price = self.get_json()['price']
            return price, sale_price
        except KeyError:
            price = self.get_json()['price']
            return price, None
