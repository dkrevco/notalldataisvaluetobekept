
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

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_size(1920, 1080)

    def open_url(self, url):
        self.driver.get(url)
        self.url = url
        time.sleep(3)
        return self.url

class ShytokNet(Browser):

    def __init__(self):
        self.base_url = 'https://shytok.net/anekdots/vstretilis-russkij-nemec-kitaec.html'
        self.jokes_db = []

        super().__init__()

    def _get_paginated_number(self):
        pagination = self.driver.find_elements(By.XPATH, f"//ul[@class='pagination']//li")
        self.last_page = int(pagination[-2].text)
        return self.last_page

    def _find_jokes(self):

        self.jokes = self.driver.find_elements(By.XPATH, f"//div[@class='text2']")
        return self.jokes

    def _get_category_name(self):

        header = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.category_name = header.split(':')[-1]

        return self.category_name

    def _add_to_jokes_db(self):

        joke_item = {}

        for joke in self.jokes:
            joke_item[self.category_name] = f'{joke.text}'
            self.jokes_db.append(joke_item)

    def _create_data(self):

        self._find_jokes()
        self._add_to_jokes_db()

    def _open_paginated_pages(self):

        paginated_url = self.url.split('.html')[0]

        for i in range(2,self._get_paginated_number() + 1):
            self.open_url(f'{paginated_url}-{i}.html')
            self._create_data()

    def _create_local_file(self):

        file_name = self.url.split('.')[1].split('/')[-1]

        with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(self.jokes_db, file, indent=4, ensure_ascii=False)
            file.close()

    def run(self, url: str):

        try:
            self.open_url(url)
            self._get_category_name()
            self._get_paginated_number()
            self._create_data()
            if self._get_paginated_number() > 1:
                self._open_paginated_pages()
            self._create_local_file()
        except Exception as ex:
            print(ex)

if __name__ == '__main__':

    main = ShytokNet()

    url = 'https://shytok.net/anekdots/vstretilis-russkij-nemec-kitaec.html'

    main.run(url)

