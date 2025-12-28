"""
Telegram бот-сюрприз для поездки в Гонконг 🎁
Квест для получения подарка с маркерами
"""

import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN, CORRECT_TRACK_NUMBER, TRIP_INFO

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Состояния разговора
(
    TRACK_NUMBER,
    DRAWING_QUESTION,
    ARTIST_PROOF,
    ARTIST_CHALLENGE,
    FINAL_REVEAL,
) = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало квеста - приветствие и проблема с доставкой."""
    user = update.effective_user
    
    await update.message.reply_text("🎨 Привет!")
    await asyncio.sleep(2)
    
    await update.message.reply_text("📦 Я бот службы доставки ArtExpress...")
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🤔 У нас возникла небольшая проблема с твоим заказом маркеров для рисования.\n\n"
        "Мне нужно уточнить некоторые детали!"
    )
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "📋 Для начала, введи трек-номер твоей посылки:\n\n"
        "💡 Подсказка: это важная дата в формате ДДММГГГГ"
    )
    
    return TRACK_NUMBER


async def check_track_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Проверка трек-номера."""
    track_number = update.message.text.strip()
    
    if track_number == CORRECT_TRACK_NUMBER:
        await update.message.reply_text("✅ Отлично! Посылка найдена!")
        await asyncio.sleep(2)
        
        await update.message.reply_text(
            "🎨 Теперь мне нужно задать тебе важный вопрос...\n\n"
            "Для чего тебе эти маркеры? Что ты будешь ими рисовать?\n\n"
            "Расскажи подробнее! 😊"
        )
        
        return DRAWING_QUESTION
    else:
        await update.message.reply_text(
            "❌ Неправильный трек-номер!\n\n"
            "💡 Подсказка: это дата в формате ДДММГГГГ\n"
            "Попробуй ещё раз:"
        )
        return TRACK_NUMBER


async def process_drawing_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа о рисовании."""
    user_answer = update.message.text
    context.user_data["drawing_answer"] = user_answer
    
    await update.message.reply_text(f"🤩 О, круто! {user_answer[:50]}...")
    await asyncio.sleep(3)
    
    await update.message.reply_text("🤔 Но есть сомнения...")
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "😰 На таможне сомневаются, что ты настоящий художник...\n\n"
        "Они требуют доказательства!"
    )
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🎨 Можешь ли ты доказать, что ты настоящий художник?\n\n"
        "Как ты это докажешь? Может, покажешь свои работы? "
        "Или расскажешь о своём опыте?\n\n"
        "Напиши, как ты можешь подтвердить, что умеешь рисовать! 😊"
    )
    
    return ARTIST_CHALLENGE


async def check_artist_challenge(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа о доказательстве художественных навыков."""
    user_answer = update.message.text
    context.user_data["artist_proof"] = user_answer
    
    await update.message.reply_text(f"👍 Звучит убедительно!")
    await asyncio.sleep(3)
    
    await update.message.reply_text("📞 Связываюсь с таможней...")
    await asyncio.sleep(3)
    
    await update.message.reply_text("⏳ Жду ответа...")
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "😓 Хм... Таможня говорит, что этого недостаточно.\n\n"
        "Они хотят проверить твои знания об искусстве!"
    )
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🧐 Давай проверим!\n\n"
        "Ответь на вопрос:\n\n"
        "Какой город называют 'Жемчужиной Востока' и где находятся "
        "самые высокие небоскрёбы Азии? 🏙️\n\n"
        "Подсказка: это город, где можно купить лучшие маркеры для художников! 😉"
    )
    
    return ARTIST_PROOF


async def check_artist_proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Проверка ответа о городе."""
    answer = update.message.text.lower().strip()
    
    # Принимаем разные варианты ответа
    correct_answers = ["гонконг", "hong kong", "hongkong", "хонгконг", "сянган"]
    
    if any(correct in answer for correct in correct_answers):
        await update.message.reply_text("🎉 Правильно! Это Гонконг!")
        await asyncio.sleep(2)
        
        await update.message.reply_text("🤔 Хм, интересное совпадение...")
        await asyncio.sleep(3)
        
        await update.message.reply_text("📍 Смотрю по трекингу...")
        await asyncio.sleep(3)
        
        await update.message.reply_text("😱 ОЙ!")
        await asyncio.sleep(2)
        
        await update.message.reply_text(
            "📦 Твои маркеры... они застряли именно в Гонконге!\n\n"
            "🚫 Таможня не пропускает их без личного присутствия получателя!"
        )
        await asyncio.sleep(3)
        
        # Переход к финальному откровению
        keyboard = [["🎁 Узнать подробности!"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        
        await update.message.reply_text(
            "🤷‍♂️ Похоже, тебе придётся лететь за ними самой...\n\n"
            "Но у меня есть для тебя новость! 😏",
            reply_markup=reply_markup,
        )
        
        return FINAL_REVEAL
    else:
        await update.message.reply_text(
            "🤔 Не совсем... Подумай ещё!\n\n"
            "💡 Подсказка: город в Китае, известный своими небоскрёбами "
            "и статусом международного финансового центра!"
        )
        return ARTIST_PROOF


async def final_reveal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Финальное откровение о поездке."""
    await update.message.reply_text(
        "🎊 СЮРПРИЗ! 🎊",
        reply_markup=ReplyKeyboardRemove(),
    )
    await asyncio.sleep(2)
    
    await update.message.reply_text("✈️ Ты летишь в настоящее путешествие!")
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🗺️ Маршрут:\n\n"
        f"📍 Шанхай ({TRIP_INFO['shanghai_dates']})\n"
        "🏙️ Один из крупнейших городов Китая\n"
        "🎭 Современная архитектура и древние храмы\n\n"
        "⬇️\n\n"
        f"📍 Гонконг ({TRIP_INFO['hongkong_dates']})\n"
        "🌃 Жемчужина Востока\n"
        "🎨 И да, здесь мы купим твои маркеры! 😄"
    )
    await asyncio.sleep(4)
    
    await update.message.reply_text(
        f"📅 Даты поездки: {TRIP_INFO['dates']}\n\n"
        "👥 Едем вместе: ты, я и мои друзья!\n\n"
        "🎒 Это будет незабываемое приключение!"
    )
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🎁 С Новым Годом! 🎄\n\n"
        "Готовься к путешествию! Нам предстоит:\n"
        "• Исследовать два удивительных города\n"
        "• Попробовать настоящую китайскую кухню\n"
        "• Увидеть небоскрёбы Гонконга\n"
        "• Купить лучшие маркеры для твоего творчества\n"
        "• И создать кучу воспоминаний! 📸\n\n"
        "Люблю тебя, сестрёнка! ❤️"
    )
    await asyncio.sleep(3)
    
    await update.message.reply_text(
        "🎨 P.S. Маркеры, конечно, никуда не застряли - "
        "это был квест! 😄\n\n"
        "Но поездка - абсолютно реальная! ✈️🇨🇳"
    )
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена разговора."""
    await update.message.reply_text(
        "Квест отменён. Напиши /start чтобы начать заново!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    """Запуск бота."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден! Создай файл .env с токеном бота.")
        return
    
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Создаём ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TRACK_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_track_number)
            ],
            DRAWING_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_drawing_answer)
            ],
            ARTIST_CHALLENGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_artist_challenge)
            ],
            ARTIST_PROOF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_artist_proof)
            ],
            FINAL_REVEAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, final_reveal)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    
    # Запускаем бота
    logger.info("🚀 Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


