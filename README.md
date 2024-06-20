## АРТ Live Plus - Хранилище Документов

Автотесты для проекта "Хранилище документов".

Для локального запуска необходим Python версии 3.8 и выше.

При первом запуске надо создать и активировать виртуальное окружение:

```angular2html
python3 -m venv env
```
```angular2html
source env/bin/activate
```

Установить зависимости проекта:

```angular2html
pip3 install -r requirements.txt
```

Запуск тестов:

```angular2html
pytest
```

Логирование реализовано через пакет logging

```angular2html
Подробнее: https://docs.python.org/3/library/logging.html
```