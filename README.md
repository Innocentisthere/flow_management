# 📘 Инструкция по запуску проекта

# 🔧 Установка зависимостей

Скачайте проект
```bash
gti clone https://github.com/Innocentisthere/flow_management.git
```

Перейдите в папку проекта
```bash
cd flow_management
```

Убедитесь, что у вас установлен **Python 3.10+** и **pip**. Затем выполните следующие команды:

```bash
# Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Установка зависимостей
pip install -r requirements.txt
```

# Настройка БД
#### По умолчанию используется SQLite. Убедитесь, что в файле settings.py указано:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
#### Инициализируйте базу данных:
```bash
python manage.py migrate
```

#### Опционально: создайте суперпользователя для доступа в админ-панель:
```bash
python manage.py createsuperuser
```

# Запуск веб-приложения
```bash
python manage.py runserver
```
### Приложение доступно по адресу
http://127.0.0.1:8000/flow/
