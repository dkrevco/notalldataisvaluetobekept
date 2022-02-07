from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests, io, time, json
import pandas as pd
from collections import Counter

with open('csv/urls.txt', 'r') as file:
    urls = file.read().splitlines()
    print(urls)

ua = UserAgent

headers = {
    'User-Agent': ua.chrome
}

api_key = 'AIzaSyAh3KpMT7Ojky4Niraun-rxtLaTrwwqRpo'


def gkb_api(keyword):

    url = f"https://kgsearch.googleapis.com/v1/entities:search?query="+keyword+f"&key={api_key}&limit=1&indent=True"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data = payload)

    data = json.loads(response.text)

    try:
        get_label = data['itemListElement'][0]['result']['@type']
    except:
        get_label = ['none']

    return get_label

full_list = []
stop_words = ['и','в','а','мы','они','по','без','за','до']
output = ''

blacklist = ['[document]','noscript','header','html','meta','head',
                'input','script','style','input']

ban_chars = ['|','/','&']

for url in urls:
    time.sleep(2)

    print(f"requesting {url}")

    res = requests.get(url, headers=headers)
    page = res.content
    soup = BeautifulSoup(page, 'lxml')
    text = soup.find_all(text=True)

    for t in text:
        if t.parent.name not in blacklist:
            output += t.replace("\n", "").replace("\t", "")

    output = output.split(" ")

    output = [x for x in output if not x == '' and not x[0] =='#' and x not in ban_chars]
    output = [x.lower() for x in output]
    output = [word for word in output if word not in stop_words]

    full_list += output




