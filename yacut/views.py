import random
import string

from flask import render_template, flash, redirect, abort

from yacut.constants import DUPLICATE_MESSAGE
from yacut.forms import CutForm
from yacut.models import URLMap
from . import app, db


@app.route('/', methods=['GET', 'POST'])
def service_page():
    form = CutForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            short_link = form.custom_id.data
            link = URLMap.query.filter_by(short=short_link).first()
            if link:
                flash(DUPLICATE_MESSAGE)
                return render_template('cutter.html', form=form)
        else:
            short_link = get_unique_short_id()
            while URLMap.query.filter_by(short=short_link).first():
                short_link = get_unique_short_id()

        cut_url = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(cut_url)
        db.session.commit()
        return render_template('cutter.html', form=form, cut_url=cut_url.short)

    return render_template('cutter.html', form=form)


@app.route('/<string:short_link>')
def redirect_link(short_link):
    external_link = URLMap.query.filter_by(short=short_link).first()
    if external_link:
        return redirect(external_link.original)

    return abort(404)


def get_unique_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


if __name__ == '__main__':
    app.run()
