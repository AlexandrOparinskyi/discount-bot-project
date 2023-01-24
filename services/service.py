import requests
import os

from dotenv import load_dotenv

load_dotenv()

cookies = {
    'Cookie': os.getenv('COOKIE')
}


def get_attributes(article: str) -> tuple[str, str, str, str]:
    url = os.getenv('LINK') + article
    res = requests.get(url=url, cookies=cookies)
    soup = res.json()['recently'][0]
    title = f"{soup['title']} {soup['brand']['title']}"
    image = f"https://a.lmcdn.ru/img600x866{soup['gallery'][0]}"
    url = f"https://www.lamoda.ru/p/{article}/{soup['seo_tail']}"
    api_url = res.url
    return title, image, url, api_url
