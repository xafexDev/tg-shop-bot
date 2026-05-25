# Каталог товаров — легко редактировать под любой магазин
CATEGORIES = {
    "hoodies": "👕 Худи",
    "tshirts": "👔 Футболки",
    "accessories": "🎒 Аксессуары",
}

PRODUCTS = {
    "hoodies": [
        {
            "id": "h1",
            "name": "Худи Oversize Black",
            "price": 3200,
            "desc": "Оверсайз худи из плотного хлопка 320г/м². Размеры S–XXL.",
            "emoji": "🖤",
        },
        {
            "id": "h2",
            "name": "Худи Classic Grey",
            "price": 2900,
            "desc": "Классический серый меланж. Мягкий флис внутри. Размеры S–XL.",
            "emoji": "🩶",
        },
        {
            "id": "h3",
            "name": "Худи Zip White",
            "price": 3500,
            "desc": "Худи на молнии, белый. Карманы кенгуру. Размеры S–XXL.",
            "emoji": "🤍",
        },
    ],
    "tshirts": [
        {
            "id": "t1",
            "name": "Футболка Basic White",
            "price": 1400,
            "desc": "Базовая белая футболка, 100% хлопок 180г/м². Размеры XS–XXL.",
            "emoji": "🤍",
        },
        {
            "id": "t2",
            "name": "Футболка Graphic Black",
            "price": 1800,
            "desc": "Чёрная с принтом. Шелкография, не выцветает. Размеры S–XL.",
            "emoji": "🖤",
        },
    ],
    "accessories": [
        {
            "id": "a1",
            "name": "Шопер Canvas",
            "price": 800,
            "desc": "Плотный хлопковый шопер. Размер 38×42 см.",
            "emoji": "🛍",
        },
        {
            "id": "a2",
            "name": "Кепка Snapback",
            "price": 1600,
            "desc": "Бейсболка с регулируемым ремешком. Один размер.",
            "emoji": "🧢",
        },
    ],
}

# Быстрый поиск товара по id
ALL_PRODUCTS = {p["id"]: p for items in PRODUCTS.values() for p in items}
