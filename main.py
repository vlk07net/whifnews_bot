import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# SETTINGS
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

SITE_URL = "https://www.whifnews.com/"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()
BRAND = "WHIF"
BRAND_FULL = "WHIF — What's happening in France"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# HELPERS
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def site_btn():
    # Secondary action only: shown in Contents and About, never on guide pages.
    return types.InlineKeyboardButton(text=f"🌐 {BRAND} website", url=SITE_URL)


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [b for b in row if b is not None]
        if row:
            markup.row(*row)
    return markup


BTN_GUIDE = ("🧭 The guide", "guide")
BTN_MENU = ("🗂 Contents", "menu")


def guide_page_rows(next_key=None, next_label=None):
    rows = []
    if next_key:
        rows.append([btn(f"➡️ Next: {next_label}", next_key)])
    rows.append([btn(*BTN_GUIDE), btn(*BTN_MENU)])
    return rows


# ============================================
# SCREEN TEXTS
# ============================================
TEXT_START = (
    f"🇫🇷 <b>Welcome to {BRAND}!</b>\n\n"
    "<i>A pocket guide to France, right here in Telegram.</i>\n\n"
    "Sights, regions, food and practical tips for your trip — "
    "short, readable chapters you can open without leaving the chat.\n\n"
    "To begin, tap <b>The guide</b>."
)

TEXT_GUIDE = (
    "🧭 <b>The guide</b>\n\n"
    "Six short chapters about France, all readable in the chat:\n\n"
    "🗼 <b>Paris</b> — the essentials in a few days.\n"
    "🏰 <b>Regions</b> — where to go beyond the capital.\n"
    "🏡 <b>Villages</b> — five places for a quiet weekend.\n"
    "🥐 <b>Food</b> — dishes to try and how French meals work.\n"
    "🚆 <b>Getting around</b> — trains, cars and cities.\n"
    "💡 <b>Good to know</b> — etiquette, money and everyday tips.\n\n"
    "Tap a chapter to open it."
)

TEXT_PARIS = (
    "🗼 <b>Paris: the essentials</b>\n\n"
    "<b>The Louvre and the Tuileries</b>\n"
    "One of the largest museums in the world. Pick one or two wings "
    "rather than trying to see everything, and book a time slot ahead.\n\n"
    "<b>Musée d'Orsay</b>\n"
    "A former railway station full of Impressionist paintings: Monet, "
    "Renoir, Degas, Van Gogh. Smaller and calmer than the Louvre.\n\n"
    "<b>Le Marais</b>\n"
    "Old mansions, small museums, the Place des Vosges and some of the "
    "best falafel in the city. Best explored on foot.\n\n"
    "<b>Montmartre</b>\n"
    "The hill of Sacré-Cœur, with village-like streets and a wide view "
    "over the rooftops. Go early in the morning to avoid the crowds.\n\n"
    "<b>The Seine at dusk</b>\n"
    "Walk from Notre-Dame towards the Eiffel Tower along the quays — "
    "the classic free way to see the city.\n\n"
    "<i>Opening hours and prices change: check official sites before you go.</i>"
)

TEXT_REGIONS = (
    "🏰 <b>Regions beyond Paris</b>\n\n"
    "<b>Loire Valley</b>\n"
    "Renaissance châteaux such as Chambord and Chenonceau, vineyards "
    "and flat cycling routes along the river.\n\n"
    "<b>Provence</b>\n"
    "Lavender fields in early summer, hilltop villages, Roman heritage "
    "in Arles and Nîmes, and the markets of Aix-en-Provence.\n\n"
    "<b>Normandy</b>\n"
    "Mont-Saint-Michel, the D-Day beaches, half-timbered Honfleur and "
    "the cliffs of Étretat. Cider and Camembert country.\n\n"
    "<b>Alsace</b>\n"
    "Colourful towns like Colmar, a wine route through the vineyards "
    "and a cuisine that mixes French and German influences.\n\n"
    "<b>The Alps</b>\n"
    "Skiing in winter, lakes and hiking in summer. Annecy is an easy "
    "and beautiful starting point."
)

TEXT_VILLAGES = (
    "🏡 <b>Five villages for a weekend</b>\n\n"
    "<b>Gordes (Provence)</b>\n"
    "Stone houses stacked on a hillside above the Luberon valley. "
    "The nearby Sénanque Abbey is famous for its lavender.\n\n"
    "<b>Rocamadour (Occitanie)</b>\n"
    "A pilgrimage village built into a cliff above a canyon. "
    "Spectacular at night when it is lit up.\n\n"
    "<b>Eguisheim (Alsace)</b>\n"
    "Concentric cobbled lanes, flower-covered houses and wine "
    "cellars. A short drive from Colmar.\n\n"
    "<b>Saint-Cirq-Lapopie (Occitanie)</b>\n"
    "A medieval village perched above the Lot river, with views "
    "that reward the climb.\n\n"
    "<b>Yvoire (Haute-Savoie)</b>\n"
    "A small fortified village on the shore of Lake Geneva, with a "
    "garden of the five senses.\n\n"
    "<i>Weekends and summer are busy: arrive early or stay overnight.</i>"
)

TEXT_FOOD = (
    "🥐 <b>Food: what to try</b>\n\n"
    "<b>At the bakery</b>\n"
    "A fresh baguette, croissants and pains au chocolat in the "
    "morning. Look for bakeries that bake on site.\n\n"
    "<b>Classic dishes</b>\n"
    "Bœuf bourguignon (beef stewed in red wine), coq au vin, "
    "ratatouille, quiche lorraine and, in Marseille, bouillabaisse.\n\n"
    "<b>Cheese</b>\n"
    "France has hundreds of cheeses. Start with Comté, Brie, "
    "Roquefort and a fresh goat's cheese.\n\n"
    "<b>Crêpes and galettes</b>\n"
    "From Brittany: sweet crêpes and savoury buckwheat galettes, "
    "traditionally with a bowl of cider.\n\n"
    "<b>How meals work</b>\n"
    "Lunch is often the main meal, and many restaurants offer a set "
    "menu (<i>formule</i>) at midday. Dinner usually starts around "
    "19:30–20:00."
)

TEXT_TRANSPORT = (
    "🚆 <b>Getting around</b>\n\n"
    "<b>High-speed trains</b>\n"
    "TGV trains connect Paris with Lyon, Marseille, Bordeaux, "
    "Strasbourg and more in a few hours. Book early for lower fares.\n\n"
    "<b>Regional trains</b>\n"
    "TER trains serve smaller towns. Great for day trips from "
    "regional cities.\n\n"
    "<b>In Paris</b>\n"
    "The metro is the fastest way around. Walking between central "
    "districts is often just as pleasant.\n\n"
    "<b>By car</b>\n"
    "Best for villages and the countryside. Motorways usually have "
    "tolls (<i>péage</i>), and city centres can be hard to park in.\n\n"
    "<b>By bike</b>\n"
    "Many cities have bike-share schemes, and there are long "
    "cycling routes along the Loire and the Atlantic coast."
)

TEXT_TIPS = (
    "💡 <b>Good to know</b>\n\n"
    "<b>Say bonjour</b>\n"
    "Greet people when you enter a shop or café. A simple "
    "\"Bonjour\" makes a real difference.\n\n"
    "<b>Money</b>\n"
    "The currency is the euro. Cards are widely accepted, but keep "
    "a little cash for markets and small cafés.\n\n"
    "<b>Tipping</b>\n"
    "Service is included in restaurant prices. Leaving small change "
    "for good service is a nice gesture, not an obligation.\n\n"
    "<b>Opening hours</b>\n"
    "In smaller towns, many shops close at lunchtime and on Sundays. "
    "Some museums close one day a week.\n\n"
    "<b>Water</b>\n"
    "Tap water is safe to drink. Ask for <i>une carafe d'eau</i> "
    "in restaurants — it's free."
)

TEXT_MENU = (
    "🗂 <b>Contents</b>\n\n"
    "From this menu you can:\n\n"
    "• Read <b>the guide</b> to France, right here in the chat.\n"
    "• Check the glossary and frequently asked questions.\n"
    "• Learn more about the project and get in touch.\n\n"
    f"For news about France in English, you can also visit the "
    f"<b>{BRAND}</b> website."
)

TEXT_GLOSSARY = (
    "📖 <b>Little glossary</b>\n\n"
    "<b>Boulangerie</b> — a bakery that bakes bread on site.\n\n"
    "<b>Brasserie</b> — a relaxed restaurant with long opening hours "
    "and classic dishes.\n\n"
    "<b>Formule</b> — a fixed-price set menu, often at lunchtime.\n\n"
    "<b>Marché</b> — an open-air market, usually held on set "
    "mornings each week.\n\n"
    "<b>Péage</b> — a motorway toll.\n\n"
    "<b>Apéro</b> — a pre-dinner drink with small snacks, a much-"
    "loved French ritual."
)

TEXT_FAQ = (
    "❓ <b>Frequently asked questions</b>\n\n"
    "<b>What is this bot?</b>\n"
    f"A travel guide to France by the team behind {BRAND}. Everything "
    "you need is readable right here in the chat.\n\n"
    "<b>Does it ask for personal data?</b>\n"
    "No. It never asks for passwords, verification codes or card "
    "details.\n\n"
    "<b>How do I mute notifications?</b>\n"
    "Use the Telegram chat settings to mute or disable them.\n\n"
    "<b>Can I share a chapter?</b>\n"
    "Yes, use Telegram's forward function."
)

TEXT_ABOUT = (
    f"ℹ️ <b>About {BRAND}</b>\n\n"
    f"<b>{BRAND_FULL}</b> is an English-language edition about France: "
    "news, culture and everyday life.\n\n"
    "This bot is our pocket travel guide: short, practical chapters "
    "about places, food and getting around, to read in Telegram "
    "without ads."
)


def contact_text():
    email_line = (
        f"• E-mail: {CONTACT_EMAIL}\n\n"
        if CONTACT_EMAIL
        else "• A contact address will be added soon.\n\n"
    )
    return (
        "✏️ <b>Contact</b>\n\n"
        "For suggestions, corrections or ideas for new chapters:\n"
        + email_line
        + "Thank you for every message!"
    )


# ============================================
# SCREENS: callback_data -> (text, buttons)
# ============================================
SCREENS = {
    "guide": (
        TEXT_GUIDE,
        [
            [btn("🗼 Paris", "paris"), btn("🏰 Regions", "regions")],
            [btn("🏡 Villages", "villages"), btn("🥐 Food", "food")],
            [btn("🚆 Getting around", "transport"), btn("💡 Good to know", "tips")],
            [btn(*BTN_MENU)],
        ],
    ),
    "paris": (TEXT_PARIS, guide_page_rows("regions", "Regions")),
    "regions": (TEXT_REGIONS, guide_page_rows("villages", "Villages")),
    "villages": (TEXT_VILLAGES, guide_page_rows("food", "Food")),
    "food": (TEXT_FOOD, guide_page_rows("transport", "Getting around")),
    "transport": (TEXT_TRANSPORT, guide_page_rows("tips", "Good to know")),
    "tips": (TEXT_TIPS, guide_page_rows()),
    "menu": (
        TEXT_MENU,
        [
            [btn(*BTN_GUIDE)],
            [btn("📖 Glossary", "glossary"), btn("❓ FAQ", "faq")],
            [btn("✏️ Contact", "contact"), btn("ℹ️ About", "about")],
            [site_btn()],
        ],
    ),
    "glossary": (TEXT_GLOSSARY, [[btn(*BTN_GUIDE), btn(*BTN_MENU)]]),
    "faq": (TEXT_FAQ, [[btn(*BTN_GUIDE), btn(*BTN_MENU)]]),
    "contact": (contact_text(), [[btn(*BTN_MENU), btn("ℹ️ About", "about")]]),
    "about": (
        TEXT_ABOUT,
        [[btn(*BTN_GUIDE)], [btn(*BTN_MENU), btn("✏️ Contact", "contact")], [site_btn()]],
    ),
}


def start_markup():
    return make_markup([[btn(*BTN_GUIDE)], [btn(*BTN_MENU)]])


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, TEXT_START, reply_markup=start_markup())


@bot.message_handler(commands=["guide", "menu"])
def open_screen_command(message):
    key = message.text.split()[0].lstrip("/").split("@")[0]
    text, rows = SCREENS[key]
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


@bot.callback_query_handler(func=lambda call: call.data in SCREENS)
def show_screen(call):
    bot.answer_callback_query(call.id)
    text, rows = SCREENS[call.data]
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    except ApiTelegramException as e:
        if "message is not modified" in str(e):
            return  # same screen tapped twice: nothing to do
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def unknown_callback(call):
    bot.answer_callback_query(call.id, "This button is outdated. Send /start.")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Use the buttons below to open the guide 👇",
        reply_markup=start_markup(),
    )


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("guide", "Open the France guide"),
        types.BotCommand("menu", "Contents"),
    ])
    bot.set_chat_menu_button(menu_button=types.MenuButtonCommands(type="commands"))

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
