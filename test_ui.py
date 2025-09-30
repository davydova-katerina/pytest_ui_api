import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from settings import settings
from main_page import MainPage
from search_page import SearchPage
from cart_page import CartPage


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации драйвера"""
    chrome_options = Options()
    if settings.HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(settings.IMPLICIT_WAIT)

    yield driver
    driver.quit()


class TestLabirintUI:
    """UI тесты для сайта Лабиринт"""

    @allure.feature("Поиск книг")
    @allure.story("Поиск существующей книги")
    def test_search_existing_book(self, driver):
        """Тест поиска существующей книги"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск книги"):
            main_page.search_book(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить результаты поиска"):
            results_count = search_page.get_search_results_count()
            assert results_count > 0, "Не найдено ни одной книги"

            book_titles = search_page.get_book_titles()
            assert any(settings.TEST_BOOK_TITLE.lower() in title.lower()
                       for title in book_titles), "Не найдена книга с указанным названием"

    @allure.feature("Поиск книг")
    @allure.story("Поиск несуществующей книги")
    def test_search_nonexistent_book(self, driver):
        """Тест поиска несуществующей книги"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск несуществующей книги"):
            main_page.search_book("NonexistentBook12345")

        with allure.step("Проверить сообщение об отсутствии результатов"):
            assert search_page.is_no_results_message_displayed(), \
                "Не отображается сообщение об отсутствии результатов"

    @allure.feature("Корзина")
    @allure.story("Добавление книги в корзину")
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
            search_page.add_first_book_to_cart()

        with allure.step("Проверить обновление счетчика корзины"):
            search_page.wait.until(
                lambda driver: search_page.get_cart_items_count() > initial_cart_count
            )
            assert search_page.get_cart_items_count() > initial_cart_count, \
                "Счетчик корзины не обновился"

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        with allure.step("Проверить наличие книги в корзине"):
            cart_items = cart_page.get_cart_item_titles()
            assert len(cart_items) > 0, "Корзина пуста"

    @allure.feature("Корзина")
    @allure.story("Очистка корзины")
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
            search_page.add_first_book_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        with allure.step("Очистить корзину"):
            cart_page.clear_cart()

        with allure.step("Проверить, что корзина пуста"):
            assert cart_page.is_cart_empty(), "Корзина не пуста после очистки"

    @allure.feature("Навигация")
    @allure.story("Переход в раздел книг")
    def test_navigate_to_books_section(self, driver):
        """Тест навигации по разделам сайта"""
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Перейти в раздел книг"):
            main_page.go_to_books_section()

        with allure.step("Проверить URL страницы"):
            current_url = main_page.get_current_url()
            assert "/books/" in current_url, "Не удалось перейти в раздел книг"

    @allure.feature("Поиск книг")
    @allure.story("Поиск по автору")
    def test_search_by_author(self, driver):
        """Тест поиска книг по автору"""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Выполнить поиск по автору"):
            main_page.search_book(settings.TEST_BOOK_AUTHOR)

        with allure.step("Проверить результаты поиска"):
            results_count = search_page.get_search_results_count()
            assert results_count > 0, "Не найдено ни одной книги автора"

            book_titles = search_page.get_book_titles()
            # Проверяем, что в результатах есть книги указанного автора
            assert len(book_titles) > 0, "Не найдено книг указанного автора"