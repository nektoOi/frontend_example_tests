import pytest
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import configparser
import os
import allure

config = configparser.ConfigParser()
config.read("settings.ini", "utf8")
url_adminka = config['bank'].get('url_adminka')
pass_adminka = config['bank'].get('pass_adminka')
login_adminka = config['bank'].get('login_adminka')


@pytest.fixture(scope="class", autouse=True)
@allure.story("Инициализируем драйвер")
def initWebDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="class", autouse=False)
@allure.story("Авторизация")
def auth(initWebDriver):
    initWebDriver.get(url_adminka + '/sign-in')
    time.sleep(1)
    initWebDriver.find_element(By.XPATH, '//input[@name= "email"]').send_keys(login_adminka)
    initWebDriver.find_element(By.XPATH, '//input[@name= "password"]').send_keys(pass_adminka)
    initWebDriver.find_element(By.XPATH, '//button[@type= "submit"]').click()
    time.sleep(1)
    config = configparser.ConfigParser()
    try:
        config.read("settings.ini", "utf8")
        external_id = config['bank'].get('external_id')
        domen_lk = config['bank'].get('domen_lk')
    except:
        config.read("../settings.ini", "utf8")
        external_id = config['bank'].get('external_id')
        domen_lk = config['bank'].get('domen_lk')
    initWebDriver.get(url_adminka + '/supervisor')
    initWebDriver.find_element(By.XPATH, '//input[@placeholder= "domain"]').send_keys(domen_lk)
    initWebDriver.find_element(By.XPATH, '//input[@placeholder= "external ID"]').send_keys(external_id)

    initWebDriver.find_element(By.XPATH, '//button[@class= "bp3-button bp3-intent-primary"]').click()
    time.sleep(1)

    initWebDriver.switch_to.window(initWebDriver.window_handles[0])
    url = initWebDriver.find_element(By.XPATH, '//b').text
    print(url)

    yield url


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Делает скриншот при упавшем тесте"""

    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'initWebDriver' in item.fixturenames:
                    web_driver = item.funcargs['initWebDriver']
                else:
                    print('Fail to take screen-shot')
                    return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))
