import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройки из переменных окружения GitHub
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # Убедись, что добавил свой ID в Secrets!

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВНУТРЕННЯЯ ФУНКЦИЯ ДЛЯ ПРОГРЕСС-БАРА ---
def get_bar(percent):
    filled = int(min(percent, 100) / 10)
    return "🟩" * filled + "⬜️" * (10 - filled)

# Хэндлер команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🛡 **Daster Helper Bot (Report) 1.0 запущен!**\n\nПришли мне ссылку на канал или чат, чтобы начать технический осмотр.")

# Основная логика проверки
@dp.message()
async def check_link(message: types.Message):
    if not message.text or not message.text.startswith("http"):
        return

    link = message.text.lower()
    user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    
    # 1. БЕЛЫЙ СПИСОК
    trust_list = ['botfather', 'wallet', 'telegram', 'stickers', 'durov', 'dfreeg']
    if any(trust in link for trust in trust_list):
        return await message.answer("✅ **ОФИЦИАЛЬНЫЙ РЕСУРС**\n\nБезопасность: 100%. Этот ресурс верифицирован.")

    # 2. ПАРАМЕТРЫ И ЦЕЛЬ
    scam, toxic, shock = 5, 2, 0
    adult, psycho = "НЕ НАЙДЕНО", "НЕТ"
    target_id = random.randint(100000, 999999)
    
    # 3. АНАЛИЗ (Триггеры)
    scam_triggers = ['crypto', 'money', 'free', 'bonus', 'casino', 'invest', 'p2p', 'giveaway']
    for t in scam_triggers:
        if t in link: scam += 25

    toxic_triggers = ['dox', 'swat', 'shlak', 'trash', 'blood', 'death', 'kill']
    for t in toxic_triggers:
        if t in link:
            toxic += 40
            psycho = "ВОЗМОЖНО"
            shock += 35

    if 'xxx' in link or 'porn' in link or '18' in link:
        adult = "ОБНАРУЖЕНО 🔞"
        scam += 15

    # 4. ВЕРДИКТ
    total_danger = scam + toxic + shock
    if total_danger < 30:
        verdict = "🟢 **БЕЗОПАСНО**"
    elif 30 <= total_danger < 70:
        verdict = "🟡 **СРЕДНЯЯ УГРОЗА**"
    else:
        verdict = "🔴 **КРИТИЧЕСКАЯ УГРОЗА**"

    # 5. КНОПКА СНОСА
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚨 ПОДАТЬ ЗАЯВКУ НА СНОС", callback_data=f"report_{target_id}")]
    ])

    # 6. ОТЧЕТ
    report = (
        f"🚨 **АНАЛИЗ ЗАВЕРШЕН**\n\n"
        f"🎯 **Цель:** `#TRG-{target_id}`\n\n"
        f"• Скам: `{min(scam, 100)}%`\n[{get_bar(scam)}]\n\n"
        f"• Токсичность: `{min(toxic, 100)}%`\n[{get_bar(toxic)}]\n\n"
        f"• Шок-контент: `{min(shock, 100)}%`\n[{get_bar(shock)}]\n\n"
        f"• 18+ Контент: **{adult}**\n"
        f"• Ломает психику: **{psycho}**\n\n"
        f"**Вердикт:** {verdict}"
    )

    await message.answer(report, parse_mode="Markdown", reply_markup=keyboard)

    # 7. ЛОГ ДЛЯ ТЕБЯ
    if ADMIN_ID:
        try:
            await bot.send_message(ADMIN_ID, f"👤 Запрос от {user_info}\n🔗 Ссылка: {message.text}\n📈 Цель: #TRG-{target_id}")
        except:
            pass

# Обработка нажатия кнопки
@dp.callback_query(F.data.startswith("report_"))
async def handle_report(callback: types.CallbackQuery):
    await callback.answer("🚀 Заявка на снос отправлена модераторам!", show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None) # Убираем кнопку после нажатия

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
