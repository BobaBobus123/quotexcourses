import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from db import init_db, add_user

TOKEN = os.environ.get("BOT_TOKEN")
SUPPORT = "https://t.me/quotexcompany_support"
WELCOME_IMAGE = "welcome.jpg"

init_db()

# ================== Состояние пользователей ==================
user_states = {}

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
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def payment_menu(course_id):
    prices = {1: "5 000 ₽", 2: "15 000 ₽", 3: "25 000 ₽"}
    price = prices.get(course_id, "Неизвестно")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"💳 Оплатить {price}", callback_data=f"pay_rub_{course_id}")],
        [InlineKeyboardButton("👨‍💼 Написать менеджеру", url=SUPPORT)],
        [InlineKeyboardButton("ℹ️ О курсе", callback_data=f"info_{course_id}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def support_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

# ================== /START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    referrer_id = int(args[0]) if args else None

    add_user(user.id, referrer_id)

    user_states[user.id] = ["main"]

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
    user_id = update.effective_user.id

    if user_id not in user_states:
        user_states[user_id] = ["main"]

    if data == "back":
        if len(user_states[user_id]) > 1:
            user_states[user_id].pop()
        await show_menu(query, user_states[user_id][-1])
        return

    new_screen = None

    if data == "courses":
        new_screen = "courses"
    elif data.startswith("course_"):
        new_screen = data
    elif data.startswith("pay_"):
        new_screen = data
    elif data == "support":
        new_screen = "support"
    elif data.startswith("info_"):
        course_id = int(data.split("_")[1])
        await send_course_info(query, course_id)

    if new_screen:
        user_states[user_id].append(new_screen)
        await show_menu(query, new_screen)

# ================== Функция показа меню ==================

async def show_menu(query, menu_id):
    if menu_id == "main":
        await query.edit_message_caption(
            caption="👋 Выберите действие:",
            reply_markup=main_menu()
        )

    elif menu_id == "courses":
        await query.edit_message_caption(
            caption="🎓 <b>Наши курсы</b>\n\nВыберите подходящий уровень:",
            parse_mode="HTML",
            reply_markup=courses_menu()
        )

    elif menu_id == "course_1":
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

    elif menu_id == "course_2":
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

    elif menu_id == "course_3":
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

    elif menu_id.startswith("pay_"):
        parts = menu_id.split("_")
        course_id = int(parts[2])
        prices = {1: "5 000 ₽", 2: "15 000 ₽", 3: "25 000 ₽"}
        price = prices.get(course_id, "Неизвестно")
        await query.edit_message_caption(
            caption=(f"💳 <b>Оплата курса {course_id}</b>\n\n"
                     f"Стоимость: {price}\n\n"
                     "Для оплаты напишите менеджеру."),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💼 Менеджер", url=SUPPORT)],
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]
            ])
        )

    elif menu_id == "support":
        await query.edit_message_caption(
            caption=("👨‍💼 <b>Поддержка</b>\n\n"
                     "По всем вопросам:\n"
                     "@quotexcompany_support"),
            parse_mode="HTML",
            reply_markup=support_menu()
        )

# ================== О КУРСЕ ==================

async def send_course_info(query, course_id):
    files = {
        1: "presentation.pdf",
        2: "presentation2.pdf",
        3: "presentation3.pdf"
    }
    file_path = files.get(course_id)
    if file_path and os.path.exists(file_path):
        await query.message.reply_document(open(file_path, "rb"))
    else:
        await query.message.reply_text("Презентация не найдена.")

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
