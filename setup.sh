#!/bin/bash

# Скрипт автоматической настройки бота для новогоднего сюрприза
# Использование: ./setup.sh

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║        🎁 НАСТРОЙКА БОТА ДЛЯ НОВОГОДНЕГО СЮРПРИЗА 🎁         ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Проверка Python
echo "🔍 Проверяю Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден! Установи Python 3.8+"
    exit 1
fi
echo "✅ Python найден: $(python3 --version)"
echo ""

# Установка зависимостей для бота
echo "📦 Устанавливаю зависимости для бота..."
pip3 install -r requirements.txt
echo ""

# Установка зависимостей для генерации QR-кода
echo "📦 Устанавливаю библиотеки для QR-кода..."
pip3 install qrcode[pil] pillow
echo ""

# Проверка .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo ""
    echo "Тебе нужно создать бота через @BotFather в Telegram:"
    echo "1. Открой Telegram"
    echo "2. Найди @BotFather"
    echo "3. Отправь /newbot"
    echo "4. Следуй инструкциям"
    echo "5. Скопируй токен"
    echo ""
    read -p "Введи токен бота: " bot_token
    echo "BOT_TOKEN=$bot_token" > .env
    echo "✅ Файл .env создан!"
    echo ""
else
    echo "✅ Файл .env найден!"
    echo ""
fi

# Получение username бота
echo "📱 Теперь мне нужен username твоего бота"
echo "(Это то, что заканчивается на 'bot', например: hongkong_surprise_bot)"
echo ""
read -p "Введи username бота: " bot_username
echo ""

# Генерация QR-кода
echo "🎨 Генерирую QR-код..."
python3 generate_qr.py "$bot_username"
echo ""

# Финальные инструкции
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║                    ✅ ВСЁ ГОТОВО! ✅                          ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 ЧТО ДАЛЬШЕ:"
echo ""
echo "1️⃣  Запусти бота:"
echo "   python3 bot.py"
echo ""
echo "2️⃣  Распечатай открытку:"
echo "   gift_card_with_qr.png"
echo ""
echo "3️⃣  Протестируй бота:"
echo "   Найди его в Telegram и напиши /start"
echo ""
echo "4️⃣  Положи открытку в конверт и готово! 🎁"
echo ""
echo "📝 ВАЖНАЯ ИНФОРМАЦИЯ:"
echo "   • Трек-номер: 14012010"
echo "   • Ответ на загадку: Гонконг"
echo "   • Даты поездки: 7-13 января 2025"
echo ""
echo "🎄 С НОВЫМ ГОДОМ! Удачи с подарком! 🎊"
echo ""


