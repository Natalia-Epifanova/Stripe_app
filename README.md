
# Реализация бэкенда с интеграцией Stripe API для обработки платежей.

Рабочее приложение: https://NataliaYep.pythonanywhere.com/

Административная панель: https://NataliaYep.pythonanywhere.com/admin/

Логин: ```admin```

Пароль: ```admin123```

## Быстрый запуск

### Локальная разработка с Docker

- Клонируйте репозиторий:

```git clone https://github.com/Natalia-Epifanova/Stripe_app.git```

```cd Stripe_app```

- Создайте файл ```.env``` на основе ```.env.example```:

- Запустите приложение:

```docker-compose up --build```

- В новом терминале выполните миграции:

```docker-compose exec web python manage.py migrate```

```docker-compose exec web python manage.py createsuperuser```

Приложение доступно по адресу: http://localhost:8000

### Локальная разработка без Docker
```python -m venv venv```

```venv\Scripts\activate ```

```pip install -r requirements.txt```

```python manage.py migrate```

```python manage.py createsuperuser```

```python manage.py runserver```

## API Endpoints
- Основные endpoints

GET ```/item/{id}/```

Возвращает HTML страницу с информацией о товаре

Содержит кнопку "Buy" для инициации платежа

GET ```/buy/{id}/```

Возвращает JSON с Stripe Session ID для товара

Выполняет запрос stripe.checkout.Session.create()

- Дополнительные endpoints (бонусные)

GET ```/order/{id}/```

Страница заказа с несколькими товарами

GET ```/create-payment-intent/{id}/```

Создает Stripe Payment Intent для товара

GET ```/create-order-payment-intent/{id}/```

Создает Stripe Payment Intent для заказа

## Поддержка валют
В зависимости от валюты товара используются соответствующие Stripe ключи:

- USD товары: STRIPE_PUBLIC_KEY_USD, STRIPE_SECRET_KEY_USD

- EUR товары: STRIPE_PUBLIC_KEY_EUR, STRIPE_SECRET_KEY_EUR

