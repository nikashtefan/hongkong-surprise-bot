"""
Скрипт для автоматической генерации QR-кода для бота
Использование: python generate_qr.py your_bot_username
"""

import sys
import os

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Установи необходимые библиотеки:")
    print("pip install qrcode[pil] pillow")
    sys.exit(1)


def generate_qr_code(bot_username: str, output_file: str = "bot_qr_code.png") -> None:
    """Генерирует QR-код для Telegram бота.
    
    Args:
        bot_username: Username бота (без @)
        output_file: Имя выходного файла
    """
    # Создаём ссылку на бота
    bot_url = f"https://t.me/{bot_username}"
    
    # Создаём QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(bot_url)
    qr.make(fit=True)
    
    # Создаём изображение
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Сохраняем
    img.save(output_file)
    print(f"✅ QR-код создан: {output_file}")
    print(f"📱 Ссылка: {bot_url}")
    print(f"📏 Размер: {img.size[0]}x{img.size[1]} пикселей")


def generate_qr_with_template(
    bot_username: str, 
    output_file: str = "gift_card_with_qr.png"
) -> None:
    """Генерирует красивую открытку с QR-кодом.
    
    Args:
        bot_username: Username бота (без @)
        output_file: Имя выходного файла
    """
    # Создаём QR-код
    bot_url = f"https://t.me/{bot_username}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(bot_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Создаём открытку
    card_width = 800
    card_height = 1000
    card = Image.new('RGB', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)
    
    # Добавляем рамку
    border_color = "#2C3E50"
    draw.rectangle([20, 20, card_width-20, card_height-20], outline=border_color, width=3)
    
    # Добавляем текст (используем стандартный шрифт)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Заголовок
    title = "📦 УВЕДОМЛЕНИЕ О ДОСТАВКЕ"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((card_width - title_width) // 2, 60), title, fill=border_color, font=title_font)
    
    # Текст
    lines = [
        "",
        "Ваш заказ маркеров для рисования",
        "требует подтверждения",
        "",
        "Отсканируйте QR-код для отслеживания посылки:",
    ]
    
    y_position = 140
    for line in lines:
        if line:
            bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = bbox[2] - bbox[0]
            draw.text(((card_width - line_width) // 2, y_position), line, fill="#34495E", font=text_font)
        y_position += 40
    
    # Вставляем QR-код
    qr_size = 400
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_position = ((card_width - qr_size) // 2, y_position + 20)
    card.paste(qr_img, qr_position)
    
    # Информация внизу
    y_position = qr_position[1] + qr_size + 40
    info_lines = [
        "Трек-номер: 14012010",
        "Служба доставки: ArtExpress",
        "Статус: Требуется подтверждение",
    ]
    
    for line in info_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((card_width - line_width) // 2, y_position), line, fill="#7F8C8D", font=small_font)
        y_position += 30
    
    # Сохраняем
    card.save(output_file)
    print(f"✅ Открытка с QR-кодом создана: {output_file}")
    print(f"📱 Ссылка: {bot_url}")
    print(f"📏 Размер: {card_width}x{card_height} пикселей")
    print(f"🖨️ Готово к печати!")


def main():
    """Главная функция."""
    if len(sys.argv) < 2:
        print("❌ Использование: python generate_qr.py your_bot_username")
        print("Пример: python generate_qr.py hongkong_surprise_bot")
        sys.exit(1)
    
    bot_username = sys.argv[1].replace("@", "")
    
    print("🎨 Генерирую QR-код...")
    print()
    
    # Генерируем простой QR-код
    generate_qr_code(bot_username, "bot_qr_code.png")
    print()
    
    # Генерируем красивую открытку
    print("🎁 Генерирую открытку с QR-кодом...")
    generate_qr_with_template(bot_username, "gift_card_with_qr.png")
    print()
    
    print("✅ Готово! Файлы созданы:")
    print("   • bot_qr_code.png - простой QR-код")
    print("   • gift_card_with_qr.png - открытка для печати")
    print()
    print("🖨️ Распечатай gift_card_with_qr.png и положи в конверт!")


if __name__ == "__main__":
    main()


