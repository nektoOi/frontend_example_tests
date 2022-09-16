from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import configparser
import allure

config = configparser.ConfigParser()
config.read("settings.ini", "utf8")
domen_lk = config['bank'].get('domen_lk')


class BonusProgram:
    def __init__(self, initWebDriver):
        self.driver = initWebDriver

        # Раздел программы
        self.program_kesh_rubli = (By.XPATH, "//span[text() = 'Кэшбэк-рубли' and contains(@class, 'ListItemCore')]")
        self.program_36_6 = (By.XPATH, "//span[text() = 'Клуб 36,6' and contains(@class, 'ListItemCore')]")

        # Основной раздел
        self.name_program = (By.XPATH, "(//span[contains(@class, 'PlainHeader__DefaultTitle')])[2]")
        self.balance_program = (By.XPATH, "(//span[contains(@class, 'BalanceValue__ValueContainer')])")
        self.balance_text = (By.XPATH, "(//span[contains(@class, 'BannerComponents__Text')])")

        # Раздел привязки
        self.name_card_in_link = (By.XPATH, "(//span[contains(@class, 'EntityControlElement__Title')])")
        self.img_card_in_link = (By.XPATH, "(//div[contains(@class, 'EntityControlElement__Icon')])//img")

        # Меню
        self.button_bonus_program = (
            By.XPATH, "//div[contains(@class, 'MenuButtonView__TextContainer') and text() = 'Бонусные программы']")

    def click_on_bonus_program_in_menu(self):
        """Кликает по бонусным программам в левом меню"""

        with allure.step('Кликает по бонусным программам в левом меню'):
            self.driver.find_element(*self.button_bonus_program).click()
            assert self.driver.current_url == "https://" + domen_lk + "/programs/99990029"

    # Раздел программы
    def click_on_program_36_6(self):
        """Кликает по бонусной программе 36.6"""

        with allure.step('Кликает по бонусной программе 36.6'):
            self.driver.find_element(*self.program_36_6).location_once_scrolled_into_view
            self.driver.find_element(*self.program_36_6).click()

    def click_on_program_kesh_rubli(self):
        """Кликает по бонусной программе Кэш рубли"""

        with allure.step('Кликает по бонусной программе Кэш рубли'):
            self.driver.find_element(*self.program_kesh_rubli).click()

    # Основной раздел
    def check_name_program_on_page(self, name_programm: str):
        """Проверяет название программы"""

        with allure.step(f'Проверяет что название программы  - {name_programm}'):
            name_program_on_page = self.driver.find_element(*self.name_program).text
            assert name_program_on_page == name_programm

    def balance_program_not_found(self):
        """Проверяет что на странице не отображается баланс"""

        with allure.step(f'Проверяет что на странице не отображается баланс'):
            try:
                self.driver.find_element(*self.balance_program)
                return False
            except NoSuchElementException:
                return True

    def balance_program_found(self):
        """Получает баланс бонусной программы"""

        with allure.step(f'Получает баланс бонусной программы'):
            balance_program = self.driver.find_element(*self.balance_program).text
            return balance_program

    def check_name_balance(self, name_balance: str):
        """Проверяет название баланса"""

        with allure.step(f'Проверяет что название баланса  - {name_balance}'):
            assert self.driver.find_element(*self.balance_text).text == name_balance

    # Раздел привязки
    def check_name_card(self, name_cart: str):
        """'Проверяет название карты"""

        with allure.step(f'Проверяет что название карты  - {name_cart}'):
            assert self.driver.find_element(*self.name_card_in_link).text == name_cart

    def check_img_card(self, img_kart_url: str):
        """Проверяет ссылку на изображение карты"""

        with allure.step(f'Проверяет ссылку на изображение карты'):
            assert self.driver.find_element(*self.img_card_in_link).get_attribute("src") == img_kart_url
