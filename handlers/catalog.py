from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import (
    main_menu_kb, categories_kb, products_kb,
    product_card_kb, CategoryCB, ProductCB,
)
from data.catalog import ALL_PRODUCTS, PRODUCTS

router = Router()

# ── /start ────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! 👋\n\n"
        "Добро пожаловать в наш магазин мерча.\n"
        "Выбери раздел в меню ниже 👇",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )

# ── Каталог ───────────────────────────────────────────────────────────────────

@router.message(F.text == "🛍 Каталог")
async def show_catalog(message: Message):
    await message.answer("Выбери категорию:", reply_markup=categories_kb())


@router.callback_query(CategoryCB.filter())
async def show_category(callback: CallbackQuery, callback_data: CategoryCB):
    category = callback_data.category
    await callback.answer()
    await callback.message.edit_text(
        "Товары в категории:",
        reply_markup=products_kb(category),
    )


@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выбери категорию:", reply_markup=categories_kb())


@router.callback_query(ProductCB.filter())
async def show_product(callback: CallbackQuery, callback_data: ProductCB):
    pid = callback_data.product_id
    product = ALL_PRODUCTS.get(pid)
    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    # Находим категорию товара
    category = next(
        (cat for cat, items in PRODUCTS.items() if any(p["id"] == pid for p in items)),
        "hoodies",
    )

    text = (
        f"{product['emoji']} <b>{product['name']}</b>\n\n"
        f"{product['desc']}\n\n"
        f"💰 Цена: <b>{product['price']} ₽</b>"
    )
    await callback.answer()
    await callback.message.edit_text(
        text,
        reply_markup=product_card_kb(pid, category),
        parse_mode="HTML",
    )

# ── О магазине ────────────────────────────────────────────────────────────────

@router.message(F.text == "ℹ️ О магазине")
async def about(message: Message):
    await message.answer(
        "🏪 <b>Мерч Маркет</b>\n\n"
        "Продаём качественный мерч: худи, футболки, аксессуары.\n\n"
        "📦 Доставка по всей России — 3–7 дней\n"
        "💳 Оплата при получении или переводом\n"
        "📞 Поддержка: @support_username",
        parse_mode="HTML",
    )
