from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('DZ_VD05_index.html')

@app.route('/blog/')
def blog():
    return render_template('DZ_VD05_blog.html')

@app.route('/templates/')
def templates():
    return render_template('DZ_VD05_templates.html')

@app.route('/time/')
def time():
    # now = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    # return f"Текущее время: {now}"
    return render_template('DZ_VD04_time.html')

if __name__ == '__main__':
    app.run()