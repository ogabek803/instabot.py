import logging
import instaloader
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio
from aiogram.client.default import DefaultBotProperties  # Yangi qo‘shilgan import

# Bot tokeningizni shu yerga qo'ying
TOKEN = "8067648519:AAFKiA-YcwNgrbLaVYUdO3zk7JI8rhZfvJk"

# Aiogram obyektlari
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))  # Tuzatilgan joy
dp = Dispatcher()

# Instaloader obyekti
L = instaloader.Instaloader()

# Instagramdan video yuklab olish funksiyasi
async def download_instagram_video(url: str):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        video_url = post.video_url

        # Video hajmini nazorat qilish (maksimal 720p)
        video_data = requests.get(video_url)
        file_size = len(video_data.content) / (1024 * 1024)  # MB ga o'tkazamiz

        if file_size > 50:  # Agar fayl hajmi 50MB dan katta bo'lsa
            return "Fayl hajmi juda katta, uni yuklab bo‘lmaydi. ⚠️"

        return video_url
    except Exception as e:
        return f"Xatolik: {str(e)}"

# Bot komandalarini sozlash
@dp.message()
async def handle_message(message: Message):
    if "instagram.com" in message.text:
        await message.answer("⏳ ozroq qisib tur😂")
        video_url = await download_instagram_video(message.text)
        
        if video_url.startswith("http"):
            await message.answer_video(video_url, caption="📥MA SUKA😂!")
        else:
            await message.answer(f"❌ Xatolik: {video_url}")
    else:
        await message.answer("📌 Pezdukcha Linkni tashachi!")

# Asosiy ishga tushirish funksiyasi
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())