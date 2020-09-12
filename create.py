from flask import Flask
from models import *

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywqxdfutjbrllu:4bf9490496b00c99e12a00ac7aad76018a943dd7997fb6667da8dc33b63dd075@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/dc4d1f73beffi3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()
