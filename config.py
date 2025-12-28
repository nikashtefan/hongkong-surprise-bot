"""Конфигурация бота для сюрприза с поездкой в Гонконг."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8563669117:AAGkW_cchbmLwq46yxlwftWCTBZA7aYjjGU")

# Правильные ответы
CORRECT_TRACK_NUMBER = "14012010"

# Информация о поездке
TRIP_INFO = {
    "dates": "7-13 января 2025",
    "cities": "Шанхай → Гонконг",
    "shanghai_dates": "7-10 января",
    "hongkong_dates": "10-13 января",
}

# Пути
BASE_DIR = Path(__file__).parent



