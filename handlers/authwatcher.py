from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from utils.authlog import get_last_login, geo_lookup
from utils.captions import themed_caption

router = Router()

@router.message(lambda msg: msg.text == "/authstats" and msg.from_user.id == ADMIN_ID)
async def authstats(msg: Message):
    ip, user, time = get_last_login()
    geo_str, _, whois = geo_lookup(ip)  # ✅ WHOIS from geo_lookup
    caption = themed_caption(ip, user, time, geo_str, whois)
    await msg.answer(caption)
    
