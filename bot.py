import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, ADMIN_ID
from handlers.authwatcher import router as authwatch_router
from handlers.loginstats import router as loginstats_router
from handlers.authgrep import router as authgrep_router  # ✅ NEW
from utils.authlog import get_last_login, geo_lookup, record_login
from utils.captions import themed_caption

# 🦔 Bot setup
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(authwatch_router)
dp.include_router(loginstats_router)
dp.include_router(authgrep_router)  # ✅ Register grep router

_last_alert = None

# 🔥 Auto-monitoring loop
async def monitor_logins():
    global _last_alert
    print("🌋 Auth monitor loop started.")
    while True:
        try:
            ip, user, time = get_last_login()
            alert_key = f"{user}|{ip}|{time}"
            if alert_key != _last_alert and ip != "N/A":
                geo = geo_lookup(ip)
                caption = themed_caption(ip, user, time, geo)
                await bot.send_message(chat_id=ADMIN_ID, text=caption)
                print(f"🦔 Alert sent for {user} @ {ip}")
                _last_alert = alert_key
                # Extract country code from geo string
                country = geo.split()[-1] if geo else ""
                record_login(ip, user, time, country)
        except Exception as e:
            print(f"⚠️ Auth monitor error: {e}")
        await asyncio.sleep(10)

# 🧠 Start command
@dp.message(lambda msg: msg.text == "/start" and msg.from_user.id == ADMIN_ID)
async def start_handler(msg: Message):
    await msg.answer_photo(
        photo="https://telegra.ph/file/ec17880d61180d3312d6a.jpg",
        caption=(
            "<b>🦔 AuthGlyph Activated</b>\n\n"
            "🌋 Monitoring login events with geo awareness and glyph precision.\n"
            "📍 Use /authstats, /loginstats, or /authgrep to trace logins.\n"
            "🧠 More modules coming soon — breach detection, heatmaps, and more."
        )
    )

# 🚀 Main entry
async def main():
    print("🦔 AuthGlyph deployed successfully.")
    asyncio.create_task(monitor_logins())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

