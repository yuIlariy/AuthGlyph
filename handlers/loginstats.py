from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from utils.authlog import get_last_login, get_login_count, geo_lookup

router = Router()

@router.message(lambda msg: msg.text == "/loginstats" and msg.from_user.id == ADMIN_ID)
async def loginstats(msg: Message):
    ip, user, time = get_last_login()
    count = get_login_count()
    geo_str, _, whois = geo_lookup(ip)  # ✅ WHOIS from geo_lookup

    caption = (
        f"📊 <b>Login Stats</b>\n"
        f"🔢 <b>Total Logins:</b> <code>{count}</code>\n"
        f"🦔 <b>Last User:</b> <code>{user}</code>\n"
        f"🕒 <b>Last Time:</b> <code>{time}</code>\n"
        f"🌐 <b>Last IP:</b> <code>{ip}</code>\n"
        f"🌍 <b>Location:</b> {geo_str}\n"
        f"🛰️ <b>WHOIS:</b> <code>{whois}</code>"
    )
    await msg.answer(caption)

