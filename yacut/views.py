from flask import flash, redirect, render_template, abort
from http import HTTPStatus

from . import app
from .forms import ShortForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def short_view():
    form = ShortForm()

    if not form.validate_on_submit():
        return render_template('short.html', form=form)

    short = form.custom_id.data

    if URLMap.check_unique_short_id(short):
        flash(f'Имя {form.custom_id.data} уже занято!')
        return render_template('short.html', form=form)

    if short and not URLMap.check_allowed_char(short):
        flash('Допустимые символы: A-Z, a-z, 0-9')
        return render_template('short.html', form=form)

    return render_template(
        'short.html', form=form,
        short_url=URLMap.get_short_url(
            URLMap.save(form.original_link.data, short).short
        )
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    url = URLMap.get(short)
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
