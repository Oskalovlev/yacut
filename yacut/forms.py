from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import Length, Optional

from .constants import ORIGINAL_LENGTH, CUSTOM_LENGTH


class ShortForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[Length(1, ORIGINAL_LENGTH)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, CUSTOM_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
