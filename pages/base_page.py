from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
from settings import settings


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver):
        """Инициализация базовой страницы."""
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
        self.base_url = settings.BASE_URL

    @allure.step("Открыть страницу {url}")
    def open(self, url=""):
        """Открыть указанную страницу."""
        full_url = f"{self.base_url}{url}" if url else self.base_url
        self.driver.get(full_url)

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator, timeout=None):
        """Найти элемент с ожиданием."""
        wait = self.wait if timeout is None else WebDriverWait(
            self.driver, timeout
        )
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Найти кликабельный элемент {locator}")
    def find_clickable_element(self, locator, timeout=None):
        """Найти кликабельный элемент."""
        wait = self.wait if timeout is None else WebDriverWait(
            self.driver, timeout
        )
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator):
        """Кликнуть на элемент."""
        element = self.find_clickable_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def type_text(self, locator, text):
        """Ввести текст в поле."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        """Получить текст элемента."""
        element = self.find_element(locator)
        return element.text

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator, timeout=None):
        """Проверить видимость элемента."""
        try:
            wait = self.wait if timeout is None else WebDriverWait(
                self.driver, timeout
            )
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL."""
        return self.driver.current_url