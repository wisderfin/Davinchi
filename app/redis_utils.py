import json

import redis


# Класс контекстного менеджера для открытия и закрытия redis сессии
class SessionManager:
    def __init__(self):
        self.session = redis.Redis(host='redis', port=6379, decode_responses=True)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# Функция декоратора для использования функций в контекстном менеджере SessionManager
def autosession(func):
    def wrapper(*args, **kwargs):
        with SessionManager() as connect:
            return func(*args, session=connect, **kwargs)
    return wrapper


# Проверка наличия значения с ключом key в redis
@autosession
def exists(key: str, session=None) -> bool:
    return session.exists(key)


# Получение значения по ключу key из redis
@autosession
def get(key: str, session=None):
    if exists(key):
        session.expire(key, 60*60*24*7)
        return session.get(key)
    return None


# Установка значения value для ключа key в redis
@autosession
def set(key: str, value, session=None):
    session.set(name=key, value=value, ex=60*60*24*7)


# Удаление ключа key из пространства ключей redis
@autosession
def remove(key: str, session=None):
    session.delete(key)


@autosession
def get_by_status(status: str, session=None):
    keys = session.keys('*')
    result = []
    try:
        for key in keys:
            if get(key=key) == status:
                result.append(key)
    except Exception:
        pass
    return result


def set_json(key, value):
    set(key, json.dumps(value))


def get_json(key):
    data = get(key)
    return json.loads(data) if data else None
