from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class SearchPage(BasePage):
    """Класс для работы со страницей поиска"""

    # Локаторы
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div.product.need-watch")
    BOOK_TITLE = (By.CSS_SELECTOR, "a.product-title-link")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a.btn.buy-link.btn-primary")
    CART_COUNTER = (By.CSS_SELECTOR, "span.b-header-b-personal-e-icon-count-m-cart.basket-in-cart-a")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.search-error")

    @allure.step("Получить количество результатов поиска")
    def get_search_results_count(self):
        """Получить количество найденных книг"""
        try:
            elements = self.driver.find_elements(*self.SEARCH_RESULTS)
            return len(elements)
        except:
            return 0

    @allure.step("Получить заголовки найденных книг")
    def get_book_titles(self):
        """Получить список заголовков найденных книг"""
        titles = []
        try:
            elements = self.driver.find_elements(*self.BOOK_TITLE)
            for element in elements:
                titles.append(element.text.strip())
        except:
            pass
        return titles

    @allure.step("Добавить первую книгу в корзину")
    def add_first_book_to_cart(self):
        """Добавить первую найденную книгу в корзину"""
        if self.get_search_results_count() > 0:
            self.click(self.ADD_TO_CART_BUTTON)
            return True
        return False

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        """Получить количество товаров в корзине"""
        try:
            element = self.find_element(self.CART_COUNTER)
            return int(element.text)
        except:
            return 0

    @allure.step("Проверить наличие сообщения 'нет результатов'")
    def is_no_results_message_displayed(self):
        """Проверить отображение сообщения об отсутствии результатов"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE)