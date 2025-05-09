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
    request_url = "https://api.vk.ru/method/utils.getShortLink"
    response = requests.get(request_url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    return response_data['response']["short_url"]


def count_clicks(token, link):
    payload = {
        "access_token": token,
        "v": 5.199,
        "key": link[-6:],
        "interval": "forever",
    }
    request_url = "https://api.vk.ru/method/utils.getLinkStats"
    response = requests.get(request_url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data:
        return False
    return response_data["response"]["stats"][0]["views"]


def is_shorten_link(token,url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != "vk.cc":
        return False
    if not count_clicks(token, url):
        return False
    return True


def main():
    load_dotenv()
    user_input = input("Введите ссылку:")
    token = environ['VK_TOKEN']
    if is_shorten_link(token, user_input):
        clicks = count_clicks(token, user_input)
        print(f"Количество переходов по ссылке: {clicks}")
    else:
        short_link = shorten_link(token, user_input)
        print(f"Укороченная ссылка: {short_link}")



if __name__ == "__main__":
    main()
