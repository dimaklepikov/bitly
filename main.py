from dotenv import load_dotenv
load_dotenv()
import requests
import json
import os
import argparse

URL_TEMPLATE = 'https://api-ssl.bitly.com/v4/{}'
BITLY_TOKEN = os.getenv("BITLY_TOKEN")

def shorten_the_link(link):
  headers = {'Authorization': BITLY_TOKEN}
  url = URL_TEMPLATE.format('shorten')
  body = { "long_url": link
  }
  response = requests.post(url, headers=headers, json=body)
  response.raise_for_status()
  link_line = response.json()
  bitlink = link_line["link"]
  return bitlink

def count_clicks(bitlink):
  headers = {'Authorization': BITLY_TOKEN}
  
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
  parser = argparse.ArgumentParser()
  parser.add_argument("link")
  args = parser.parse_args()
  
  if 'bit.ly' in args.link:
    bitl_clicks = count_clicks(args.link)
    print('кол-во переходов по ссылке:', bitl_clicks)
    return
  
  try:
    bitlink = shorten_the_link(args.link)
    print(bitlink)
  except requests.exceptions.HTTPError:
    print('ссылка неверна')

  if 'bit.ly' in args.link:
    try:
      clicks_count = count_clicks(args.link)
      print('кол-во переходов по ссылке:', clicks_count)
    except requests.exceptions.HTTPError:
      print('ссылка неверна')

if __name__ == '__main__':
  main()



