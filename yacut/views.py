from flask import flash, redirect, render_template, abort, url_for
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
    original = form.original_link.data

    try:
        return render_template(
            'short.html', form=form,
            short_url=url_for(
                'redirect_url',
                short=URLMap.save(original, short).short,
                _external=True
            )
        )
    except ValueError:
        flash(f'Имя {short} уже занято!')
        return render_template('short.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    url = URLMap.get(short)
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
