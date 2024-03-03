from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional, URL, Regexp

from yacut.constants import (
    WRONG_FORMAT_MASSAGE, WRONG_LINK_NAME_MESSAGE, REG_EXPRESSION
)


class CutForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[
            Length(1, 256),
            URL(message=WRONG_FORMAT_MASSAGE)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Length(max=16, message=WRONG_LINK_NAME_MESSAGE),
            Optional(),
            Regexp(
                regex=REG_EXPRESSION,
                message=WRONG_FORMAT_MASSAGE
            )
        ]
    )
    submit = SubmitField('Создать')
