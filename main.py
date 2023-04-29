from selenium.webdriver import Keys
import pytest
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import random
import string

import requests

GEO_URL = 'http://api.openweathermap.org/geo/1.0/direct'
STATUS_OK = 200

#Тест проверяет, соответствуют ли значения температуры на веб-странице значениям в api сайта.
def test_city_temp_geo(): #для api-запроса температуры нужны геоданные города, получаем их из гео-api-запроса
    query_params = {
        'q': 'Reykjavík, IS',
        'appid': '40b38098e34cc96139b85134c113fe3b', #ключ дается сайтом перманентно при регистрации
        'limit': 1
    }
    response = requests.get(f'{GEO_URL}', params=query_params)
    response1 = response.json()[0]
    lat = response1['lat']
    lon = response1['lon']
    assert lat in response1.values()
    assert lon in response1.values()
    assert response.status_code == STATUS_OK
    list1 = [lat, lon]
    return list1


def test_city_temp_temperature(): #вставляем значения из гео-запроса (переменными) в запрос температуры с помощью конкатенации
    # (можно вставить готовые values для Рейкьявика, но переменные позволят не переписывать код под каждый город)
    geo = test_city_temp_geo() #используем return предыдущей функции
    lat1 = str(geo[0])
    lat2 = str(geo[1])
    appid1 = '40b38098e34cc96139b85134c113fe3b'
    response2 = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + lat1 + '&lon=' + lat2 + '&appid=' + appid1 + '&units=metric')
    response3 = response2.json()
    assert 'main' in response3
    response4 = response3['main']
    temp = response4['temp']
    assert temp in response4.values()
    temp_value = str(round(response4['temp']))
    assert response2.status_code == STATUS_OK
    print(temp_value + '°C')
    return temp_value

def test_city_temperature_selenium(driver):
    driver.get('http://openweathermap.org/')
    time.sleep(5)
    search_city_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Search city']")))
    search_city_field.send_keys('Reykjavík')
    search_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[class='button-round dark']")))
    search_button.click()
    search_option = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(), 'Reykjavík, IS')]")))
    search_option.click()
    expected_city = 'Reykjavík, IS'
    displayed_city = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//h2[contains(text(), 'Reykjavík, IS')]")))
    assert displayed_city.text == expected_city #проверяем, соответствует ли вывод запросу
    temperature_scale_choice = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Metric: °C, m/s')]")))  # удостоверимся, что шкала для теста - Цельсий (можно рассматривать это как precondition, но лучше подстраховаться)
    temperature_scale_choice.click()
    displayed_temperature = WebDriverWait(driver, 15).until(EC.presence_of_element_located( #проверяем, адекватны ли температурные значения
        (By.CSS_SELECTOR, "span[class='heading']")))
    print(displayed_temperature.text)
    temp_value_api = test_city_temp_temperature() #используем return прерыдущей функции
    assert displayed_temperature.text[:-2] == temp_value_api #сравниваем значание из API (с округлением и в типе int)
    # со значением с веб-страницы
    print('Compared successfully')
