import pytest
import allure
import requests
from helpers import APIHelper
from settings import settings


class TestLabirintAPI:
    """API тесты для сайта Лабиринт"""

    @pytest.fixture
    def api_helper(self):
        return APIHelper()

    @allure.feature("API")
    @allure.story("Проверка доступности сайта")
    def test_site_availability(self, api_helper):
        """Тест доступности сайта"""
        with allure.step("Отправить запрос к главной странице"):
            response = api_helper.check_availability()

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Сайт недоступен. Статус: {response.status_code}"

        with allure.step("Проверить содержимое ответа"):
            assert "Лабиринт" in response.text, "В ответе нет ожидаемого содержимого"

    @allure.feature("API")
    @allure.story("Поиск книг через API")
    def test_search_books_api(self, api_helper):
        """Тест поиска книг через API"""
        with allure.step("Выполнить поиск книг"):
            response = api_helper.search_books(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ошибка поиска. Статус: {response.status_code}"

        with allure.step("Проверить содержимое ответа"):
            assert settings.TEST_BOOK_TITLE in response.text, \
                "В ответе нет упоминания искомой книги"
            assert "книг" in response.text, "Ответ не содержит информацию о книгах"

    @allure.feature("API")
    @allure.story("Поиск несуществующей книги через API")
    def test_search_nonexistent_book_api(self, api_helper):
        """Тест поиска несуществующей книги через API"""
        with allure.step("Выполнить поиск несуществующей книги"):
            response = api_helper.search_books("NonexistentBook12345")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ошибка поиска. Статус: {response.status_code}"

        with allure.step("Проверить сообщение об отсутствии результатов"):
            # На сайте Лабиринт при отсутствии результатов обычно показывается сообщение
            assert "ничего не найдено" in response.text.lower() or \
                   "0 товаров" in response.text, \
                "Не отображается сообщение об отсутствии результатов"

    @allure.feature("API")
    @allure.story("Проверка структуры ответа поиска")
    def test_search_response_structure(self, api_helper):
        """Тест структуры ответа поиска"""
        with allure.step("Выполнить поиск книг"):
            response = api_helper.search_books(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить основные элементы ответа"):
            response_text = response.text

            # Проверяем наличие ключевых элементов на странице
            assert '<html' in response_text, "Ответ не является HTML страницей"
            assert '</body>' in response_text, "Ответ не содержит закрывающий тег body"
            assert 'search-field' in response_text, "Ответ не содержит поле поиска"

    @allure.feature("API")
    @allure.story("Поиск с пустым запросом")
    def test_search_empty_query(self, api_helper):
        """Тест поиска с пустым запросом"""
        with allure.step("Выполнить поиск с пустым запросом"):
            response = api_helper.search_books("")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ошибка поиска. Статус: {response.status_code}"

        with allure.step("Проверить поведение при пустом запросе"):
            # При пустом запросе сайт обычно показывает главную страницу или все книги
            assert "Лабиринт" in response.text, \
                "При пустом запросе не возвращается ожидаемая страница"

    @allure.feature("API")
    @allure.story("Поиск с специальными символами")
    def test_search_special_characters(self, api_helper):
        """Тест поиска с специальными символами"""
        with allure.step("Выполнить поиск со специальными символами"):
            response = api_helper.search_books("Python @#$%")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ошибка поиска. Статус: {response.status_code}"

        with allure.step("Проверить обработку специальных символов"):
            # Сайт должен корректно обрабатывать специальные символы
            assert response.status_code == 200, \
                "Сайт не смог обработать запрос со специальными символами"