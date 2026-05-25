from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.inline import cart_kb, confirm_order_kb, cancel_kb, main_menu_kb, CartCB
from data.catalog import ALL_PRODUCTS
from states.order import OrderStates
from config import ADMIN_ID

router = Router()


# ── Хелперы корзины ───────────────────────────────────────────────────────────

async def get_cart(state: FSMContext) -> dict:
    data = await state.get_data()
    return data.get("cart", {})

async def set_cart(state: FSMContext, cart: dict):
    await state.update_data(cart=cart)

def cart_text(cart: dict) -> str:
    if not cart:
        return "🛒 Корзина пуста"
    lines = ["🛒 <b>Твоя корзина:</b>\n"]
    total = 0
    for pid, qty in cart.items():
        p = ALL_PRODUCTS.get(pid)
        if p:
            subtotal = p["price"] * qty
            total += subtotal
            lines.append(f"• {p['emoji']} {p['name']} × {qty} = <b>{subtotal} ₽</b>")
    lines.append(f"\n💰 Итого: <b>{total} ₽</b>")
    return "\n".join(lines)


# ── Добавление в корзину ──────────────────────────────────────────────────────

@router.callback_query(CartCB.filter(F.action == "add"))
async def cart_add(callback: CallbackQuery, callback_data: CartCB, state: FSMContext):
    pid = callback_data.product_id
    product = ALL_PRODUCTS.get(pid)
    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    cart = await get_cart(state)
    cart[pid] = cart.get(pid, 0) + 1
    await set_cart(state, cart)

    await callback.answer(f"✅ «{product['name']}» добавлен в корзину!")


# ── Просмотр корзины ──────────────────────────────────────────────────────────

@router.message(F.text == "🛒 Корзина")
async def show_cart(message: Message, state: FSMContext):
    cart = await get_cart(state)
    text = cart_text(cart)
    if cart:
        await message.answer(text, reply_markup=cart_kb(cart), parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")


@router.callback_query(CartCB.filter(F.action == "view"))
async def view_cart_cb(callback: CallbackQuery, state: FSMContext):
    cart = await get_cart(state)
    await callback.answer()
    await callback.message.edit_text(
        cart_text(cart),
        reply_markup=cart_kb(cart) if cart else None,
        parse_mode="HTML",
    )


# ── Удаление из корзины ───────────────────────────────────────────────────────

@router.callback_query(CartCB.filter(F.action == "remove"))
async def cart_remove(callback: CallbackQuery, callback_data: CartCB, state: FSMContext):
    pid = callback_data.product_id
    cart = await get_cart(state)
    cart.pop(pid, None)
    await set_cart(state, cart)
    await callback.answer("Удалено")
    text = cart_text(cart)
    await callback.message.edit_text(
        text,
        reply_markup=cart_kb(cart) if cart else None,
        parse_mode="HTML",
    )


@router.callback_query(CartCB.filter(F.action == "clear"))
async def cart_clear(callback: CallbackQuery, state: FSMContext):
    await set_cart(state, {})
    await callback.answer("Корзина очищена")
    await callback.message.edit_text("🛒 Корзина пуста")


# ── Оформление заказа (FSM) ───────────────────────────────────────────────────

@router.callback_query(CartCB.filter(F.action == "checkout"))
async def checkout_start(callback: CallbackQuery, state: FSMContext):
    cart = await get_cart(state)
    if not cart:
        await callback.answer("Корзина пуста!", show_alert=True)
        return
    await callback.answer()
    await state.set_state(OrderStates.waiting_name)
    await callback.message.answer(
        "📝 Оформляем заказ!\n\nВведи своё <b>имя и фамилию</b>:",
        reply_markup=cancel_kb(),
        parse_mode="HTML",
    )


@router.message(OrderStates.waiting_name)
async def order_name(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.set_state(None)
        await message.answer("Оформление отменено.", reply_markup=main_menu_kb())
        return
    await state.update_data(customer_name=message.text)
    await state.set_state(OrderStates.waiting_phone)
    await message.answer("📱 Введи <b>номер телефона</b> (например: +79991234567):", parse_mode="HTML")


@router.message(OrderStates.waiting_phone)
async def order_phone(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.set_state(None)
        await message.answer("Оформление отменено.", reply_markup=main_menu_kb())
        return
    phone = message.text.strip()
    if not (phone.startswith("+") and len(phone) >= 11):
        await message.answer("Неверный формат. Введи номер в формате +79991234567")
        return
    await state.update_data(customer_phone=phone)
    await state.set_state(OrderStates.waiting_address)
    await message.answer("📍 Введи <b>адрес доставки</b> (город, улица, дом, квартира):", parse_mode="HTML")


@router.message(OrderStates.waiting_address)
async def order_address(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.set_state(None)
        await message.answer("Оформление отменено.", reply_markup=main_menu_kb())
        return
    await state.update_data(customer_address=message.text)

    data = await state.get_data()
    cart = data.get("cart", {})

    # Собираем итоговое сообщение
    items_text = "\n".join(
        f"• {ALL_PRODUCTS[pid]['emoji']} {ALL_PRODUCTS[pid]['name']} × {qty} = {ALL_PRODUCTS[pid]['price'] * qty} ₽"
        for pid, qty in cart.items()
        if pid in ALL_PRODUCTS
    )
    total = sum(ALL_PRODUCTS[pid]["price"] * qty for pid, qty in cart.items() if pid in ALL_PRODUCTS)

    summary = (
        f"📋 <b>Проверь заказ:</b>\n\n"
        f"👤 Имя: {data['customer_name']}\n"
        f"📱 Телефон: {data['customer_phone']}\n"
        f"📍 Адрес: {data['customer_address']}\n\n"
        f"<b>Товары:</b>\n{items_text}\n\n"
        f"💰 Итого: <b>{total} ₽</b>"
    )

    await state.set_state(OrderStates.waiting_confirm)
    await message.answer(summary, reply_markup=confirm_order_kb(), parse_mode="HTML")


@router.callback_query(F.data == "order_confirm")
async def order_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    cart = data.get("cart", {})

    items_text = "\n".join(
        f"• {ALL_PRODUCTS[pid]['name']} × {qty} = {ALL_PRODUCTS[pid]['price'] * qty} ₽"
        for pid, qty in cart.items()
        if pid in ALL_PRODUCTS
    )
    total = sum(ALL_PRODUCTS[pid]["price"] * qty for pid, qty in cart.items() if pid in ALL_PRODUCTS)

    # Уведомление администратору
    admin_text = (
        f"🛒 <b>Новый заказ!</b>\n\n"
        f"👤 {data['customer_name']}\n"
        f"📱 {data['customer_phone']}\n"
        f"📍 {data['customer_address']}\n"
        f"🆔 Telegram: @{callback.from_user.username or callback.from_user.id}\n\n"
        f"<b>Товары:</b>\n{items_text}\n\n"
        f"💰 Сумма: <b>{total} ₽</b>"
    )
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception:
        pass  # Если ADMIN_ID не задан — просто пропускаем

    # Очищаем корзину и состояние
    await state.clear()

    await callback.answer("Заказ принят!")
    await callback.message.edit_text(
        "✅ <b>Заказ оформлен!</b>\n\n"
        "Мы свяжемся с тобой в ближайшее время для подтверждения.\n"
        "Спасибо за покупку! 🎉",
        parse_mode="HTML",
    )
    await callback.message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(F.data == "order_edit")
async def order_edit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.answer()
    await callback.message.answer(
        "Заказ отменён. Можешь изменить корзину и оформить снова.",
        reply_markup=main_menu_kb(),
    )


# ── Мои заказы (заглушка) ─────────────────────────────────────────────────────

@router.message(F.text == "📦 Мои заказы")
async def my_orders(message: Message):
    await message.answer(
        "📦 История заказов пока недоступна.\n"
        "По вопросам о заказах пишите: @support_username"
    )
