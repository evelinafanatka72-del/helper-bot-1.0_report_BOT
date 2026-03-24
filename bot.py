import asyncio
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

# Вставь свой токен и ID (узнай ID через @userinfobot)
TOKEN = "ТВОЙ_ТОКЕН"
ADMIN_ID = 123456789 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text.contains("t.me/"))
async def scan_process(message: types.Message):
    # 1. Начало осмотра
    status_msg = await message.answer("🔍 **Начинаю технический осмотр ссылки...**\n[░░░░░░░░░░] 0%")
    
    # 2. Имитация процесса (30-60 сек для солидности)
    await asyncio.sleep(4)
    await status_msg.edit_text("🧪 **Анализ текста на TOXIC и SCAM...**\n[████░░░░░░] 40%")
    await asyncio.sleep(5)
    await status_msg.edit_text("🧬 **Проверка медиафайлов на 18+ и шок-контент...**\n[███████░░░] 70%")
    await asyncio.sleep(5)
    
    # --- АНАЛИЗ ЦИФР (Генерация данных) ---
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
    
    # Создаем кнопку только если канал опасен или подозрителен
    kb_list = []
    if show_button:
        kb_list.append([types.InlineKeyboardButton(text="🚨 ПОДАТЬ ЗАЯВКУ НА СНОС", callback_data="report_delete")])
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=kb_list)
    await status_msg.edit_text(result_text, reply_markup=kb)

# 4. Обработка заявки на снос
@dp.callback_query(F.data == "report_delete")
async def send_to_admins(callback: types.Callback_query):
    # Уведомляем пользователя
    await callback.message.answer("📥 **Заявка отправлена администраторам Daster Store.**\nМы изучим цель и начнем атаку жалобами, если это подтвердится.")
    
    # Отправляем отчет ТЕБЕ (админу)
    await bot.send_message(
        ADMIN_ID, 
        f"🔥 **ЦЕЛЬ НА СНОС!**\nОтправил: @{callback.from_user.username}\nТекст проверки:\n{callback.message.text}"
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
