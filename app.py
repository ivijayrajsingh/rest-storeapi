import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from security import authenticate,identity
from resources.user import RegisterUser,User,UserLogin
from resources.item import Item,ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'  #app.config['JWT_SECRET_KEY']
api = Api(app)



jwt = JWTManager(app)

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(RegisterUser,'/register')
api.add_resource(User,'/User')
api.add_resource(UserLogin,'/login')

if __name__== '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)