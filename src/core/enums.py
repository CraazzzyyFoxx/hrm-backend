from enum import StrEnum, Enum


class RouteTag(StrEnum):
    """Tags used to classify API routes"""

    SETTINGS = "⚙️ Settings"

    USERS = "🤷🏿‍♀️‍ Users"
    BELBIN = "🎭 Belbin"
    AUTH = "🤷🏿‍♀️‍ Auth"


class SearchStatus(StrEnum):
    """Status of a search"""

    active = "Активно ищу работу"
    considering = "Рассматриваю предложения"
    offer_thinking = "Предложили работу, пока думаю"
    going_new = "Уже выхожу на новое место"
    not_looking = "Не ищу работу"


class BelbinRole(StrEnum):
    chairman = "Председатель"
    closer = "Доводчик"
    shaper = "Формирователь"
    thinker = "Мыслитель"
    appraiser = "Оценщик"
    collectivist = "Коллективист"
    scout = "Разведчик"
    executor = "Исполнитель"
