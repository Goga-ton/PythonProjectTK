from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm # Это базовый класс для создания форм
from wtforms import StringField, SubmitField # Это классы для создания полей внутри формы
from wtforms.validators import DataRequired # Валидатор, нуный для проверки

app = Flask(__name__)

#Создаём секретный ключ для защиты форм
app.config['SECRET_KEY'] = 'your_secret_key'

#Создаём класс для создания формы
class NameForm(FlaskForm): # Используем FlaskForm в качестве родительского класса
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Создаём маршрут для главной страницы
@app.route('/', methods=['GET', 'POST']) #  С помощью этого маршрута мы сможем и отправлять, и получать информацию
def index():
    form = NameForm() #  Создаём объект формы
    if form.validate_on_submit(): # Проверка того, прошла ли форма валидацию и вообще отправлена ли она
        name = form.name.data #  Получаем значение из формы, информацию из этого значения. Сохраняем в переменную
        return redirect(url_for('hello', name=name)) # Отправляем пользователя на новую страницу, передаём полученное имя
    return render_template('VD07_index_2.html', form=form)

#Создаём маршрут для отображения приветствия
@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)