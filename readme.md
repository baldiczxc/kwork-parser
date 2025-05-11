# Kwork-Parser

Асинхронный парсер новых заказов с kwork.ru  
Уведомляет о них в заданный Telegram-канал.

Telegram-канал: https://t.me/kworkneworders

## Готовимся к запуску
```bash
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Укажите в .env токен бота & ID канала, куда будут отправляться уведомления, ID
категорий, которые нужно парсить с kwork. Их можно найти в ссылке - https://kwork.ru/projects?fc=39.
Здесь 39 - ID категории.

## Запуск (из корня проекта)
```bash
python main.py
```
