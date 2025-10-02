import pytest
import allure
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from settings import settings
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage


def create_chrome_driver():
    """Создать Chrome драйвер"""
    chrome_options = Options()

    if settings.HEADLESS:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"WebDriver Manager failed: {e}. Using system ChromeDriver...")
        driver = webdriver.Chrome(options=chrome_options)

    return driver


def create_firefox_driver():
    """Создать Firefox драйвер"""
    firefox_options = webdriver.FirefoxOptions()

    if settings.HEADLESS:
        firefox_options.add_argument("--headless")

    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"WebDriver Manager failed: {e}. Using system GeckoDriver...")
        driver = webdriver.Firefox(options=firefox_options)

    return driver


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации драйвера"""
    browser = settings.BROWSER.lower()

    if browser == "chrome":
        driver_instance = create_chrome_driver()
    elif browser == "firefox":
        driver_instance = create_firefox_driver()
    elif browser == "edge":
        try:
            service = Service(EdgeChromiumDriverManager().install())
            driver_instance = webdriver.Edge(service=service)
        except Exception as e:
            print(f"WebDriver Manager failed: {e}. Using system EdgeDriver...")
            driver_instance = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver_instance.implicitly_wait(settings.IMPLICIT_WAIT)
    driver_instance.maximize_window()

    yield driver_instance

    try:
        driver_instance.quit()
    except Exception as e:
        print(f"Error closing driver: {e}")


class TestLabirintUI:
    """UI тесты для сайта Лабиринт"""

    @allure.feature("Поиск книг")
    @allure.story("Поиск существующей книги")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_existing_book(self, driver):
        """Тест поиска существующей книги"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            assert "Лабиринт" in driver.title, "Главная страница не загрузилась"

        with allure.step("Выполнить поиск книги"):
            main_page.search_book(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить результаты поиска"):
            search_page.wait.until(
                lambda d: search_page.get_search_results_count() > 0 or
                          search_page.is_no_results_message_displayed()
            )

            results_count = search_page.get_search_results_count()
            assert results_count > 0, "Не найдено ни одной книги"

            book_titles = search_page.get_book_titles()
            assert len(book_titles) > 0, "Не удалось получить названия книг"

    @allure.feature("Поиск книг")
    @allure.story("Поиск несуществующей книги")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_book(self, driver):
        """Тест поиска несуществующей книги"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск несуществующей книги"):
            main_page.search_book("NonexistentBook12345XYZ")

        with allure.step("Проверить сообщение об отсутствии результатов"):
            search_page.wait.until(
                lambda d: search_page.is_no_results_message_displayed() or
                          search_page.get_search_results_count() == 0
            )

            no_results = (search_page.is_no_results_message_displayed() or
                          search_page.get_search_results_count() == 0)
            assert no_results, "Не отображается сообщение об отсутствии результатов"

    @allure.feature("Корзина")
    @allure.story("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_book_to_cart(self, driver):
        """Тест добавления книги в корзину"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск книги"):
            main_page.search_book(settings.TEST_BOOK_TITLE)

        with allure.step("Добавить первую книгу в корзину"):
            initial_cart_count = search_page.get_cart_items_count()

            if search_page.get_search_results_count() > 0:
                search_page.add_first_book_to_cart()

                search_page.wait.until(
                    lambda d: search_page.get_cart_items_count() != initial_cart_count
                )

                assert search_page.get_cart_items_count() != initial_cart_count, \
                    "Счетчик корзины не обновился"
            else:
                pytest.skip("Нет книг для добавления в корзину")

    @allure.feature("Корзина")
    @allure.story("Очистка корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_clear_cart(self, driver):
        """Тест очистки корзины"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск книги"):
            main_page.search_book(settings.TEST_BOOK_TITLE)

        with allure.step("Добавить книгу в корзину"):
            if search_page.get_search_results_count() > 0:
                search_page.add_first_book_to_cart()
                search_page.wait.until(
                    lambda d: search_page.get_cart_items_count() > 0
                )
            else:
                pytest.skip("Нет книг для добавления в корзину")

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        with allure.step("Очистить корзину"):
            cart_items_before = cart_page.get_cart_items_count()
            if cart_items_before > 0:
                cart_page.clear_cart()

                cart_page.wait.until(
                    lambda d: cart_page.is_cart_empty() or
                              cart_page.get_cart_items_count() == 0
                )

        with allure.step("Проверить, что корзина пуста"):
            assert cart_page.is_cart_empty() or cart_page.get_cart_items_count() == 0, \
                "Корзина не пуста после очистки"

    @allure.feature("Навигация")
    @allure.story("Переход в раздел книг")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_to_books_section(self, driver):
        """Тест навигации по разделам сайта"""
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Перейти в раздел книг"):
            main_page.go_to_books_section()

        with allure.step("Проверить URL страницы"):
            current_url = main_page.get_current_url()
            assert "/books/" in current_url, f"Не удалось перейти в раздел книг. Текущий URL: {current_url}"

    @allure.feature("Поиск книг")
    @allure.story("Поиск по автору")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_author(self, driver):
        """Тест поиска книг по автору"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск по автору"):
            main_page.search_book(settings.TEST_BOOK_AUTHOR)

        with allure.step("Проверить результаты поиска"):
            search_page.wait.until(
                lambda d: search_page.get_search_results_count() > 0 or
                          search_page.is_no_results_message_displayed()
            )

            results_count = search_page.get_search_results_count()
            assert results_count > 0, "Не найдено ни одной книги автора"