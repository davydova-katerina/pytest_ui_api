import requests
import allure
import time
from settings import settings


class APIHelper:
    """Класс для работы с API"""

    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        # Устанавливаем реалистичные заголовки
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # Добавляем задержку между запросами чтобы избежать блокировки
        self.last_request_time = 0
        self.request_delay = 2  # секунды

    def _make_request(self, method, url, **kwargs):
        """Вспомогательный метод для выполнения запросов с задержкой"""
        # Добавляем задержку между запросами
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_delay:
            time.sleep(self.request_delay - time_since_last_request)

        try:
            response = self.session.request(method, url, **kwargs)
            self.last_request_time = time.time()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            # Создаем mock response с ошибкой
            mock_response = requests.Response()
            mock_response.status_code = 0
            mock_response._content = str(e).encode()
            return mock_response

    @allure.step("API: Поиск книг по запросу: {query}")
    def search_books(self, query):
        """Поиск книг через API"""
        url = f"{self.base_url}/search/"
        params = {
            'st': query,
            'available': 1
        }
        return self._make_request('GET', url, params=params, timeout=10)

    @allure.step("API: Получить информацию о книге по ISBN: {isbn}")
    def get_book_info(self, isbn):
        """Получить информацию о книге по ISBN"""
        url = f"{self.base_url}/books/{isbn}/"
        return self._make_request('GET', url, timeout=10)

    @allure.step("API: Проверить доступность сайта")
    def check_availability(self):
        """Проверить доступность сайта"""
        return self._make_request('GET', self.base_url, timeout=10)

    @allure.step("API: Проверить здоровье сайта")
    def health_check(self):
        """Проверить здоровье сайта - упрощенная версия"""
        try:
            response = self._make_request('GET', self.base_url, timeout=5)
            return response is not None
        except:
            return False