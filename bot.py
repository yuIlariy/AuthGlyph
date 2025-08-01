import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, ADMIN_ID
from handlers.authwatcher import router as authwatch_router

# 🦔 Bot setup
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(authwatch_router)

# 🧠 Start command
@dp.message(lambda msg: msg.text == "/start" and msg.from_user.id == ADMIN_ID)
async def start_handler(msg: Message):
    await msg.answer_photo(
        photo="https://telegra.ph/file/ec17880d61180d3312d6a.jpg",
        caption=(
            "<b>🦔 AuthGlyph Activated</b>\n\n"
            "🌋 Monitoring login events with geo awareness and glyph precision.\n"
            "📍 Use /authstats to view the latest login.\n"
            "🧠 More modules coming soon — breach detection, heatmaps, and more."
        )
    )

async def main():
    print("🦔 AuthGlyph deployed successfully.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
