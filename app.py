import os
from flask import Flask, jsonify
from models import db, User
from routes.currency import currency_bp
from routes.items import items_bp

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'coursework.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)

app.register_blueprint(currency_bp)
app.register_blueprint(items_bp)


@app.route('/')
def index():
    return jsonify({"message": "Coursework API is running!", "status": "ok"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password='password123'))
            db.session.commit()
            print("Admin created.")

    app.run(host='0.0.0.0', port=5001, debug=True)