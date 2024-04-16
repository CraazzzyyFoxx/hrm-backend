from enum import StrEnum, Enum


class RouteTag(StrEnum):
    """Tags used to classify API routes"""

    SETTINGS = "⚙️ Settings"

    USERS = "🤷🏿‍♀️‍ Users"
    ORDERS = "📒 Orders"
    PREORDERS = "📒 Pre Orders"
    SHEETS = "📊 Google Sheets"
    RESPONSES = "📩 Responses"
    AUTH = "🤷🏿‍♀️‍ Auth"
    MESSAGES = "✉️ Messages"
    CHANNELS = "✉️ Channels"
    RENDER = "✉️ Message Render"
    ACCOUNTING = "📊 Accounting"
    ADMIN = "🤷🏿‍♀️‍ Admin"
    CURRENCY = "💰 Currency"
    ORDER_RENDERS = "📒 Order Renders"
    SCREENSHOTS = "📷 Screenshots"

    DISCORD_OAUTH = "🤷🏿‍♀️‍ Discord OAuth"


class SearchStatus(StrEnum):
    """Status of a search"""

    active = "Активно ищу работу"
    considering = "Рассматриваю предложения"
    offer_thinking = "Предложили работу, пока думаю"
    going_new = "Уже выхожу на новое место"
    not_looking = "Не ищу работу"
