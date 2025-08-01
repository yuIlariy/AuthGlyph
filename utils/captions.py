import random

themes = [
    "🦔 <b>Sentinel Mode</b>",
    "🌋 <b>Breach Watch</b>",
    "🧊 <b>Frost Login</b>",
    "🌪️ <b>Storm Access</b>",
    "🛡️ <b>Guardian Alert</b>",
    "🕵️ <b>Shadow Trace</b>",
    "⚡ <b>Pulse Entry</b>",
    "🧠 <b>Neural Breach</b>",
    "🛰️ <b>Orbital Ping</b>",
    "🧨 <b>Exploit Triggered</b>",
    "🪓 <b>Root Chop</b>",
    "🧬 <b>Genome Access</b>",
    "🧱 <b>Firewall Breach</b>",
    "🧿 <b>Watcher Glyph</b>",
    "🪐 <b>Cosmic Login</b>",
    "🧛 <b>Vampire Session</b>",
    "🧟 <b>Zombie Shell</b>",
    "🧳 <b>Traveler Login</b>",
    "🧭 <b>Compass Trace</b>",
    "🧰 <b>Toolchain Entry</b>",
    "🧗 <b>Climber Access</b>",
    "🧼 <b>Clean Shell</b>",
    "🧱 <b>Bricklayer Mode</b>",
    "🧞 <b>Wishful Login</b>",
    "🧙 <b>Wizard Shell</b>",
    "🧚 <b>Fairy Ping</b>",
    "🧜 <b>Deep Sea Login</b>",
    "🧀 <b>Cheesy Breach</b>",
    "🧊 <b>Glacier Trace</b>",
    "🧨 <b>Detonator Ping</b>",
    "🧵 <b>Threaded Entry</b>",
    "🧹 <b>Sweeper Login</b>",
    "🧺 <b>Basket Shell</b>",
    "🧼 <b>Sanitized Access</b>",
    "🧯 <b>Extinguisher Mode</b>",
    "🧪 <b>Lab Session</b>",
    "🧫 <b>Petri Login</b>",
    "🧬 <b>DNA Trace</b>",
]

def themed_caption(ip, user, time, geo):
    theme = random.choice(themes)
    return (
        f"{theme}\n"
        f"👤 <b>User:</b> <code>{user}</code>\n"
        f"🕒 <b>Time:</b> <code>{time}</code>\n"
        f"🌐 <b>IP:</b> <code>{ip}</code>\n"
        f"🌍 <b>Location:</b> {geo}"
    )

