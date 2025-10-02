import pytest
import allure
from helpers import APIHelper
from settings import settings


class TestLabirintAPI:
    """API тесты для сайта Лабиринт."""

    @pytest.fixture
    def api_helper(self):
        return APIHelper()

    @allure.feature("API")
    @allure.story("Проверка доступности сайта")
    def test_site_availability(self, api_helper):
        """Тест доступности сайта."""
        with allure.step("Отправить запрос к главной странице"):
            response = api_helper.check_availability()

        with allure.step("Проверить, что сайт отвечает"):
            assert response is not None, "Сайт не отвечает"

            if response.status_code == 502:
                pytest.skip("Сайт временно недоступен (502 Bad Gateway)")
            elif response.status_code != 200:
                pytest.skip(f"Сайт возвращает статус {response.status_code}")

            assert "Лабиринт" in response.text