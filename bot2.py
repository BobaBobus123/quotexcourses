import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/quotextradenews"
REVIEWS_CHANNEL = "https://t.me/+7FvjGCCQ4ng4MGM8"
COURSES_BOT = "https://t.me/QuotexCourses_bot"
CONTACT = "@quotexcompany_support"
WELCOME_IMAGE = "start1.jpg"


bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

# ---------- Главное меню ----------

def main_menu():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="📌 О проекте", callback_data="about"),
            types.InlineKeyboardButton(text="🎓 Обучение", callback_data="study")
        ],
        [
            types.InlineKeyboardButton(text="📊 Методология", callback_data="method"),
            types.InlineKeyboardButton(text="📈 Результаты", callback_data="results")
        ],
        [
            types.InlineKeyboardButton(text="🧠 База знаний", callback_data="knowledge"),
            types.InlineKeyboardButton(text="❓ Вопросы", callback_data="faq")
        ],
        [
            types.InlineKeyboardButton(text="🛡 Прозрачность", callback_data="trust"),
            types.InlineKeyboardButton(text="💬 Отзывы", url=REVIEWS_CHANNEL)
        ],
        [
            types.InlineKeyboardButton(text="💳 Перейти к обучению", callback_data="buy")
        ],
        [
            types.InlineKeyboardButton(text="📞 Связь", callback_data="contact"),
            types.InlineKeyboardButton(text="🚀 Основной канал", url=CHANNEL_LINK)
        ]
    ])

# ---------- /start ----------

@dp.message(CommandStart())
async def start(message: types.Message):
    text = (
        "🚀 *Quotex Crypto Academy*\n\n"
        "Добро пожаловать в образовательную платформу\n"
        "по криптотрейдингу и цифровым рынкам 📊\n\n"
        "Здесь ты найдёшь:\n"
        "💡 структурированное обучение\n"
        "🧠 реальные знания\n"
        "📈 практический подход\n\n"
        "Выбери раздел ниже 👇"
    )

    photo = types.FSInputFile(WELCOME_IMAGE)
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_menu()
    )


# ---------- Универсальная кнопка Назад ----------

def back_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")]
    ])

@dp.callback_query(lambda c: c.data == "back")
async def back(call: types.CallbackQuery):
    await call.message.edit_text(
        "🏠 *Главное меню*\n\nВыбери нужный раздел 👇",
        reply_markup=main_menu()
    )

# ---------- Разделы ----------

@dp.callback_query(lambda c: c.data == "about")
async def about(call):
    text = (
        "📌 *О проекте*\n\n"
        "Quotex Crypto Academy — это образовательная среда,\n"
        "созданная для тех, кто хочет понимать рынок,\n"
        "а не играть в угадайку 🎯\n\n"
        "Мы фокусируемся на:\n"
        "📊 логике движения цены\n"
        "📚 анализе данных\n"
        "🧠 принятии решений\n"
    )
    await call.message.edit_text(text, reply_markup=back_kb())

@dp.callback_query(lambda c: c.data == "study")
async def study(call):
    text = (
        "🎓 *Обучение*\n\n"
        "Формат обучения:\n\n"
        "📚 модули\n"
        "🎥 видео-уроки\n"
        "🧠 теория + практика\n"
        "📊 реальные кейсы\n\n"
        "Без воды. Только то, что работает."
    )
    await call.message.edit_text(text, reply_markup=back_kb())

@dp.callback_query(lambda c: c.data == "method")
async def method(call):
    text = (
        "📊 *Методология*\n\n"
        "Мы используем:\n\n"
        "📈 технический анализ\n"
        "📉 рыночную структуру\n"
        "🧮 риск-менеджмент\n"
        "🧠 психологию трейдинга\n\n"
        "Это системный подход, а не сигналы."
    )
    await call.message.edit_text(text, reply_markup=back_kb())

@dp.callback_query(lambda c: c.data == "results")
async def results(call):
    text = (
        "📈 *Результаты*\n\n"
        "Наши ученики:\n\n"
        "✔ понимают рынок\n"
        "✔ умеют анализировать\n"
        "✔ не зависят от чужих прогнозов\n\n"
        "Главный результат — мышление трейдера 🧠"
    )
    await call.message.edit_text(text, reply_markup=back_kb())

@dp.callback_query(lambda c: c.data == "knowledge")
async def knowledge(call):
    text = (
        "🧠 *База знаний*\n\n"
        "Внутри обучения:\n\n"
        "📘 глоссарий терминов\n"
        "📊 паттерны рынка\n"
        "📉 примеры сделок\n"
        "🧮 формулы риска\n"
    )
    await call.message.edit_text(text, reply_markup=back_kb())

@dp.callback_query(lambda c: c.data == "faq")
async def faq(call):
    text = (
        "❓ *Частые вопросы*\n\n"
        "— Это подходит новичкам?\n"
        "Да, обучение с нуля 👶\n\n"
        "— Это инвестиции?\n"
        "Нет, это образование 📚\n\n"
        "— Есть гарантии прибыли?\n"
        "Нет. Есть знания и система."
    )
    await call.message.edit_text(text, reply_markup=back_kb())

# ---------- Прозрачность (анти-скам блок) ----------

@dp.callback_query(lambda c: c.data == "trust")
async def trust(call):
    text = (
        "🛡 *Прозрачность*\n\n"
        "Мы не обещаем:\n"
        "❌ лёгких денег\n"
        "❌ гарантированной прибыли\n"
        "❌ чудо-стратегий\n\n"
        "Мы даём:\n"
        "✔ структуру\n"
        "✔ знания\n"
        "✔ инструменты\n\n"
        "Ты учишься принимать решения сам.\n"
        "Это и есть главный навык трейдера 💼"
    )
    await call.message.edit_text(text, reply_markup=back_kb())

# ---------- Покупка / переход ----------

@dp.callback_query(lambda c: c.data == "buy")
async def buy(call):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎓 Перейти к обучению", url=COURSES_BOT)],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

    text = (
        "💳 *Доступ к обучению*\n\n"
        "Обучение проходит в отдельном боте.\n\n"
        "Там ты найдёшь:\n"
        "📚 уроки\n"
        "🧠 практику\n"
        "📊 разборы\n\n"
        "Нажми кнопку ниже 👇"
    )
    await call.message.edit_text(text, reply_markup=keyboard)

# ---------- Контакты ----------

@dp.callback_query(lambda c: c.data == "contact")
async def contact(call):
    text = (
        "📞 *Связь*\n\n"
        "По всем вопросам:\n"
        f"{CONTACT}\n\n"
        "Мы не продаём мечты.\n"
        "Мы обучаем мышлению 🧠"
    )
    await call.message.edit_text(text, reply_markup=back_kb())

# ---------- Запуск ----------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())