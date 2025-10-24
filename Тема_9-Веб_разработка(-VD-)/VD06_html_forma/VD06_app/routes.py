from flask import render_template, request, redirect, url_for
from VD06_app import app

posts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tit = request.form.get('ima')
        cont = request.form.get('teck')
        if tit and cont:
            posts.append({'kt':tit, 'mc':cont})
            return redirect(url_for('index')) #обновляем страницу что бы увидеть результат
    return render_template('blog.html', posts=posts)