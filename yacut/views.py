from flask import render_template, redirect, flash

from yacut.error_handlers import CreateLinkException
from yacut.forms import CutForm
from yacut.models import URLMap
from . import app


@app.route('/', methods=['GET', 'POST'])
def service_page():
    form = CutForm()
    if form.validate_on_submit():
        try:
            cut_url = URLMap.create_link(form.data)
            return render_template('cutter.html', form=form, cut_url=cut_url.short)
        except CreateLinkException as e:
            flash(e.args[0])

    return render_template('cutter.html', form=form)


@app.route('/<string:short_link>')
def redirect_link(short_link):
    external_link = URLMap.query.filter_by(short=short_link).first_or_404()
    return redirect(external_link.original)


if __name__ == '__main__':
    app.run()
