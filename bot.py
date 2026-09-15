import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

PRODUCTS = {
    "king": {
        "name": "👑 AIM CARROM KING",
        "plans": [
            ("AUTOPLAY NORMAL", [
                ("3 Days", 250), ("1 Week", 450), ("1 Month", 1250), ("3 Months", 2500)
            ]),
            ("AUTOPLAY QUEUE", [
                ("3 Days", 350), ("1 Week", 550), ("1 Month", 1450), ("3 Months", 3000)
            ]),
        ],
    },
    "snake": {
        "name": "🐍 SNAKE ENGINE",
        "plans": [
            ("AUTOPLAY", [
                ("3 Days", 200), ("10 Days", 500), ("30 Days", 1100), ("90 Days", 2600)
            ]),
        ],
    },
    "aimai": {
        "name": "🤖 AIM AI ENGINE",
        "plans": [
            ("AUTOPLAY", [
                ("1 Day", 120), ("3 Days", 200), ("7 Days", 300),
                ("15 Days", 500), ("30 Days", 850), ("90 Days", 2100)
            ]),
        ],
    },
    "kos": {
        "name": "🎱 KOS ENGINE",
        "plans": [
            ("AUTOPLAY", [
                ("1 Day", 110), ("7 Days", 350), ("15 Days", 570), ("30 Days", 990)
            ]),
        ],
    },
    "bitaim": {
        "name": "🔵 BITAIM+ PREMIUM",
        "plans": [
            ("LINES", [
                ("1 Week", 70), ("1 Month", 170), ("3 Months", 360), ("Lifetime", 1999)
            ]),
        ],
    },
    "lynx": {
        "name": "🔴 LYNX CHEATS",
        "plans": [
            ("AUTOPLAY", [
                ("1 Day", 110), ("3 Days", 190), ("7 Days", 330),
                ("15 Days", 540), ("30 Days", 880)
            ]),
        ],
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍️ PRODUCTS", callback_data="products")],
        [InlineKeyboardButton("📦 MY ORDERS", callback_data="orders")],
        [InlineKeyboardButton("🎮 PLAY CARROM", callback_data="carrom")],
        [InlineKeyboardButton("📜 RULES", callback_data="rules")],
        [InlineKeyboardButton("💬 HELP", callback_data="help")],
    ]

    await update.message.reply_text(
        "👑 APEX GAMING SHOP\n\n"
        "Welcome! 🛍️\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(p["name"], callback_data=f"product_{key}")]
        for key, p in PRODUCTS.items()
    ]

    keyboard.append([InlineKeyboardButton("🔙 BACK", callback_data="home")])

    await query.edit_message_text(
        "🛍️ SELECT A PRODUCT:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def product_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    key = query.data.replace("product_", "")
    product = PRODUCTS[key]

    text = f"{product['name']}\n\n"

    keyboard = []

    for category, plans in product["plans"]:
        text += f"🔹 {category}\n"
        for i, (duration, price) in enumerate(plans):
            text += f"• {duration} — ₹{price}\n"
            keyboard.append([
                InlineKeyboardButton(
                    f"🛒 Buy {duration} ₹{price}",
                    callback_data=f"buy_{key}_{i}_{category.replace(' ', '_')}",
                )
            ])
        text += "\n"

    keyboard.append([
        InlineKeyboardButton("🔙 PRODUCTS", callback_data="products")
    ])

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    key = parts[1]
    index = int(parts[2])

    product = PRODUCTS[key]

    selected_category = None
    selected_plan = None

    for category, plans in product["plans"]:
        if parts[3] == category.replace(" ", "_"):
            selected_category = category
            selected_plan = plans[index]
            break

    if not selected_plan:
        await query.edit_message_text("❌ Plan not found.")
        return

    duration, price = selected_plan

    await query.edit_message_text(
        f"🛒 ORDER DETAILS\n\n"
        f"Product: {product['name']}\n"
        f"Plan: {selected_category}\n"
        f"Duration: {duration}\n"
        f"Price: ₹{price}\n\n"
        f"💳 Payment instructions will be added here.\n\n"
        f"After payment, contact support with your payment proof.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 CONTACT SUPPORT", callback_data="help")],
            [InlineKeyboardButton("🔙 PRODUCTS", callback_data="products")],
        ]),
    )


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📦 MY ORDERS\n\n"
        "You don't have any orders yet.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛍️ PRODUCTS", callback_data="products")],
            [InlineKeyboardButton("🔙 HOME", callback_data="home")],
        ]),
    )


async def carrom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎮 PLAY CARROM\n\n"
        "Carrom game section is coming soon.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 HOME", callback_data="home")]
        ]),
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📜 SHOP RULES\n\n"
        "1️⃣ Check the product and plan carefully.\n"
        "2️⃣ Payment proof may be required.\n"
        "3️⃣ Orders are processed after verification.\n"
        "4️⃣ Contact support if you have any issue.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 HOME", callback_data="home")]
        ]),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "💬 HELP & SUPPORT\n\n"
            "For order or payment support, contact the shop administrator.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 HOME", callback_data="home")]
            ]),
        )
    else:
        await update.message.reply_text(
            "💬 HELP & SUPPORT\n\n"
            "For order or payment support, contact the shop administrator."
        )


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🛍️ PRODUCTS", callback_data="products")],
        [InlineKeyboardButton("📦 MY ORDERS", callback_data="orders")],
        [InlineKeyboardButton("🎮 PLAY CARROM", callback_data="carrom")],
        [InlineKeyboardButton("📜 RULES", callback_data="rules")],
        [InlineKeyboardButton("💬 HELP", callback_data="help")],
    ]

    await query.edit_message_text(
        "👑 APEX GAMING SHOP\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "products":
        await products(update, context)
    elif query.data.startswith("product_"):
        await product_details(update, context)
    elif query.data.startswith("buy_"):
        await buy(update, context)
    elif query.data == "orders":
        await orders(update, context)
    elif query.data == "carrom":
        await carrom(update, context)
    elif query.data == "rules":
        await rules(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "home":
        await home(update, context)


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("APEX GAMING SHOP BOT is starting...")

    app.run_polling()


if __name__ == "__main__":
    main()
