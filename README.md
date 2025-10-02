# pytest_ui_api

## Проект автоматизации тестирования сайта Лабиринт

### Шаги
- Склонировать проект 'git clone https://github.com/davydova-katerina/pytest_ui_api.git'
- Установить все зависимости 'python -m pip install -r requirements.txt'
- Запустить тесты 'pytest'

### Стек:
- pytest
- selenium
- webdriver manager
- requests
- allure
- configparser
- json

## Структура проекта
labirint_test_project/
├── config/ # Конфигурационные файлы
├── pages/ # Page Object модели
├── tests/ # Тесты (UI и API)
├── utils/ # Вспомогательные утилиты
├── requirements.txt # Зависимости проекта
├── pytest.ini # Конфигурация pytest
└── README.md # Документация

### Полезные ссылки
- [Генератор файла .gitignore] (https://www.toptal.com/developers/gitignore)
- [Про configparse] (https://docs.python.org/3/library/configparser.html)
- [Про pip freeze] (https://pip.pypa.io/en/stable/cli/pip_freeze/)

### Команды для запуска тестов

- # Запуск UI тестов
- pytest tests/test_ui.py -v
- # Запуск API тестов
- pytest tests/test_api.py -v