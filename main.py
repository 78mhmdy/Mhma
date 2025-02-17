import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from fastapi import FastAPI, Request

# تعيين مفاتيح API
TELEGRAM_BOT_TOKEN = "7504087824:AAHCgJb3s99FtOeIIga8oDYdV6Zn9y82gQw"
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

WEBHOOK_URL = "https://mhma-gamma.vercel.app/webhook"  # استبدل هذا بالرابط الحقيقي بعد نشر البوت

# تهيئة البوت والموزع
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# دالة إرسال الطلب إلى OpenRouter
async def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
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

# Webhook لاستقبال التحديثات من تيليغرام
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)
    return {"ok": True}

@app.get("/")
async def home():
    return {"message": "Bot is running on Vercel"}

# ضبط Webhook عند بدء التشغيل
async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)

asyncio.run(set_webhook())
