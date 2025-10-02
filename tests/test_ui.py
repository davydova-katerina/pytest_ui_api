import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from settings import settings
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации драйвера."""
    chrome_options = Options()

    if settings.HEADLESS:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.implicitly_wait(settings.IMPLICIT_WAIT)

    yield driver_instance

    try:
        driver_instance.quit()
    except Exception as e:
        print(f"Error closing driver: {e}")


class TestLabirintUI:
    """UI тесты для сайта Лабиринт."""

    @allure.feature("Поиск книг")
    @allure.story("Поиск существующей книги")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_existing_book(self, driver):
        """Тест поиска существующей книги."""
        main_page = MainPage(driver)
        search_page = SearchPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open()
            assert "Лабиринт" in driver.title

        with allure.step("Выполнить поиск книги"):
            main_page.search_book(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить результаты поиска"):
            search_page.wait.until(
                lambda d: (
                        search_page.get_search_results_count() > 0 or
                        search_page.is_no_results_message_displayed()
                )
            )

            results_count = search_page.get_search_results_count()
            assert results_count > 0, "Не найдено ни одной книги"