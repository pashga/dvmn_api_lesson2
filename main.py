import requests
from os import environ
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    payload = {
        "access_token": token,
        "v": 5.199,
        "url": url,
    }
    url_vk = "https://api.vk.ru/method/utils.getShortLink"
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    response_json = response.json()
    return response_json['response']["short_url"]


def count_clicks(token, link):
    payload = {
        "access_token": token,
        "v": 5.199,
        "key": link[-6:],
        "interval": "forever",
    }
    url_vk = "https://api.vk.ru/method/utils.getLinkStats"
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    clicks_count = response.json()
    return clicks_count["response"]["stats"][0]["views"]


def is_shorten_link(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != "vk.cc":
        return False
    return True


def main():
    load_dotenv()
    user_input = input("Введите ссылку:")
    token = environ['VK_TOKEN']
    if is_shorten_link(user_input):
        clicks = count_clicks(token, user_input)
        print(f"Количество переходов по ссылке: {clicks}")
    else:
        short_link = shorten_link(token, user_input)
        print(f"Укороченная ссылка: {short_link}")



if __name__ == "__main__":
    main()
