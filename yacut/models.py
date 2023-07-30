from datetime import datetime
import random
import re

from . import db
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
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def check_allowed_char(custom_id):
        return re.match(ALLOWED_REGULAR, custom_id)

    @staticmethod
    def get_unique_short_id():
        return ''.join(random.choices(ALLOWED_CHAR, k=RANDOM_LENGTH))

    @staticmethod
    def check_unique_short_id(short):
        if URLMap.get(short):
            return short

    def save(original, short, validate=False):
        if short is None:
            short = URLMap.get_unique_short_id()

        if len(short) > CUSTOM_LENGTH or not re.match(ALLOWED_REGULAR, short):
            raise ValueError(
                'Указано недопустимое имя для короткой ссылки'
            )

        if URLMap.check_unique_short_id(short):
            raise ValueError(f'Имя "{short}" уже занято.')

        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
