from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class CartPage(BasePage):
    """Класс для работы с корзиной."""

    # Локаторы
    CART_ITEMS = (By.CSS_SELECTOR, "div.cart-item")
    ITEM_TITLE = (By.CSS_SELECTOR, "a.product-title")
    ITEM_PRICE = (By.CSS_SELECTOR, "span.price-val")
    TOTAL_PRICE = (By.CSS_SELECTOR, "div.total-price")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "div.cart-empty")
    DELETE_ITEM_BUTTON = (By.CSS_SELECTOR, "a.btn-action-delete")

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        """Получить количество товаров в корзине."""
        try:
            elements = self.driver.find_elements(*self.CART_ITEMS)
            return len(elements)
        except Exception:
            return 0

    @allure.step("Получить названия товаров в корзине")
    def get_cart_item_titles(self):
        """Получить список названий товаров в корзине."""
        titles = []
        try:
            elements = self.driver.find_elements(*self.ITEM_TITLE)
            for element in elements:
                titles.append(element.text.strip())
        except Exception:
            pass
        return titles

    @allure.step("Получить общую стоимость корзины")
    def get_total_price(self):
        """Получить общую стоимость товаров в корзине."""
        try:
            element = self.find_element(self.TOTAL_PRICE)
            return element.text.strip()
        except Exception:
            return "0 ₽"

    @allure.step("Удалить все товары из корзины")
    def clear_cart(self):
        """Удалить все товары из корзины."""
        while self.get_cart_items_count() > 0:
            self.click(self.DELETE_ITEM_BUTTON)
            self.wait.until(
                lambda driver: self.get_cart_items_count() == 0
            )

    @allure.step("Проверить, пуста ли корзина")
    def is_cart_empty(self):
        """Проверить, отображается ли сообщение о пустой корзине."""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)