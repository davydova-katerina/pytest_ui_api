from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class MainPage(BasePage):
    """Класс для работы с главной страницей Лабиринта"""

    # Локаторы
    SEARCH_INPUT = (By.ID, "search-field")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.b-header-b-search-e-btn")
    CART_BUTTON = (By.CSS_SELECTOR, "a.b-header-b-personal-e-link.top-link-main.top-link-main_cart")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a.js-b-autofade-wrap")
    BOOKS_MENU = (By.CSS_SELECTOR, "a[href='/books/']")

    @allure.step("Выполнить поиск книги: {query}")
    def search_book(self, query):
        """Выполнить поиск книги"""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Перейти в корзину"""
        self.click(self.CART_BUTTON)

    @allure.step("Перейти в раздел книг")
    def go_to_books_section(self):
        """Перейти в раздел книг"""
        self.click(self.BOOKS_MENU)

    @allure.step("Получить текст поля поиска")
    def get_search_input_text(self):
        """Получить текст из поля поиска"""
        element = self.find_element(self.SEARCH_INPUT)
        return element.get_attribute("value")