from dotenv import load_dotenv
import requests
import json
import os
import argparse

URL_TEMPLATE = 'https://api-ssl.bitly.com/v4/{}'


def shorten_the_link(link, bitly_token):
  headers = {'Authorization': bitly_token}
  url = URL_TEMPLATE.format('shorten')
  body = { "long_url": link
  }
  response = requests.post(url, headers=headers, json=body)
  response.raise_for_status()
  link_line = response.json()
  bitlink = link_line["link"]
  return bitlink

def count_clicks(bitlink, bitly_token):
  headers = {'Authorization': bitly_token}
  
  params = {'unit': 'day', 'units':'-1',}
  url = "{}{}/clicks/summary".format(
    URL_TEMPLATE.format('bitlinks/'), 
    bitlink.replace('https://', '').replace('http://', '')
  )
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  clicks_line = response.json()
  clicks = clicks_line["total_clicks"]
  return clicks

def main():
  load_dotenv(dotenv_path='.env', verbose=True)
  bitly_token = os.getenv("BITLY_TOKEN")
  parser = argparse.ArgumentParser()
  parser.add_argument("link")
  args = parser.parse_args()
  
  if 'bit.ly' in args.link:
    try:
      clicks_count = count_clicks(args.link, bitly_token)
      print('кол-во переходов по ссылке:', clicks_count)
    except requests.exceptions.HTTPError:
      print('ссылка неверна')

  if 'bit.ly' not in args.link:
    try:
      bitlink = shorten_the_link(args.link, bitly_token)
      print(bitlink)
    except requests.exceptions.HTTPError:
      print('ссылка неверна')


if __name__ == '__main__':
  main()
  



