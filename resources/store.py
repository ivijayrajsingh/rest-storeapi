from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):

    pareser = reqparse.RequestParser()
    pareser.add_argument('name',type=str,required=True,help='name cannot be empty')

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message':'store with name:{} doesnt exists'.format(name)}


    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'store with name: {} already exists'.format(name)}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'error accured while saving to db'} ,500
        return store.json(),201

    def put(self,name):
        if StoreModel.find_by_name(name):
            store = StoreModel(name)
        else:
            store = StoreModel(name)
        store.save_to_db()
        return store.json()

    def delete(self,name):
        store =  StoreModel.find_by_name(name)
        if store:
            store.delete(name)
            return {'message':'succesfully deleted'}
        return {'message':'store doesnot exists'} , 500

class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}