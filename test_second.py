import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SbisHomePage:
    def __init__(self, driver):
        self.driver = driver
        self.contacts_link_locator = (By.XPATH, '//a[contains(@href, "contacts")]')
        self.region_chooser_locator = (By.CLASS_NAME, 'sbis_ru-Region-Chooser')
        self.region_panel_locator = (By.CLASS_NAME, 'sbis_ru-Region-Panel')
        self.region_item_locator = (By.XPATH, '//span[@title="Камчатский край"]')
        self.region_info_locator = (By.CSS_SELECTOR, '.sbisru-Contacts__underline span')

    def open(self):
        self.driver.get("https://sbis.ru/")

    def go_to_contacts(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.contacts_link_locator)
        ).click()

    def change_region_to_kamchatka(self):
        kamchatka_region_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.region_chooser_locator)
        )
        kamchatka_region_button.click()

        # Ждем, пока появится панель с регионами
        region_panel = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.region_panel_locator)
        )

        # Находим и кликаем по элементу "Камчатский край"
        kamchatka_region_item = WebDriverWait(region_panel, 30).until(
            EC.element_to_be_clickable(self.region_item_locator)
        )
        kamchatka_region_item.click()


# Фикстура для инициализации и закрытия браузера
@pytest.fixture(scope="module")
def browser():
    # Инициализация драйвера
    driver = webdriver.Chrome()
    yield driver
    # Закрытие браузера
    driver.quit()


def test_go_to_contacts(browser):
    # Создаем экземпляр класса HomePage
    home_page = SbisHomePage(browser)
    # Открываем домашнюю страницу
    home_page.open()

    # Кликаем по ссылке на страницу контактов
    home_page.go_to_contacts()

    # Например, проверка наличия конкретной информации на странице контактов
    assert "Контакты" in home_page.driver.title


def test_check_region_info(browser):
    # Создаем экземпляр класса HomePage
    home_page = SbisHomePage(browser)
    # Открываем домашнюю страницу
    home_page.open()

    # Кликаем по ссылке на страницу контактов
    home_page.go_to_contacts()

    # Проверить наличие информации о регионе
    element_region_info = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(home_page.region_info_locator)
    )

    # Проверить, отображается ли информация о регионе на странице "Контакты"
    assert "Тюменская обл." in element_region_info.text


def test_find_partner_in_list(browser):
    # Создаем экземпляр класса HomePage
    home_page = SbisHomePage(browser)
    # Открываем домашнюю страницу
    home_page.open()

    # Кликаем по ссылке на страницу контактов
    home_page.go_to_contacts()

    # Найти "Тюмень" в списке партнеров
    partner_locator = (By.XPATH,
                       '//div[@id="contacts_list"]//div[contains(@class, "sbisru-Contacts-List__col")]/div['
                       'contains(text(), "Тюмень")]')
    partner_element = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(partner_locator)
    )

    # Проверить, что "Тюмень" присутствует в списке партнеров
    assert "Тюмень" in partner_element.text


def test_change_region_to_kamchatka(browser):
    # Создаем экземпляр класса HomePage
    home_page = SbisHomePage(browser)
    # Открываем домашнюю страницу
    home_page.open()

    # Кликаем по ссылке на страницу контактов
    home_page.go_to_contacts()
    home_page.change_region_to_kamchatka()

    # Ждем, пока загрузится страница (предполагаем, что заголовок - уникальный элемент)
    WebDriverWait(browser, 30).until(
        EC.title_contains("Камчатский край")
    )

    assert "Камчатский край" in home_page.driver.title
    assert "41-kamchatskij-kraj" in home_page.driver.current_url, "URL не соответствует ожидаемому"

    # Проверяем, что в элементе region_chooser_locator отображается "Камчатский край"
    region_chooser_text = home_page.driver.find_element(*home_page.region_chooser_locator).text
    assert "Камчатский край" in region_chooser_text, "Элемент не содержит 'Камчатский край'"

    # Найти "Камчатка" в списке партнеров
    partner_locator = (By.XPATH,
                       '//div[@id="contacts_list"]//div[contains(@class, "sbisru-Contacts-List__col")]/div['
                       'contains(text(), "Камчатка")]')
    partner_element = WebDriverWait(home_page.driver, 30).until(
        EC.visibility_of_element_located(partner_locator)
    )

    # Проверить, что "Камчатка" присутствует в списке партнеров
    assert "Камчатка" in partner_element.text
