from flask import render_template, request, redirect, url_for
from DZ_VD06_app import app

posts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        hobby = request.form.get('hobby')
        number = request.form.get('number')
        if name and city and hobby and number:
            posts.append({'nam':name, 'cit':city, 'hob':hobby, 'num':number})
            return redirect(url_for('index')) #обновляем страницу что бы увидеть результат
    return render_template('blog.html', posts=posts)