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

SITE_URL = "https://europe-times.net/"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()
BRAND = "Europe Times"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# HELPERS
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def site_btn():
    return types.InlineKeyboardButton(
        text=f"🌐 Open {BRAND}",
        url=SITE_URL,
    )


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [button for button in row if button is not None]
        if row:
            markup.row(*row)
    return markup


BTN_HEADLINES = ("📋 Today's stories", "headlines")
BTN_MENU = ("🗂 Contents", "menu")


def article_rows():
    return [
        [site_btn()],
        [btn(*BTN_HEADLINES), btn(*BTN_MENU)],
    ]


# ============================================
# SCREEN TEXTS
# ============================================
TEXT_START = (
    f"🇧🇪 <b>Welcome to {BRAND}!</b>\n\n"
    "<i>A small seasonal guide to culture, food and travel in Belgium.</i>\n\n"
    "Each season, a short selection of reads to enjoy right here in the chat.\n\n"
    "To begin, tap <b>Today's stories</b>."
)

TEXT_HEADLINES = (
    "📋 <b>Today's stories</b>\n\n"
    "Three reads picked for today, each available in full in the chat.\n\n"
    "<b>Culture</b> — five exhibitions to see this autumn.\n\n"
    "<b>Food</b> — four classic Belgian recipes.\n\n"
    "<b>Travel</b> — five villages for a weekend away.\n\n"
    "Tap a title to open the article."
)

TEXT_CULTURE = (
    "🎨 <b>Five exhibitions to see this autumn</b>\n\n"
    "<b>Brussels — Magritte and Surrealism</b>\n"
    "The Magritte Museum presents a retrospective with rarely shown "
    "works on loan from private collections. A dialogue between dream "
    "and reality.\n\n"
    "<b>Antwerp — Rubens Rediscovered</b>\n"
    "The Royal Museum of Fine Arts offers a fresh look at Rubens "
    "through modern restoration techniques. Details unseen for four "
    "centuries.\n\n"
    "<b>Ghent — Flemish Contemporary Art</b>\n"
    "S.M.A.K. hosts a new generation of Belgian artists. Installation, "
    "video and sculpture in dialogue with the permanent collection.\n\n"
    "<b>Liège — Industrial Photography</b>\n"
    "La Boverie presents a century of images from the Walloon steel "
    "basin. A documentary and poetic look at a vanished world.\n\n"
    "<b>Bruges — Medieval Manuscripts</b>\n"
    "The Groeningemuseum unveils illuminated manuscripts from the "
    "15th century. A rare chance to see treasures usually kept in "
    "storage.\n\n"
    "<i>Dates and opening hours: please check the museums' official sites.</i>"
)

TEXT_CUISINE = (
    "🍺 <b>Four classic Belgian recipes</b>\n\n"
    "<b>Flemish carbonade</b>\n"
    "Beef slow-cooked in brown ale with gingerbread and mustard. "
    "Two hours of gentle cooking. Serve with fries, of course.\n\n"
    "<b>Mussels and fries</b>\n"
    "Fresh mussels cooked in white wine with celery, onion and "
    "parsley. Belgian fries are cut thick and fried twice. The "
    "national dish.\n\n"
    "<b>Ghent waterzooi</b>\n"
    "A creamy stew of chicken or fish with carrots, leeks and "
    "potatoes. From Ghent, the ultimate comfort food for autumn days.\n\n"
    "<b>Liège waffles</b>\n"
    "Brioche-style dough with pearl sugar, cooked until caramelised. "
    "Irresistible while warm. The secret: good butter.\n\n"
    "<i>Amounts and cooking times can be adjusted to taste.</i>"
)

TEXT_TRAVEL = (
    "🏠 <b>Five villages for an autumn weekend</b>\n\n"
    "<b>Durbuy (Luxembourg province)</b>\n"
    "Said to be the smallest town in the world. Medieval lanes, fine "
    "dining and the topiary park. Perfect for a weekend for two.\n\n"
    "<b>Crupet (Namur province)</b>\n"
    "A postcard village with its 12th-century keep and a grotto "
    "dedicated to Saint Anthony. The autumn colours are spectacular.\n\n"
    "<b>Torgny (Luxembourg province)</b>\n"
    "Belgium's southernmost village. Roman-tiled roofs, vineyards and "
    "a surprisingly mild microclimate.\n\n"
    "<b>Redu (Luxembourg province)</b>\n"
    "The book village: many second-hand booksellers in a tiny place. "
    "Literary browsing and walks in the Ardennes forest.\n\n"
    "<b>Foy-Notre-Dame (Namur province)</b>\n"
    "A hamlet around a 17th-century church with a remarkable painted "
    "ceiling. Hiking trails across the wooded hills of the Meuse.\n\n"
    "<i>For lodging, midweek booking is recommended.</i>"
)

TEXT_MENU = (
    "🗂 <b>Contents</b>\n\n"
    "From this menu you can:\n\n"
    "• Read <b>today's stories</b> and the articles, right here.\n"
    "• Browse the sections: Culture, Food, Travel.\n"
    "• Check the glossary and frequently asked questions.\n"
    "• Learn more about the project and get in touch."
)

TEXT_GLOSSARY = (
    "📖 <b>Little glossary</b>\n\n"
    "<b>Beguinage</b> — a cluster of houses around a courtyard where "
    "the Beguines once lived. Several are UNESCO-listed.\n\n"
    "<b>Estaminet</b> — a traditional, cosy and unpretentious café, "
    "typical of Flanders and the north.\n\n"
    "<b>Kermesse</b> — a village fair with a funfair, music and local "
    "specialities.\n\n"
    "<b>Speculoos</b> — a spiced cinnamon biscuit, a Belgian emblem.\n\n"
    "<b>Ducasse</b> — a local Walloon festival, often with processions "
    "and giant figures.\n\n"
    "<b>Zwanze</b> — Brussels humour: teasing and self-deprecating."
)

TEXT_FAQ = (
    "❓ <b>Frequently asked questions</b>\n\n"
    "<b>Is this bot official?</b>\n"
    "It is an editorial project of the team behind it. It never asks "
    "for passwords, verification codes or card details in the chat.\n\n"
    "<b>How often is it updated?</b>\n"
    "The selection of articles is refreshed each season.\n\n"
    "<b>How do I mute notifications?</b>\n"
    "From the Telegram chat settings you can mute or disable "
    "notifications.\n\n"
    "<b>Can I share an article?</b>\n"
    "Yes. Use Telegram's forward function."
)

TEXT_ABOUT = (
    f"ℹ️ <b>About {BRAND}</b>\n\n"
    f"{BRAND} gathers, each season, a few reads about Belgium: "
    "museums, traditional food and beautiful places to visit.\n\n"
    "The idea is simple: short, pleasant texts to read right in "
    "Telegram, without ads and without rushing."
)


def contact_text():
    email_line = (
        f"• E-mail: {CONTACT_EMAIL}\n\n"
        if CONTACT_EMAIL
        else "• A contact address will be added soon.\n\n"
    )
    return (
        "✏️ <b>Contact</b>\n\n"
        "For suggestions, corrections or article ideas:\n"
        + email_line
        + "Thank you for every message!"
    )


# ============================================
# SCREENS: callback_data -> (text, buttons)
# ============================================
SCREENS = {
    "headlines": (
        TEXT_HEADLINES,
        [
            [btn("🎨 Culture — autumn exhibitions", "culture")],
            [btn("🍺 Food — classic recipes", "cuisine")],
            [btn("🏠 Travel — five villages", "travel")],
            [btn(*BTN_MENU)],
        ],
    ),
    "culture": (TEXT_CULTURE, article_rows()),
    "cuisine": (TEXT_CUISINE, article_rows()),
    "travel": (TEXT_TRAVEL, article_rows()),
    "menu": (
        TEXT_MENU,
        [
            [site_btn()],
            [btn(*BTN_HEADLINES)],
            [btn("📖 Glossary", "glossary"), btn("❓ FAQ", "faq")],
            [btn("✏️ Contact", "contact"), btn("ℹ️ About", "about")],
        ],
    ),
    "glossary": (TEXT_GLOSSARY, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "faq": (TEXT_FAQ, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "contact": (
        contact_text(),
        [[btn(*BTN_MENU), btn("ℹ️ About", "about")]],
    ),
    "about": (
        TEXT_ABOUT,
        [[site_btn()], [btn(*BTN_MENU), btn("✏️ Contact", "contact")]],
    ),
}


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = make_markup([[site_btn()], [btn(*BTN_HEADLINES), btn(*BTN_MENU)]])
    bot.send_message(message.chat.id, TEXT_START, reply_markup=markup)


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
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.set_chat_menu_button(menu_button=types.MenuButtonDefault(type="default"))

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
