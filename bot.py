import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройки
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # Твой ID (узнай в @userinfobot)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_bar(percent):
    filled = int(min(percent, 100) / 10)
    return "🟩" * filled + "⬜️" * (10 - filled)

# --- 1. ПРИВЕТСТВИЕ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Как это работает?", callback_data="help_info")]
    ])
    await message.answer(
        "🛡 **Daster Helper Control 2.0**\n\n"
        "Я сканирую ресурсы на токсичность, скам и запрещенный контент.\n"
        "**Пришли мне ссылку на канал или чат.**",
        reply_markup=kb
    )

@dp.callback_query(F.data == "help_info")
async def help_info(callback: types.CallbackQuery):
    await callback.answer(
        "Бот анализирует метаданные и содержимое ссылки по 7 критериям нарушения. "
        "Добавление в группы отключено для безопасности.", 
        show_alert=True
    )

# --- 2. ЛОГИКА СКАНЕРА С АНИМАЦИЕЙ ---
@dp.message()
async def scan_link(message: types.Message):
    if not message.text or "t.me/" not in message.text:
        return

    link = message.text.lower()
    
    # Белый список
    trust = ['botfather', 'wallet', 'telegram', 'durov', 'dfreeg']
    if any(t in link for t in trust):
        return await message.answer("✅ **ОФИЦИАЛЬНЫЙ РЕСУРС**\nБезопасность: 100%")

    # Начало анимации
    status_msg = await message.answer("🔍 **Инициализация сканирования...**\n`[⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️]`")
    await asyncio.sleep(1)

    # Параметры (имитация анализа)
    scam = 45 if any(x in link for x in ['crypto', 'money', 'free', 'win']) else random.randint(5, 20)
    toxic = 60 if any(x in link for x in ['dox', 'swat', 'shlak']) else random.randint(2, 15)
    shock = random.randint(0, 10)
    
    # Анимация заполнения (3 этапа)
    stages = ["📡 Подключение к серверам...", "🧬 Анализ контента...", "📊 Финализация отчета..."]
    for i in range(1, 4):
        bar = get_bar(i * 33)
        await status_msg.edit_text(f"{stages[i-1]}\n`[{bar}]`")
        await asyncio.sleep(0.8)

    # Уровни опасности
    total = scam + toxic + shock
    if total < 30:
        verdict = "🟢 **УРОВЕНЬ 1: БЕЗОПАСНО**"
    elif total < 60:
        verdict = "🟡 **УРОВЕНЬ 2: СРЕДНЯЯ ОПАСНОСТЬ**"
    elif total < 90:
        verdict = "🟠 **УРОВЕНЬ 3: ВЫСОКИЙ РИСК**"
    else:
        verdict = "🔴 **УРОВЕНЬ 4: СМЕРТЕЛЬНАЯ УГРОЗА**"

    target_id = random.randint(111111, 999999)
    
    report = (
        f"🚨 **АНАЛИЗ ЗАВЕРШЕН**\n"
        f"🎯 Цель: `#TRG-{target_id}`\n\n"
        f"• Скам: `{scam}%`\n[{get_bar(scam)}]\n"
        f"• Токсичность: `{toxic}%`\n[{get_bar(toxic)}]\n"
        f"• Шок-контент: `{shock}%`\n[{get_bar(shock)}]\n\n"
        f"• 18+ Материалы: {'ДА' if total > 50 else 'НЕТ'}\n"
        f"• Маты/Агрессия: {'ВЫСОКО' if toxic > 40 else 'НИЗКО'}\n\n"
        f"**Вердикт:** {verdict}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 ПОДАТЬ НА СНОС", callback_data=f"snos_{target_id}")]
    ])

    await status_msg.edit_text(report, reply_markup=kb, parse_mode="Markdown")

# --- 3. ОБРАБОТКА СНОСА ---
@dp.callback_query(F.data.startswith("snos_"))
async def handle_snos(callback: types.CallbackQuery):
    target = callback.data.split("_")[1]
    
    await callback.answer("⏳ Подготовка пакетов жалоб...", show_alert=False)
    await asyncio.sleep(2)
    
    # Имитация процесса
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"✅ **Жалобы отправлены (15 шт).**\nЦель #TRG-{target} поставлена в очередь на ограничение.")

    # Отчет тебе
    if ADMIN_ID:
        try:
            await bot.send_message(
                ADMIN_ID, 
                f"🔔 **УВЕДОМЛЕНИЕ О СНОСЕ**\n\n"
                f"Админ @DFREEG, пользователь запросил снос цели `#TRG-{target}`.\n"
                f"Требуется ручная проверка ресурса."
            )
        except:
            pass

async def main():
    # Запрещаем работу в группах (только приватные чаты)
    @dp.message(F.chat.type != "private")
    async def no_groups(message: types.Message):
        await message.leave_chat()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
