from flask import Flask
import os

def create_app():
    app=Flask(__name__)
    app.secret_key=os.getenv("SECRET_KEY")
    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)


    return app