from flask import render_template, redirect, url_for, request, flash
from VD09_host import app, db, bcrypt
from VD09_host.VD09_models import User
from VD09_host.VD09_forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@login_required
def index():
    from VD09_host.VD09_models import User  # ← Добавьте импорт
    top_users = User.query.order_by(User.clicks.desc()).limit(5).all()
    return render_template('VD09_index.html', top_users=top_users, User=User)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегестрировались', 'success')
        return redirect(url_for('login'))
    return render_template('VD09_register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Вы ввели некоректные данные', 'danger')
    return render_template('VD09_login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))