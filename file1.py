import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import pytest



GEO_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_WEB_URL = 'http://openweathermap.org/'
STATUS_OK = 200
WEATHER_API_APPID = '40b38098e34cc96139b85134c113fe3b' # ключ дается сайтом перманентно при регистрации
NAME_CITY = 'Reykjavík, IS'
PARAM_WEATHER_KEY = 'wind'
PARAM_WEATHER_VALUE = 'speed'
SEARCH_OPTION_SELECTOR = '//span[contains(text(), "Reykjavík, IS")]'
DISPLAYED_CITY_SELECTOR = '//h2[contains(text(), "Reykjavík, IS")]'
DISPLAYED_PARAM_SELECTOR = 'div[class="wind-line"]'

@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope='module')
def api_geo():
    geo_params = {
        'q': NAME_CITY,
        'appid': WEATHER_API_APPID,
        'limit': 1
    }
    response_geo = requests.get(GEO_URL, params=geo_params)
    assert response_geo.status_code == STATUS_OK
    assert response_geo is not None
    response_geo_data = response_geo.json()[0]
    lat = response_geo_data['lat']
    lon = response_geo_data['lon']
    assert lat in response_geo_data.values()
    assert lon in response_geo_data.values()
    return lat, lon

@pytest.fixture()
def api_weather(api_geo):
    lat, lon = api_geo
    response_weather = requests.get(WEATHER_API_URL, {
        'lat': lat,
        'lon': lon,
        'appid': WEATHER_API_APPID,
        'units': 'metric'
    })
    assert response_weather.status_code == STATUS_OK
    assert response_weather is not None
    response_weather_data = response_weather.json()
    assert PARAM_WEATHER_KEY in response_weather_data.keys()
    return response_weather_data

@pytest.fixture()
def api_param(api_weather):
    response_weather_by_key = api_weather[PARAM_WEATHER_KEY]
    raw_param = response_weather_by_key[PARAM_WEATHER_VALUE]
    assert raw_param in response_weather_by_key.values()
    final_param = round(float(raw_param))
    return final_param

@pytest.fixture()
def web_param(driver):
    driver.get(WEATHER_WEB_URL)
    time.sleep(5)
    search_city_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Search city']")))
    search_city_field.send_keys(NAME_CITY)
    search_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[class='button-round dark']")))
    search_button.click()
    search_option = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, SEARCH_OPTION_SELECTOR)))
    search_option.click()
    expected_city = NAME_CITY
    displayed_city = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, DISPLAYED_CITY_SELECTOR)))
    assert displayed_city.text == expected_city
    temperature_scale_choice = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, '//div[contains(text(), "Metric: °C, m/s")]')))  # удостоверимся, что шкала для теста - Цельсий (можно рассматривать это как precondition, но лучше подстраховаться)
    temperature_scale_choice.click()
    displayed_param = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, DISPLAYED_PARAM_SELECTOR)))
    displayed_param1 = displayed_param.text
    pattern = re.compile(r'^([0-9]+[.]?[0-9]*)')
    final_displayed_param = round(float(pattern.match(displayed_param1).group(1)))
    return final_displayed_param

def test_matching_param(api_param, web_param):
    assert abs(web_param-api_param) <= 2
    print('Matched successfully')