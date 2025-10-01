import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Класс для хранения настроек проекта"""

    # URL сайта
    BASE_URL = "https://www.labirint.ru"

    # API endpoints
    API_BASE_URL = "https://www.labirint.ru"
    SEARCH_API_URL = f"{BASE_URL}/search/"

    # Тестовые данные
    TEST_BOOK_TITLE = "Python"
    TEST_BOOK_AUTHOR = "Марк Лутц"
    TEST_INVALID_ISBN = "0000000000"

    # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    TIMEOUT = 10

    # Настройки ожидания
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20

    # Настройки API тестов
    API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "2"))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

    # Настройки для обработки 502 ошибок
    SKIP_502_ERRORS = os.getenv("SKIP_502_ERRORS", "True").lower() == "true"


settings = Settings()