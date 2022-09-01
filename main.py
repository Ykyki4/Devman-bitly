import requests
import os
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv


def is_bitlink(user_url, token):
    parsed_url = urlparse(user_url)
    bearer_token = {'Authorization': f'Bearer {token}'}
    if parsed_url.scheme == "https" or parsed_url.scheme == "http":
        url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.hostname}{parsed_url.path}'
    else:
        url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.path}'
    response = requests.get(url, headers=bearer_token)
    return response.ok


def shorten_link(token, user_url):
    bearer_token = {'Authorization': f'Bearer {token}'}
    long_url = {"long_url": user_url}
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(url, headers=bearer_token, json=long_url)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(user_url, token):
    bearer_token = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(user_url)
    if parsed_url.scheme == "https" or parsed_url.scheme == "http":
        bitlink = f'{parsed_url.hostname}{parsed_url.path}'
    else:
        bitlink = f'{parsed_url.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=bearer_token)
    response.raise_for_status()
    return response.json()['total_clicks']


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_url")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    args = arg_parser()
    user_url = args.user_url
    try:
        if is_bitlink(user_url, bitly_token):
            print('Кол-во кликов:', count_clicks(user_url, bitly_token))
        else:
            print('Битлинк', shorten_link(bitly_token, user_url))
    except requests.exceptions.HTTPError:
         print('Wrong url. Please try again.')
