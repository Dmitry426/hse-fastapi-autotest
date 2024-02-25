## Описание проекта

Проект разработан с целью проведения автоматизированного тестирования проектов, 
созданных с использованием фреймворка FastAPI на кафедре компьютерных наук Высшей Школы Экономики.
Для сквозного тестирования используется openapi.json схема.
Схема находится в самом приложении по пути ` hse_fastapi_autotest/config/openapi.json`
и может быть отредактирована/заменена как в среде разработки, так и уже в установленном пакете.
На основе этой схемы формируется сквозной тест приложения, 
потенциально схема может быть сколько угодно сложной и тест формируется по каждому указному пути и методу.
Также кроме сквозных тестов запускаются 2 статических теста (pylint и flake8) и тест на "мусорные" директории.
Результаты тестов записываются в качестве подробных html репортов в загруженный репозиторий студента 
(`/tmp/tested_repos/<имя репозитория студента >`), также результаты тестирования выводятся в stdout.

## Запуск приложения

### Разработка

Для запуска приложения в среде разработки доступен вариант запуска напрямую через `python`

#### Python Runner

```bash
 python3 hse_fastapi_autotest/cmd/commands.py
```

Энрипоинты для импорта и использования в других
приложениях находятся в сервисном слое :` hse_fastapi_autotest/services/testing_services.py`

### Сборка

Собрать пакет можно выполнив команду

```bash
  make dist
```

### Консольные команды

После установки пакета и в среде разработки доступны консольные команды
Посмотреть список доступных параметров можно

```bash
  fast_api_test --help 
```

### Перед началом работы

```bash
make dev
```

Это позволит проверить внесённые изменения до их сохранения.

### Зависимости

Управлением зависимостями занимается утилита `poetry`. \
Перечень зависимостей находится в файле `pyproject.toml`. \
Инструкция по настройке poetry-окружения для
pyCharm [здесь](https://www.jetbrains.com/help/pycharm/poetry.html).

Для добавления зависимости достаточно написать `poetry add requests`, утилита сама подберёт версию,
не конфликтующую с текущими зависимостями. \
Зависимости с точными версиями фиксируются в файл `poetry.lock`. \
Для получения дерева зависимостей можно воспользоваться командой `poetry show --tree`. Остальные
команды доступны в официальной документации к утилите.

