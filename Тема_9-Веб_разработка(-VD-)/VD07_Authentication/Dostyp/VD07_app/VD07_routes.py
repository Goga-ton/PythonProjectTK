from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from VD07_app.VD07_models import User
from VD07_app import app, db, bcrypt
from VD07_app.VD07_forms import RegistrationForm, LoginForm, UpdateProfileForm



@app.route('/')
def home():
    return render_template('VD07_home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print(f"Form submitted: {form.is_submitted()}")
    print(f"Form validated: {form.validate()}")
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегестрировались', 'success')
        return redirect(url_for('login'))
    else:
        print("✅ Ошибки валидации:")  # ← Это покажет какие именно поля не прошли проверку
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
    return render_template('VD07_register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    print(f"Login form submitted: {form.is_submitted()}")  # ← Добавь
    print(f"Login form validated: {form.validate()}")  # ← Добавь
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User found: {user}")  # ← Добавь
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Password correct!")  # ← Добавь
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            print("Invalid email or password")
            flash('Введены не верные данные', 'danger')
    else:
        print("Login form errors:", form.errors)  # ← Добавь
    return render_template('VD07_login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route('/account')
# @login_required
# def account():
#     return render_template('VD07_account.html') # смотри декаратор выше, вопрос в написании адресов и смысла функций

 #ДЗ по уроку VD07 создаем форму для коректировки профиля
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # Проверяем текущий пароль
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            # Обновляем данные
            current_user.username = form.username.data
            current_user.email = form.email.data

            # Если указан новый пароль - обновляем
            if form.new_password.data:
                current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

            db.session.commit()
            flash('Профиль успешно обновлен!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Неверный текущий пароль', 'danger')

    # Заполняем форму текущими данными
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('VD07_account.html', form=form)
