from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time
import json

class Browser:

    def __init__(self):

        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={headers}')
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        # self.driver.set_window_size(1920, 1080)


    def open_url(self, url):

        print(f'open {url}')
        self.url = url
        self.driver.get(url)
        time.sleep(2)
        return self.url

class ShytokNet(Browser):

    def __init__(self):

        super().__init__()


    def run(self, url: str):

        self.jokes_db = []

        try:
            self._get_file_name(url)
            self.open_url(url)
            self._get_category_name()
            self._get_paginated_number()
            self._add_joke_items_to_db()
            if self._get_paginated_number() > 1:
                self._open_paginated_pages()
            self._write_jokes_to_local_file()
        except Exception as ex:
            print(ex)

    def _get_file_name(self, url):

        self.file_name = url.split('.')[1].split('/')[-1]
        return self.file_name


    def _get_category_name(self):

        self.category_name = ''
        header = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.category_name = header.split(':')[-1]

        return self.category_name

    def _add_joke_items_to_db(self):
        self._find_jokes()
        self._create_joke_items_for_db()

    def _find_jokes(self):

        self.jokes = self.driver.find_elements(By.XPATH, f"//div[@class='text2']")
        return self.jokes

    def _create_joke_items_for_db(self):

        for joke in self.jokes:
            joke_item = {}
            joke_item[self.category_name] = f'{joke.text}'
            self.jokes_db.append(joke_item)

    def _write_jokes_to_local_file(self):

        print(f'write about {self.category_name}')

        if os.path.exists(f'{self.file_name}.json'):
            with open(f'{self.file_name}.json', 'a', encoding='utf-8') as self.file:
                json.dump(self.jokes_db, self.file, indent=4, ensure_ascii=False)
        else:
            with open(f'{self.file_name}.json', 'w', encoding='utf-8') as self.file:
                json.dump(self.jokes_db, self.file, indent=4, ensure_ascii=False)

        return self.file



    def _open_paginated_pages(self):

        paginated_url = self.url.split('.html')[0]

        for i in range(2, self._get_paginated_number() + 1):
            self.open_url(f'{paginated_url}-{i}.html')
            self._add_joke_items_to_db()

    def _get_paginated_number(self):
        pagination = self.driver.find_elements(By.XPATH, f"//ul[@class='pagination']//li")
        self.last_page = int(pagination[-2].text)
        return self.last_page



def main():

    urls = [
            # 'https://shytok.net/anekdots/vstretilis-russkij-nemec-kitaec.html',
            # 'https://shytok.net/anekdots/anekdoty-pro-vasiliya-ivanovicha-i-petku.html',
            # 'https://shytok.net/anekdots/anekdoty-pro-poruchika-rzhevskogo.html',
            'https://shytok.net/anekdots/anekdoty-pro-vovochku.html',
            'https://shytok.net/anekdots/anekdoty-pro-evreev.html',
            'https://shytok.net/anekdots/anekdoty-pro-shtirlica.html'
            ]
    joke_parser = ShytokNet()

    for url in urls:
        joke_parser.run(url)

if __name__ == '__main__':
    main()







