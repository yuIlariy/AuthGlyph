import random

themes = [
    "🦔 <b>Sentinel Mode</b>",
    "🌋 <b>Breach Watch</b>",
    "🧊 <b>Frost Login</b>",
    "🌪️ <b>Storm Access</b>",
    "🛡️ <b>Guardian Alert</b>",
    "🕵️ <b>Shadow Trace</b>",
    "⚡ <b>Pulse Entry</b>",
]

def themed_caption(ip, user, time, geo):
    theme = random.choice(themes)
    return (
        f"{theme}\n"
        f"👤 <b>User:</b> <code>{user}</code>\n"
        f"🕒 <b>Time:</b> <code>{time}</code>\n"
        f"🌍 <b>IP:</b> <code>{ip}</code>\n"
        f"📍 <b>Location:</b> {geo}"
    )
