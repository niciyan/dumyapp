from flask import render_template, redirect, flash, url_for, current_app
from . import main
from .. import db
from ..models import Message
from .forms import NameForm
from datetime import datetime

@main.route('/')
def index():
    return render_template('index.html', messages=Message().query.order_by(Message.date.desc()).limit(6).all())

@main.route('/new', methods=['GET', 'POST'])
def new():
    form = NameForm() 
    # if request.method == 'POST':
    if form.validate_on_submit():
        # form.text.data
        now = datetime.now()
        me = Message(message=form.text.data, date=now)
        db.session.add(me)
        db.session.commit()
        flash('新しいメッセージを追加しました!!')
        current_app.logger.debug('new data inserted.')
        return redirect('/')
        print('passed')
    else:
        return render_template('new.html', form=form)

