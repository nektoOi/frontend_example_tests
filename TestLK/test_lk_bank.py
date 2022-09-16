from PageObject import BonusProgram
import configparser
import allure



config = configparser.ConfigParser()
config.read("settings.ini", "utf8")
domen_bank = config['bank'].get('domen')
balance_total_first_cart = config['bank'].get('balance_total_first_cart')


class TestBonusnieProgrammi:
    @allure.story(
        f"Переход в бонусные порграммы, ожидаем перейти на страницу 'https://{domen_bank}/programs'")
    def test_open_bonus_brogram(self, initWebDriver, auth):
        self.driver = initWebDriver
        self.url = auth
        initWebDriver.get(auth)
        initWebDriver.get(auth)
        self.driver.execute_script("document.body.style.transform = 'scale(0.5)'")
        programm_page = BonusProgram.BonusProgram(initWebDriver)

        programm_page.click_on_bonus_program_in_menu()

    @allure.story("Проверка бонусной Программы 36.6")
    def test_program_36_6(self, initWebDriver, auth):
        self.driver = initWebDriver
        self.url = auth
        initWebDriver.get(auth)
        initWebDriver.get(auth)
        self.driver.execute_script("document.body.style.transform = 'scale(0.5)'")
        programm_page = BonusProgram.BonusProgram(initWebDriver)

        programm_page.click_on_bonus_program_in_menu()
        programm_page.click_on_program_36_6()
        programm_page.check_name_program_on_page('Клуб 36,6')
        programm_page.balance_program_not_found()
        programm_page.check_name_balance('Авторизуйте программу')

    @allure.story("Проверка бонусной Программы Кэшбэк рубли")
    def test_program_kesh_rubli(self, initWebDriver, auth):
        self.driver = initWebDriver
        self.url = auth
        initWebDriver.get(auth)
        initWebDriver.get(auth)
        self.driver.execute_script("document.body.style.transform = 'scale(0.5)'")
        programm_page = BonusProgram.BonusProgram(initWebDriver)

        programm_page.click_on_bonus_program_in_menu()
        programm_page.click_on_program_kesh_rubli()
        programm_page.check_name_program_on_page('Кэшбэк-рубли')
        assert str(balance_total_first_cart) in str(programm_page.balance_program_found()), \
            str(balance_total_first_cart)
        programm_page.check_name_balance('Кэшбэк-рублей')

