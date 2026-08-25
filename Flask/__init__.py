from flask import Flask

def create_app():
    app=Flask(__name__)

    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)


    return app