import random

from .constants import ALLOWED_CHAR
from .models import URLMap


def check_allowed_char(custom_id):
    for char in custom_id:
        if char not in ALLOWED_CHAR:
            return False
    return True


def check_unique_short_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None


def get_unique_short_id():
    short = random.choices(ALLOWED_CHAR, k=6)
    return ''.join(short)