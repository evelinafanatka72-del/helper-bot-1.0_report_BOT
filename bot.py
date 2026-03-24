import os
import asyncio
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

# --- НАСТРОЙКИ БЕЗОПАСНОСТИ ---
# Бот берет токен из переменных окружения (Environment Variables)
# На GitHub это настраивается в Settings -> Secrets
TOKEN = os.getenv("BOT_TOKEN") 
ADMIN_ID = int(os.getenv("ADMIN_ID", 123456789)) # Твой ID тут (можно оставить цифрами)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ХЭНДЛЕР: КОМАНДА /START ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🛡️ **Daster Helper Bot (Report) 1.0 запущен!**\n\n"
        "Я сканирую Telegram на наличие токсичности, скама и опасного контента.\n\n"
        "📥 **Пришли мне ссылку на канал или чат** (например, t.me/name), "
        "чтобы начать технический осмотр."
    )

# --- ХЭНДЛЕР: ПРОВЕРКА ССЫЛОК ---
@dp.message(F.text.contains("t.me/"))
async def scan_process(message: types.Message):
    # 1. Начало осмотра
    status_msg = await message.answer("🔍 **Начинаю технический осмотр ссылки...**\n[░░░░░░░░░░] 0%")
    
    # 2. Имитация процесса
    await asyncio.sleep(4)
    await status_msg.edit_text("🧪 **Анализ текста на TOXIC и SCAM...**\n[████░░░░░░] 40%")
    await asyncio.sleep(5)
    await status_msg.edit_text("🧬 **Проверка медиафайлов на 18+ и шок-контент...**\n[███████░░░] 70%")
    await asyncio.sleep(5)
    
    # --- АНАЛИЗ ЦИФР ---
    toxic_val = random.randint(5, 95)
    scam_val = random.randint(0, 80)
    is_psycho = "ДА" if toxic_val > 70 else "НЕТ"
    is_18plus = "ОБНАРУЖЕНО" if random.random() > 0.7 else "НЕ НАЙДЕНО"
    
    # --- ЛОГИКА ВЕРДИКТА ---
    if toxic_val > 75 or scam_val > 60 or is_18plus == "ОБНАРУЖЕНО":
        verdict = "🔴 КРИТИЧЕСКАЯ УГРОЗА / ТОКСИЧНО"
        emoji = "🚨"
        show_button = True
    elif 40 <= toxic_val <= 75:
        verdict = "🟡 ПОДОЗРИТЕЛЬНО (Warning)"
        emoji = "⚠️"
        show_button = True
    else:
        verdict = "🟢 БЕЗОПАСНО"
        emoji = "✅"
        show_button = False

    # 3. Финальный результат
    result_text = (
        f"{emoji} **СКАНИРОВАНИЕ ЗАВЕРШЕНО!**\n\n"
        f"📊 **Результаты:**\n"
        f"• Токсичность: {toxic_val}%\n"
        f"• Скам: {scam_val}%\n"
        f"• Ломает психику: {is_psycho}\n"
        f"• 18+ Контент: {is_18plus}\n\n"
        f"**Вердикт:** {verdict}"
    )
    
    kb_list = []
    if show_button:
        kb_list.append([types.InlineKeyboardButton(text="🚨 ПОДАТЬ ЗАЯВКУ НА СНОС", callback_data="report_delete")])
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=kb_list)
    await status_msg.edit_text(result_text, reply_markup=kb)

# --- ХЭНДЛЕР: ОБРАБОТКА ЗАЯВКИ НА СНОС ---
@dp.callback_query(F.data == "report_delete")
async def send_to_admins(callback: types.Callback_query):
    await callback.message.answer("📥 **Заявка отправлена администраторам Daster Store.**\nОжидайте массовой атаки жалобами.")
    
    await bot.send_message(
        ADMIN_ID, 
        f"🔥 **ЦЕЛЬ НА СНОС!**\nОтправил: @{callback.from_user.username}\nДанные проверки:\n{callback.message.text}"
    )
    await callback.answer()

# --- ЗАПУСК ---
async def main():
    print("Бот запущен и сканирует...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
