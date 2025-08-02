from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from utils.authlog import search_logins, get_login_count
from utils.glyphs import flag_emoji

router = Router()

def safe_flag(code: str) -> str:
    if not code or len(code) != 2 or not code.isalpha():
        return "🌍"
    return flag_emoji(code)

@router.message(lambda msg: msg.text.startswith("/authgrep") and msg.from_user.id == ADMIN_ID)
async def authgrep(msg: Message):
    args = msg.text.split(maxsplit=1)

    # 🧠 No query — show usage examples
    if len(args) < 2:
        examples = (
            "🧠 <b>AuthGlyph Trace Examples</b>\n\n"
            "Try one of these:\n"
            "• 👤 <code>/authgrep root</code> — by username\n"
            "• 🌐 <code>/authgrep 102.219</code> — by IP fragment\n"
            "• 🧬 <code>/authgrep US</code> — by country code\n"
            "• 🔎 <code>/authgrep adm</code> — partial match\n"
            "• 🔥 <code>/authgrep suspicious</code> — foreign logins only\n\n"
            "📊 Each result shows timestamp, IP, and country flag.\n"
            "🌍 Foreign logins are auto-flagged as suspicious."
        )
        await msg.answer(examples, parse_mode="HTML")
        return

    query = args[1].strip().lower()

    # 🔥 Suspicious mode — filter foreign logins
    if query == "suspicious":
        from utils.authlog import _login_records  # direct access
        matches = [entry for entry in _login_records if entry.get("country", "").upper() != "KE"]
        if not matches:
            await msg.answer("🌍 No suspicious logins found outside Kenya 🇰🇪", parse_mode="HTML")
            return

        lines = [f"🔥 <b>Suspicious Logins</b>",
                 f"🌍 <b>Outside Kenya 🇰🇪</b>",
                 f"📊 <b>Matches:</b> {len(matches)}\n"]

        for entry in matches:
            user = entry['user']
            ip = entry['ip']
            time = entry['time']
            country = entry.get('country', '')
            flag = safe_flag(country)
            lines.append(f"🧍 <b>{user}</b>\n • {time} — <code>{ip}</code> {flag}")

        await msg.answer("\n".join(lines), parse_mode="HTML")
        return

    # 🔍 Normal grep mode
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
        flag = safe_flag(country)
        lines.append(f"🧍 <b>{user}</b>\n • {time} — <code>{ip}</code> {flag}")

    await msg.answer("\n".join(lines), parse_mode="HTML")

