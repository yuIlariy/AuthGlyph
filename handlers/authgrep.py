from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from utils.authlog import search_logins
from utils.glyphs import flag_emoji

router = Router()

@router.message(lambda msg: msg.text.startswith("/authgrep") and msg.from_user.id == ADMIN_ID)
async def authgrep(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        await msg.answer("🧠 Usage: <code>/authgrep &lt;query&gt;</code>", parse_mode="HTML")
        return

    query = args[1].strip()
    matches = search_logins(query)

    if not matches:
        await msg.answer(f"🔍 No matches found for <code>{query}</code>", parse_mode="HTML")
        return

    lines = [f"🧠 <b>AuthGlyph Trace</b>",
             f"🔍 <b>Query:</b> <code>{query}</code>",
             f"📊 <b>Matches:</b> {len(matches)}\n"]

    for entry in matches:
        user = entry['user']
        ip = entry['ip']
        time = entry['time']
        country = entry.get('country', '')
        flag = flag_emoji(country)
        lines.append(f"🧍 <b>{user}</b>\n • {time} — <code>{ip}</code> {flag}")

    await msg.answer("\n".join(lines), parse_mode="HTML")

