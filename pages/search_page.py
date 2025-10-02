from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time


class SearchPage(BasePage):
    """Класс для работы со страницей поиска."""

    # Обновленные локаторы
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div.product.need-watch, div.product-card")
    BOOK_TITLE = (By.CSS_SELECTOR, "a.product-title-link, a.product-card__title")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR,
                          "a.btn.buy-link.btn-primary, button.btn-buy")
    CART_COUNTER = (By.CSS_SELECTOR,
                    "span.b-header-b-personal-e-icon-count-m-cart, "
                    "span.basket-in-cart-a")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR,
                          "div.search-error, div.searchnoresults")
    SEARCH_TITLE = (By.CSS_SELECTOR, "h1.searchtitle")

    @allure.step("Получить количество результатов поиска")
    def get_search_results_count(self):
        """Получить количество найденных книг."""
        try:
            elements = self.driver.find_elements(*self.SEARCH_RESULTS)
            return len(elements)
        except Exception:
            return 0

    @allure.step("Получить заголовки найденных книг")
    def get_book_titles(self):
        """Получить список заголовков найденных книг."""
        titles = []
        try:
            elements = self.driver.find_elements(*self.BOOK_TITLE)
            for element in elements:
                if element.text.strip():
                    titles.append(element.text.strip())
        except Exception as e:
            print(f"Error getting book titles: {e}")
        return titles

    @allure.step("Добавить первую книгу в корзину")
    def add_first_book_to_cart(self):
        """Добавить первую найденную книгу в корзину."""
        try:
            buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
            if buttons:
                buttons[0].click()
                time.sleep(2)
                return True
        except Exception as e:
            print(f"Error adding to cart: {e}")
        return False

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        """Получить количество товаров в корзине."""
        try:
            element = self.find_element(self.CART_COUNTER, timeout=5)
            return int(element.text) if element.text.isdigit() else 0
        except Exception:
            return 0

    @allure.step("Проверить наличие сообщения 'нет результатов'")
    def is_no_results_message_displayed(self):
        """Проверить сообщение об отсутствии результатов."""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)

    @allure.step("Дождаться загрузки результатов поиска")
    def wait_for_search_results(self, timeout=10):
        """Дождаться загрузки результатов поиска."""
        try:
            self.wait.until(
                lambda d: (
                        self.get_search_results_count() > 0 or
                        self.is_no_results_message_displayed() or
                        self.is_element_visible(self.SEARCH_TITLE, timeout=5)
                )
            )
            return True
        except Exception:
            return False