import requests
import argparse
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
    response = requests.post(request_url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data:
        return False
    if response_data["response"]["stats"] == []:
        return 0
    return response_data["response"]["stats"][0]["views"]


def is_shorten_link(token,url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != "vk.cc":
        return False
    if count_clicks(token, url) is False:
        return False
    return True


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("user_input", type=str, help="Enter your link")
    args = parser.parse_args()
    #user_input = input("Введите ссылку:")
    token = environ['VK_TOKEN']
    if is_shorten_link(token, args.user_input):
        clicks = count_clicks(token, args.user_input)
        print(f"Количество переходов по ссылке: {clicks}")
    else:
        short_link = shorten_link(token, args.user_input)
        print(f"Укороченная ссылка: {short_link}")



if __name__ == "__main__":
    main()
