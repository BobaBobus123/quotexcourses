import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.environ.get("BOT_TOKEN")
SUPPORT = "https://t.me/quotexcompany_support"
WELCOME_IMAGE = "welcome.jpg"


# ================== КЛАВИАТУРЫ ==================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Курсы", callback_data="courses")],
        [InlineKeyboardButton("👨‍💼 Поддержка", callback_data="support")]
    ])


def courses_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Криптотрейдинг с нуля", callback_data="course_1")],
        [InlineKeyboardButton("🔵 Проф трейдинг и аналитика", callback_data="course_2")],
        [InlineKeyboardButton("🔴 VIP Мастер трейдинга", callback_data="course_3")],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"courses")]
    ])


def payment_menu(course_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Оплатить USDT", callback_data=f"pay_usdt_{course_id}")],
        [InlineKeyboardButton("₽ Оплатить в рублях", callback_data=f"pay_rub_{course_id}")],
        [InlineKeyboardButton("👨‍💼 Написать менеджеру", url=SUPPORT)],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"course_{course_id}")]
    ])


# ================== /START С ФОТО ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(WELCOME_IMAGE, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=(
                "👋 Добро пожаловать в <b>Quotex Company</b>\n\n"
                "Профессиональное обучение трейдингу:\n"
                "от нуля до стабильного дохода.\n\n"
                "Выберите действие:"
            ),
            parse_mode="HTML",
            reply_markup=main_menu()
        )


# ================== CALLBACK ==================

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- Главное меню ---
    if data == "back_main":
        await query.edit_message_caption(
            caption="👋 Выберите действие:",
            reply_markup=main_menu()
        )

    # --- Курсы ---
    elif data == "courses":
        await query.edit_message_caption(
            caption="🎓 <b>Наши курсы</b>\n\nВыберите подходящий уровень:",
            parse_mode="HTML",
            reply_markup=courses_menu()
        )

    # --- Курс 1 ---
    elif data == "course_1":
        text = (
            "🟢 <b>Курс 1: Криптотрейдинг с нуля</b>\n\n"
            "Идеально для новичков.\n\n"
            "<b>Что входит:</b>\n"
            "• Мануал по трейдингу\n"
            "• Наставничество\n"
            "• База рынка\n"
            "• Гайд по Quotex\n\n"
            "<b>Результат:</b>\n"
            "Доход до 50 000 ₽ / месяц"
        )
        await query.edit_message_caption(
            caption=text, parse_mode="HTML", reply_markup=payment_menu(1)
        )

    # --- Курс 2 ---
    elif data == "course_2":
        text = (
            "🔵 <b>Курс 2: Профессиональный трейдинг</b>\n\n"
            "Для стабильного дохода.\n\n"
            "<b>Что входит:</b>\n"
            "• Расширенный мануал\n"
            "• Аналитика рынка\n"
            "• Индикаторы\n"
            "• Стратегии\n\n"
            "<b>Результат:</b>\n"
            "Доход до 100 000 ₽ / месяц"
        )
        await query.edit_message_caption(
            caption=text, parse_mode="HTML", reply_markup=payment_menu(2)
        )

    # --- Курс 3 ---
    elif data == "course_3":
        text = (
            "🔴 <b>VIP Мастер трейдинга</b>\n\n"
            "Максимальный уровень.\n\n"
            "<b>Что входит:</b>\n"
            "• Самый большой мануал\n"
            "• VIP наставник\n"
            "• Психология трейдера\n"
            "• Закрытый чат\n\n"
            "<b>Результат:</b>\n"
            "Потенциал до 1 000 000 ₽ / месяц"
        )
        await query.edit_message_caption(
            caption=text, parse_mode="HTML", reply_markup=payment_menu(3)
        )

    # --- Оплата ---
    elif data.startswith("pay_"):
        parts = data.split("_")
        currency = "USDT" if parts[1] == "usdt" else "рублях"
        course_id = parts[2]

        await query.edit_message_caption(
            caption=(
                f"💳 <b>Оплата курса {course_id}</b>\n\n"
                f"Способ: {currency}\n\n"
                "Для оплаты напишите менеджеру."
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💼 Менеджер", url=SUPPORT)],
                [InlineKeyboardButton("🔙 Назад", callback_data="courses")]
            ])
        )

    # --- Поддержка ---
    elif data == "support":
        await query.edit_message_caption(
            caption=(
                "👨‍💼 <b>Поддержка</b>\n\n"
                "По всем вопросам:\n"
                "@quotexcompany_support"
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_main")]
            ])
        )


# ================== ТЕКСТ ==================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Используйте кнопки меню 👇",
        reply_markup=main_menu()
    )


# ================== ЗАПУСК ==================

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Бот запущен...")
    app.run_polling()
