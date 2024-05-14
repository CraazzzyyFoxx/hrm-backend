from enum import StrEnum


class RouteTag(StrEnum):
    """Tags used to classify API routes"""

    SETTINGS = "⚙️ Settings"

    USERS = "🤷🏿‍♀️‍ Users"
    BELBIN = "🎭 Belbin"
    AUTH = "🤷🏿‍♀️‍ Auth"
    RESUME = "📄 Resume"


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


class Gender(StrEnum):
    male = "Мужской"
    female = "Женский"


class Busyness(StrEnum):
    full = "Полная занятость"
    part = "Частичная занятость"
    project = "Проектная работа"
    volunteering = "Волонтерство"
    internship = "Стажировка"


class WorkSchedule(StrEnum):
    full = "Полный день"
    shift = "Сменный график"
    remote = "Удаленная работа"
    flexible = "Гибкий график"
    duty = "Вахтовый метод"


