import requests
import os
from typing import NoReturn

from dotenv import load_dotenv

load_dotenv()

cookies = {
    'Cookie': os.getenv('COOKIE')
}


class Attributes:

    def __init__(self, article: str) -> NoReturn:
        self.article = article

    def get_response(self):
        url = os.getenv('LINK') + self.article
        response = requests.get(url=url, cookies=cookies)
        return response

    def get_json(self) -> dict:
        return self.get_response().json()['recently'][0]

    def get_title(self) -> str:
        return self.get_json()['title'] + self.get_json()['brand']['title']

    def get_image(self) -> str:
        return f"https://a.lmcdn.ru/img600x866{self.get_json()['gallery'][0]}"

    def get_url(self) -> str:
        return f"""https://www.lamoda.ru/p/{self.article}/
                   {self.get_json()['seo_tail']}"""

    def get_api_url(self) -> str:
        return self.get_response().url
