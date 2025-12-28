#!/bin/bash

echo "🔄 Останавливаю все процессы бота..."
killall -9 python3 2>/dev/null
killall -9 Python 2>/dev/null
pkill -9 -f bot.py 2>/dev/null

echo "⏳ Жду 5 секунд..."
sleep 5

echo "🧹 Очищаю webhook..."
curl -s -X POST "https://api.telegram.org/bot8563669117:AAGkW_cchbmLwq46yxlwftWCTBZA7aYjjGU/deleteWebhook?drop_pending_updates=true"

echo ""
echo "⏳ Жду ещё 5 секунд..."
sleep 5

echo "🚀 Запускаю бота..."
cd /Users/nike/Documents/cursorchik/telegram-bot-project/hongkong_surprise_bot
python3 bot.py

echo ""
echo "✅ Бот должен работать!"
echo "Проверь в Telegram: напиши /start"


