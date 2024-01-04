import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Класс HomePage, представляющий домашнюю страницу
class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.contacts_link_locator = (By.XPATH, '//a[contains(@href, "contacts")]')
        self.banner_link_locator = (By.CSS_SELECTOR, 'a.sbisru-Contacts__logo-tensor')
        self.power_in_people_locator = (By.CSS_SELECTOR, '.tensor_ru-Index__card-title')
        self.image_wrappers_locator = (By.CSS_SELECTOR, '.tensor_ru-About__block3-image-wrapper')

    def open(self):
        # Открываем домашнюю страницу
        self.driver.get("https://sbis.ru/")

    def open_about_page(self):
        # Открываем страницу "О нас"
        self.driver.get("https://tensor.ru/about")
        WebDriverWait(self.driver, 30).until(EC.title_contains("О компании"))

    def go_to_contacts(self):
        # Кликаем по ссылке на страницу контактов
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.contacts_link_locator)
        ).click()

    def find_banner_link(self):
        # Находим ссылку на баннер
        banner_link = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.banner_link_locator)
        )
        return banner_link

    def find_power_in_people(self):
        power_in_people = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.power_in_people_locator)
        )
        return power_in_people

    def get_images_sizes(self):
        # Получаем размеры изображений в секции "Работаем"
        image_wrappers = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.image_wrappers_locator)
        )

        sizes = []
        for wrapper in image_wrappers:
            image = wrapper.find_element(By.TAG_NAME, 'img')
            size = (int(image.get_attribute("width")), int(image.get_attribute("height")))
            sizes.append(size)

        return sizes


# Фикстура для инициализации и закрытия браузера
@pytest.fixture(scope="module")
def browser():
    # Инициализация драйвера
    driver = webdriver.Chrome()
    yield driver
    # Закрытие браузера
    driver.quit()


# Тест для проверки раздела контакты
def test_contacts(browser):
    # Создаем экземпляр класса HomePage
    home_page = HomePage(browser)
    # Открываем домашнюю страницу
    home_page.open()

    # Кликаем по ссылке на страницу контактов
    home_page.go_to_contacts()

    # Проверяем, что открыта страница с контактами
    assert "Контакты" in home_page.driver.title

    # Находим ссылку на баннер
    banner_link = home_page.find_banner_link()
    # Проверяем, что баннер ведет на tensor.ru
    assert banner_link.get_attribute("href") == "https://tensor.ru/"

    # Кликаем по баннеру
    banner_link.click()
    # Переключаемся на новую вкладку
    browser.switch_to.window(browser.window_handles[-1])
    # Проверяем, что открыт сайт tensor.ru
    assert "tensor.ru" in browser.current_url

    # Находим блок "Сила в людях"
    power_in_people_block = home_page.find_power_in_people()
    # Проверяем, что блок "Сила в людях" найден
    assert power_in_people_block.is_displayed()


# Тест для проверки размеров изображений на странице "О нас"
def test_images_have_same_size(browser):
    # Создаем экземпляр класса AboutPage
    about_page = HomePage(browser)

    # Открываем страницу "О нас"
    about_page.open_about_page()
    # Получаем размеры изображений
    image_sizes = about_page.get_images_sizes()

    # Проверяем, что все изображения имеют одинаковые размеры
    assert all(size == image_sizes[0] for size in image_sizes), "Изображения в 'Работаем' имеют разный размер"

