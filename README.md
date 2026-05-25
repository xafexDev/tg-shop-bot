# Telegram Shop Bot

A Telegram bot for a merch store built with [aiogram 3](https://docs.aiogram.dev/). Covers the full purchase flow: browsing a catalog, managing a cart, placing an order, and notifying the store admin.

---

## Screenshots

<table>
  <tr>
    <td align="center"><b>Main menu</b></td>
    <td align="center"><b>Catalog</b></td>
    <td align="center"><b>Product card</b></td>
    <td align="center"><b>Checkout</b></td>
  </tr>
  <tr>
    <td><img src="img/image.png" width="200"/></td>
    <td><img src="img/image copy.png" width="200"/></td>
    <td><img src="img/image copy 2.png" width="200"/></td>
    <td><img src="img/image copy 3.png" width="200"/></td>
  </tr>
</table>

---

## Features

- Inline-button catalog with categories and product cards
- Persistent cart — add, remove, and clear items across messages
- Multi-step checkout flow using aiogram FSM (name, phone, delivery address, confirmation)
- Admin notification on every confirmed order
- Reply keyboard for main navigation

---

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| [aiogram](https://docs.aiogram.dev/) | 3.28 | Telegram Bot API framework |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0 | Environment variable loading |

---

## Project Structure

```
.
├── bot.py              # Entry point, polling setup
├── config.py           # Environment config
├── requirements.txt
├── env.example
├── data/
│   └── catalog.py      # Product catalog data
├── handlers/
│   ├── catalog.py      # Start command, catalog, product card
│   └── cart.py         # Cart management, FSM checkout
├── keyboards/
│   └── inline.py       # All keyboards and CallbackData factories
└── states/
    └── order.py        # FSM state groups
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/your-username/merch-bot.git
cd merch-bot
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

```bash
cp env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_ID=123456789
```

- `BOT_TOKEN` — get from [@BotFather](https://t.me/BotFather)
- `ADMIN_ID` — your Telegram user ID ([@userinfobot](https://t.me/userinfobot))

**4. Run**

```bash
python bot.py
```

---

## Adding Products

All catalog data lives in `data/catalog.py`. Add a new item to the relevant category list:

```python
PRODUCTS = {
    "hoodies": [
        {
            "id": "h4",
            "name": "Hoodie Crop Black",
            "price": 2800,
            "desc": "Cropped fit, 300 g/m2 cotton. Sizes XS–L.",
            "emoji": "🖤",
        },
    ],
}
```

To add a new category, register it in `CATEGORIES` and add a matching key in `PRODUCTS`.

---

## Roadmap

- [ ] Size selection per product
- [ ] Product photos
- [ ] Payment integration (YooKassa / Stripe)
- [ ] Order history with persistent storage
- [ ] Admin panel for order management

---

## License

MIT
