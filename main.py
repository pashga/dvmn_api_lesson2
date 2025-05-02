import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    payload = {
        "access_token": token,
        "v": 5.199,
        "url": url,
    }
    url_vk = "https://api.vk.ru/method/utils.getShortLink"
    responce = requests.get(url_vk, params=payload)
    responce.raise_for_status()
    rsp = responce.json()
    return rsp['response']["short_url"]


def count_clicks(token, link):
    payload = {
        "access_token": token,
        "v": 5.199,
        "key": link[-6:],
        "interval": "forever",
    }
    url_vk = "https://api.vk.ru/method/utils.getLinkStats"
    responce = requests.get(url_vk, params=payload)
    responce.raise_for_status()
    clicks_count = responce.json()
    return clicks_count["response"]["stats"][0]["views"]


def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != "vk.cc":
        return False
    return count_clicks(token, url)


def main():
    load_dotenv()
    user_input = input("Введите ссылку:")
    token = os.getenv("VK_TOKEN")
    try:
        if is_shorten_link(token=token, url=user_input):
            clicks = count_clicks(token=token, link=user_input)
            print(f"Количество переходов по ссылке: {clicks}")
        else:
            short_link = shorten_link(token=token, url=user_input)
            print(f"Укороченная ссылка: {short_link}")
    except KeyError:
        print(f"Неправильный сайт!")


if __name__ == "__main__":
    main()
