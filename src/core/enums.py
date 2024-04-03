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


class OrderStatus(StrEnum):
    Refund = "Refund"
    InProgress = "In Progress"
    Completed = "Completed"


class OrderPaidStatus(StrEnum):
    Paid = "Paid"
    NotPaid = "Not Paid"


class PayrollType(StrEnum):
    binance_email = "Binance Email"
    binance_id = "Binance ID"
    trc20 = "TRC 20"
    phone = "Phone"
    card = "Card"


class NotificationType(Enum):
    ORDER_RESPONSE_APPROVE = "order_response_approve"
    ORDER_RESPONSE_DECLINE = "order_response_decline"
    ORDER_RESPONSE_ADMIN = "order_response_admin"
    LOGGED_NOTIFY = "logged_notify"
    REGISTERED_NOTIFY = "registered_notify"
    REQUEST_VERIFY = "request_verify"
    VERIFIED_NOTIFY = "verified_notify"
    ORDER_CLOSE_REQUEST = "order_close_request"
    ORDER_SENT_NOTIFY = "order_sent_notify"
    ORDER_EDITED_NOTIFY = "order_edited_notify"
    ORDER_DELETED_NOTIFY = "order_deleted_notify"
    RESPONSE_CHOSE_NOTIFY = "response_chose_notify"
    ORDER_PAID_NOTIFY = "order_paid_notify"
