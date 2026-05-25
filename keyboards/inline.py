from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from data.catalog import CATEGORIES, PRODUCTS, ALL_PRODUCTS


# ── CallbackData фабрики ──────────────────────────────────────────────────────

class CategoryCB(CallbackData, prefix="cat"):
    category: str

class ProductCB(CallbackData, prefix="prod"):
    product_id: str

class CartCB(CallbackData, prefix="cart"):
    action: str        # "add", "remove", "clear", "view", "checkout"
    product_id: str = ""


# ── Главное меню (reply) ──────────────────────────────────────────────────────

def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🛍 Каталог")
    builder.button(text="🛒 Корзина")
    builder.button(text="📦 Мои заказы")
    builder.button(text="ℹ️ О магазине")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


# ── Категории ─────────────────────────────────────────────────────────────────

def categories_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, name in CATEGORIES.items():
        builder.button(text=name, callback_data=CategoryCB(category=key))
    builder.adjust(1)
    return builder.as_markup()


# ── Список товаров категории ──────────────────────────────────────────────────

def products_kb(category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in PRODUCTS.get(category, []):
        builder.button(
            text=f"{p['emoji']} {p['name']} — {p['price']} ₽",
            callback_data=ProductCB(product_id=p["id"]),
        )
    builder.button(text="⬅️ Назад", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()


# ── Карточка товара ───────────────────────────────────────────────────────────

def product_card_kb(product_id: str, category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛒 Добавить в корзину",
        callback_data=CartCB(action="add", product_id=product_id),
    )
    builder.button(
        text="⬅️ Назад к категории",
        callback_data=CategoryCB(category=category),
    )
    builder.adjust(1)
    return builder.as_markup()


# ── Корзина ───────────────────────────────────────────────────────────────────

def cart_kb(cart: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for pid in cart:
        p = ALL_PRODUCTS.get(pid)
        if p:
            builder.button(
                text=f"❌ Убрать «{p['name']}»",
                callback_data=CartCB(action="remove", product_id=pid),
            )
    builder.button(text="🗑 Очистить корзину", callback_data=CartCB(action="clear"))
    builder.button(text="✅ Оформить заказ", callback_data=CartCB(action="checkout"))
    builder.adjust(1)
    return builder.as_markup()


# ── Подтверждение заказа ──────────────────────────────────────────────────────

def confirm_order_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="order_confirm")
    builder.button(text="✏️ Изменить", callback_data="order_edit")
    builder.adjust(2)
    return builder.as_markup()


# ── Кнопка отмены во время оформления ────────────────────────────────────────

def cancel_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True)
