import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
 # تعيين مفاتيح API
TELEGRAM_BOT_TOKEN = ""
OPENROUTER_API_KEY = ""
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# تعيين مفاتيح API
TELEGRAM_BOT_TOKEN = "7504087824:AAHCgJb3s99FtOeIIga8oDYdV6Zn9y82gQw"
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# تهيئة البوت والموزع
bot = Bot(token=TELEGRAM_BOT_TOKEN)  # تم تصحيح التعريف هنا
dp = Dispatcher()

# دالة إرسال الطلب إلى OpenRouter
async def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # يمكن تغييره إلى gpt-4 إذا كان متاحًا
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "لم أفهم سؤالك!")

# التعامل مع الرسائل المستلمة
@dp.message()
async def handle_message(message: Message):
    user_input = message.text
    ai_response = await get_ai_response(user_input)
    await message.answer(ai_response)

# تشغيل البوت
async def main():
    print("البوت قيد التشغيل...")
    await dp.start_polling(bot)  # الآن `bot` معرف بشكل صحيح

if __name__ == "__main__":
    asyncio.run(main())
