import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

items = []
class Item(Resource):

    pareser = reqparse.RequestParser()
    pareser.add_argument('price',type=float,required=True,help='price cannot be empty')

    pareser.add_argument('store_id', type=int, required=True, help='every item need a store')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message':'item with {} doesnot exists'.format(name)}, 404



    def post(self, name):
        row = ItemModel.find_by_name(name)
        if row :
            return {'message':'item with name "{}" already exists'.format(name)}, 400      # bad request
        data = Item.pareser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'message':'an error acuured'} , 500 #internal server error
        return item.json(), 201



    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'items got deleted'}

        else:
            return {'message':'item not found'}, 400


    def put(self,name):
        data = Item.pareser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name,data['price'],data['store_id'])
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  #[item.json for item in ItemModel.query.all()]
