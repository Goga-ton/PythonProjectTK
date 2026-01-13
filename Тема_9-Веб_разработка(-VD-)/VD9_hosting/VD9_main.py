from VD09_host import app, db
from VD09_host.VD09_models import User

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)