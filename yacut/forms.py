from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional, URL, Regexp, DataRequired

from yacut.constants import (
    WRONG_FORMAT_MASSAGE,
    WRONG_LINK_NAME_MESSAGE,
    REG_EXPRESSION,
    MIN_LENGTH_URL,
    MAX_LENGTH_URL,
    MAX_LENGTH_SHORT_ID
)


class CutForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[
            DataRequired(message='Поле обязательно для заполнения'),
            Length(MIN_LENGTH_URL, MAX_LENGTH_URL),
            URL(message=WRONG_FORMAT_MASSAGE)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Length(max=MAX_LENGTH_SHORT_ID, message=WRONG_LINK_NAME_MESSAGE),
            Optional(),
            Regexp(
                regex=REG_EXPRESSION,
                message=WRONG_FORMAT_MASSAGE
            )
        ]
    )
    submit = SubmitField('Создать')
