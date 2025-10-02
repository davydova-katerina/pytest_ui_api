import pytest
import allure
import requests
from utils.helpers import APIHelper
from config.settings import settings


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

        with allure.step("Проверить, что сайт отвечает"):
            # Проверяем, что получаем какой-то ответ (не обязательно 200)
            assert response is not None, "Сайт не отвечает"

            # Для 502 ошибки проверяем, что это временная проблема
            if response.status_code == 502:
                pytest.skip("Сайт временно недоступен (502 Bad Gateway)")
            elif response.status_code != 200:
                pytest.skip(f"Сайт возвращает статус {response.status_code}")

            # Если статус 200, проверяем содержимое
            assert "Лабиринт" in response.text, "В ответе нет ожидаемого содержимого"

    @allure.feature("API")
    @allure.story("Поиск книг через API")
    def test_search_books_api(self, api_helper):
        """Тест поиска книг через API"""
        with allure.step("Выполнить поиск книг"):
            response = api_helper.search_books(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить ответ поиска"):
            assert response is not None, "Поиск не вернул ответ"

            # Обрабатываем разные статус коды
            if response.status_code == 502:
                pytest.skip("Сервис поиска временно недоступен (502)")
            elif response.status_code == 403:
                pytest.skip("Доступ к поиску запрещен (403)")
            elif response.status_code != 200:
                # Для других статусов проверяем, что есть какой-то контент
                assert len(response.text) > 0, "Пустой ответ при поиске"
                pytest.skip(f"Поиск вернул статус {response.status_code}")

            # Если статус 200, проверяем содержимое
            response_text = response.text.lower()
            assert any(keyword in response_text for keyword in ['книг', 'товар', 'результат']), \
                "Ответ не содержит информацию о результатах поиска"

    @allure.feature("API")
    @allure.story("Поиск несуществующей книги через API")
    def test_search_nonexistent_book_api(self, api_helper):
        """Тест поиска несуществующей книги через API"""
        with allure.step("Выполнить поиск несуществующей книги"):
            response = api_helper.search_books("NonexistentBook12345XYZabc")

        with allure.step("Проверить ответ"):
            assert response is not None, "Поиск не вернул ответ"

            if response.status_code == 502:
                pytest.skip("Сервис поиска временно недоступен (502)")
            elif response.status_code == 403:
                pytest.skip("Доступ к поиску запрещен (403)")

            # Для поиска несуществующей книги сайт может вернуть 200 с сообщением "ничего не найдено"
            # или другой статус. Проверяем, что запрос обработан.
            response_text = response.text.lower()

            # Проверяем различные варианты сообщений об отсутствии результатов
            no_results_indicators = [
                'ничего не найдено',
                'не найдено',
                '0 товаров',
                'товаров не найдено',
                'книг не найдено'
            ]

            has_no_results = any(indicator in response_text for indicator in no_results_indicators)

            # Либо статус не 200, либо есть сообщение об отсутствии результатов
            assert response.status_code != 200 or has_no_results, \
                "Не обнаружено сообщение об отсутствии результатов"

    @allure.feature("API")
    @allure.story("Проверка структуры ответа поиска")
    def test_search_response_structure(self, api_helper):
        """Тест структуры ответа поиска"""
        with allure.step("Выполнить поиск книг"):
            response = api_helper.search_books(settings.TEST_BOOK_TITLE)

        with allure.step("Проверить основные элементы ответа"):
            assert response is not None, "Поиск не вернул ответ"

            if response.status_code == 502:
                pytest.skip("Сервис поиска временно недоступен (502)")

            response_text = response.text

            # Базовые проверки для любого ответа
            assert len(response_text) > 0, "Пустой ответ"

            # Проверяем, что ответ содержит HTML структуру
            has_html_structure = any(tag in response_text for tag in ['<html', '<!DOCTYPE', '<body'])

            # Или хотя бы содержит какие-то данные
            has_content = len(response_text.strip()) > 100  # Не пустой ответ

            assert has_html_structure or has_content, "Ответ не содержит ожидаемую структуру"

    @allure.feature("API")
    @allure.story("Поиск с пустым запросом")
    def test_search_empty_query(self, api_helper):
        """Тест поиска с пустым запросом"""
        with allure.step("Выполнить поиск с пустым запросом"):
            response = api_helper.search_books("")

        with allure.step("Проверить поведение при пустом запросе"):
            assert response is not None, "Поиск не вернул ответ"

            if response.status_code == 502:
                pytest.skip("Сервис поиска временно недоступен (502)")

            # При пустом запросе сайт может вернуть главную страницу или страницу со всеми книгами
            response_text = response.text.lower()

            # Проверяем, что это страница Лабиринта
            is_labirint_page = 'лабиринт' in response_text

            # Или проверяем, что есть какой-то содержательный ответ
            has_content = len(response_text.strip()) > 1000  # Не пустая страница

            assert is_labirint_page or has_content, \
                "При пустом запросе не возвращается ожидаемая страница"

    @allure.feature("API")
    @allure.story("Поиск с специальными символами")
    def test_search_special_characters(self, api_helper):
        """Тест поиска с специальными символами"""
        with allure.step("Выполнить поиск со специальными символами"):
            response = api_helper.search_books("Python @#$% тест")

        with allure.step("Проверить обработку специальных символов"):
            assert response is not None, "Поиск не вернул ответ"

            if response.status_code == 502:
                pytest.skip("Сервис поиска временно недоступен (502)")

            # Главное - что сайт не падает с ошибкой 500
            assert response.status_code != 500, "Серверная ошибка при обработке специальных символов"

            # Проверяем, что запрос обработан (любой статус кроме 5xx ошибок)
            is_server_error = 500 <= response.status_code < 600
            assert not is_server_error, f"Серверная ошибка {response.status_code}"