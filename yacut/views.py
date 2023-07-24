from flask import flash, redirect, render_template

from . import app, db
from .forms import YacutForm
from .models import URLMap
from .functionality import check_allowed_char, get_unique_short_id, check_unique_short_id
from .constants import URL


@app.route('/', methods=['GET', 'POST'])
def short_view():
    form = YacutForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if check_unique_short_id(custom_id):
            flash(f'Имя {custom_id} уже занято!')
            return render_template('short.html', form=form)

        if custom_id and not check_allowed_char(custom_id):
            flash('Допустимые символы: A-Z, a-z, 0-9')
            return render_template('short.html', form=form)

        if custom_id is None:
            custom_id = get_unique_short_id()

        url = URLMap(
            original=original_link,
            short=custom_id,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('short.html',
                               form=form,
                               short_url=URL + url.short,
                               original_link=url.original)
    return render_template('short.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
