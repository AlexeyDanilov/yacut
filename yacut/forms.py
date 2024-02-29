from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional, URL, Regexp


class CutForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[
            Length(1, 256),
            URL(message='Ссылка неверного формата')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Length(6, 16),
            Optional(),
            Regexp(regex='[A-Z]+|[a-z]+|\d+')
        ]
    )
    submit = SubmitField('Создать')
