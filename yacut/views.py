import random
import string

from flask import render_template, flash, redirect, url_for

from yacut.forms import CutForm
from yacut.models import URLMap
from . import app, db


@app.route('/', methods=['GET', 'POST'])
def service_page():
    form = CutForm()
    if form.validate_on_submit():
        if form.custom_id:
            link = URLMap.query.filter_by(short=form.custom_id.data).first()
            if link:
                flash('Такая ссылка уже существует')
                return render_template('index.html', form=form)
            cut_url = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            db.session.add(cut_url)
            db.session.commit()
            return render_template('index.html', form=form, cut_url=cut_url.short)

        while True:
            random_url = get_unique_short_id()
            link = URLMap.query.filter_by(short=random_url).first()
            if not link:
                break
        cut_url = URLMap(
            original=form.original_link.data,
            short=random_url
        )
        db.session.add(cut_url)
        db.session.commit()
        return render_template('index.html', form=form, cut_url=cut_url)

    return render_template('index.html', form=form)


@app.route('/<string:short_link>')
def redirect_link(short_link):
    external_link = URLMap.query.filter_by(short=short_link).first()
    if external_link:
        return redirect(external_link.original)

    return ...


def get_unique_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


if __name__ == '__main__':
    app.run()
