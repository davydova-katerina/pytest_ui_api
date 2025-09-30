import requests
import allure
from settings import settings


class APIHelper:
    """Класс для работы с API"""

    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        # Устанавливаем заголовки как у браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*'
        })

    @allure.step("API: Поиск книг по запросу: {query}")
    def search_books(self, query):
        """Поиск книг через API"""
        url = f"{self.base_url}/search/"
        params = {
            'st': query,
            'available': 1
        }
        response = self.session.get(url, params=params)
        return response

    @allure.step("API: Получить информацию о книге по ISBN: {isbn}")
    def get_book_info(self, isbn):
        """Получить информацию о книге по ISBN"""
        url = f"{self.base_url}/books/{isbn}/"
        response = self.session.get(url)
        return response

    @allure.step("API: Проверить доступность сайта")
    def check_availability(self):
        """Проверить доступность сайта"""
        response = self.session.get(self.base_url)
        return response