from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import Length, Optional


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[Length(1, 256)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
