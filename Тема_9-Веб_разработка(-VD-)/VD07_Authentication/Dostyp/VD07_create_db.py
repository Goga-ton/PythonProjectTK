from VD07_app import db, app
from VD07_app.VD07_models import User

with app.app_context():
    db.create_all()
    print("✅ База данных создана!")
    users = User.query.all()
    print(f"Users in database: {users}")
# exit()
