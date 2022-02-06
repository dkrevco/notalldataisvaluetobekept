# import pandas as pd
# import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_index_result(url, headless=True):
    """
    :param url: str
    :param headless: True
    :return: list
    """

    print(f'Opening {url}')
    data = []
    # Search Engines Block
    google_xpath = '//*[@id="result-stats"]'
    google_request = f'https://www.google.com/search?q=site%3A{url}'
    yandex_xpath = '//*[@id="search-result-aside"]/div/div[2]'
    yandex_request = f'https://yandex.ru/search/?text=site%3A{url}&lr=2'

    # Selenium Settings
    options = Options()
    options.headless = headless
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Google data
    driver.get(google_request)
    google_index = driver.find_element(By.XPATH, google_xpath).text
    google_index = google_index.split("Результатов: примерно ")[1].split("(")[0].replace(" ", "")
    print(f'В Google проиндексировано {google_index} страниц')
    data.append(google_index)

    # Yandex data
    driver.get(yandex_request)
    yandex_index = driver.find_element(By.CLASS_NAME, "serp-adv__found").text

    if yandex_index.find("тыс.") > 0:
        yandex_index = yandex_index.split("Нашлось ")[1].split(" тыс.")[0]
        yandex_index = str(int(yandex_index) * 1000)
    else:
        yandex_index = yandex_index.split("Нашлось ")[1].split(' результатов')[0]

    print(f"В Яндексe {yandex_index} результатов")
    data.append(yandex_index)

    return data


if __name__ == '__main__':

    indexes = {}
    url = 'iport.ru'
    index = get_index_result(url)
    indexes[url] = index
