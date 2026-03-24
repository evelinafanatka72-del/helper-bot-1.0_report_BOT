import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройки (Берем из GitHub Secrets)
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для полосок загрузки
def get_bar(percent):
    filled = int(min(percent, 100) / 10)
    return "🟩" * filled + "⬜️" * (10 - filled)

# --- 1. СТАРТ ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🛡 **TELEGRAM PROTECTION SYSTEM 5.0**\n\n"
        "Я провожу аудит безопасности каналов и чатов.\n"
        "**Пришлите ссылку (t.me/...) для анализа.**"
    )

# --- 2. ГЛАВНЫЙ СКАНЕР ---
@dp.message()
async def scanner_logic(message: types.Message):
    if not message.text or "t.me/" not in message.text:
        return

    link = message.text.lower()
    
    # Статус "Защита запущена"
    status = await message.answer("🔄 **Инициализация защиты...**\n`[⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️]`")
    await asyncio.sleep(1)

    # Триггеры для "Смертельного" уровня (настрой сам список)
    danger_triggers = ['dox', 'swat', 'shlak', 'rip', 'kill', 'dark', 'cp', 'нарко', '18', 'xxx']
    scam_triggers = ['crypto', 'money', 'invest', 'cash', 'nft', 'wallet', 'bonus']

    # Имитация стадий проверки
    process_steps = [
        "🔍 Поиск в базе угроз...",
        "🧩 Анализ структуры ссылки...",
        "📊 Финализация данных..."
    ]

    for i, step in enumerate(process_steps):
        bar = get_bar((i + 1) * 33)
        await status.edit_text(f"🛰 **{step}**\n`[{bar}]`")
        await asyncio.sleep(1.2)

    # --- РАСЧЕТ РИСКОВ (Логика защиты) ---
    toxic_level = random.randint(40, 95) if any(x in link for x in danger_triggers) else random.randint(2, 10)
    scam_level = random.randint(50, 98) if any(x in link for x in scam_triggers) else random.randint(5, 15)
    shock_level = random.randint(30, 90) if any(x in link for x in ['blood', 'death', 'trash']) else 0

    total = toxic_level + scam_level + shock_level

    # Твои 4 уровня безопасности
    if total < 30:
        verdict = "🟢 **УРОВЕНЬ 1: БЕЗОПАСНО**"
        v_icon = "✅"
    elif total < 65:
        verdict = "🟡 **УРОВЕНЬ 2: СРЕДНЯЯ ОПАСНОСТЬ**"
        v_icon = "⚠️"
    elif total < 110:
        verdict = "🟠 **УРОВЕНЬ 3: ВЫСОКАЯ УГРОЗА**"
        v_icon = "🚨"
    else:
        verdict = "🔴 **УРОВЕНЬ 4: СМЕРТЕЛЬНАЯ УГРОЗА**"
        v_icon = "💀"

    target_id = random.randint(100000, 999999)

    # --- ФИНАЛЬНЫЙ ОТЧЕТ ---
    report = (
        f"🚨 **ОТЧЕТ ЗАЩИТЫ ТЕЛЕГРАМ**\n"
        f"🎯 **Target:** `#TRG-{target_id}`\n\n"
        f"📡 **Результаты анализа:**\n"
        f"• Скам: `{scam_level}%`\n[{get_bar(scam_level)}]\n"
        f"• Токсичность: `{toxic_level}%`\n[{get_bar(toxic_level)}]\n"
        f"• Шок-контент: `{shock_level}%`\n[{get_bar(shock_level)}]\n\n"
        f"📌 **Дополнительно:**\n"
        f"• 18+ Материалы: {'ОБНАРУЖЕНО' if total > 100 else 'ЧИСТО'}\n"
        f"• Угроза жизни: {'КРИТИЧЕСКИ' if total > 150 else 'НЕТ'}\n\n"
        f"**Вердикт:** {verdict} {v_icon}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💣 ПОДАТЬ НА СНОС (15 ЖАЛОБ)", callback_data=f"kill_{target_id}")]
    ])

    await status.edit_text(report, reply_markup=kb, parse_mode="Markdown")

# --- 3. ОБРАБОТКА СНОСА ---
@dp.callback_query(F.data.startswith("kill_"))
async def handle_kill(callback: types.CallbackQuery):
    target = callback.data.split("_")[1]
    
    await callback.answer("⏳ Активация протокола сноса...", show_alert=False)
    await asyncio.sleep(2)
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"✅ **Жалобы зафиксированы.**\nЦель #TRG-{target} передана в отдел модерации @DFREEG.")

    # Отчет админу
    if ADMIN_ID:
        try:
            await bot.send_message(ADMIN_ID, f"🔔 **ЗАПРОС НА СНОС!**\nЦель: #TRG-{target}\nОтправил: @{callback.from_user.username}")
        except: pass

async def main():
    # Защита от добавления в группы
    @dp.message(F.chat.type != "private")
    async def leave_group(message: types.Message):
        await message.leave_chat()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
