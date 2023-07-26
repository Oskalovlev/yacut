from datetime import datetime
from http import HTTPStatus
from flask import url_for
import random
import re

from . import db
from .error_handlers import InvalidAPIUsage
from .constants import ORIGINAL_LENGTH, CUSTOM_LENGTH, URL
from .constants import ALLOWED_CHAR, RANDOM_LENGTH, ALLOWED_REGULAR


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(CUSTOM_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=URL + self.short,
        )

    @staticmethod
    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def check_allowed_char(custom_id):
        for char in custom_id:
            if char not in ALLOWED_CHAR:
                return False
        return True

    @staticmethod
    def get_unique_short_id():
        short = random.choices(ALLOWED_CHAR, k=RANDOM_LENGTH)
        return ''.join(short)

    @staticmethod
    def check_unique_short_id(custom_id):
        if URLMap.query.filter_by(short=custom_id).first():
            return custom_id
        return None

    @staticmethod
    def get_short_url(short):
        return url_for('redirect_url', short=short, _external=True)

    @staticmethod
    def save(original, short=None, validate=False):
        if short in [None, ""]:
            short = URLMap.get_unique_short_id()
        if validate:
            if len(short) > CUSTOM_LENGTH or not re.match(ALLOWED_REGULAR, short):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки',
                    HTTPStatus.BAD_REQUEST
                )
        if URLMap.check_unique_short_id(short):
            raise InvalidAPIUsage(
                (f'Имя "{short}" уже занято.'),
                HTTPStatus.BAD_REQUEST
            )
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
