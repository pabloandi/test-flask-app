from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models import Store as StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return dict(message='Store not found'), 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return dict(message=f'A store with name {name} already exists'), 400
        
        store = StoreModel(name)
        try:
            store.save()
        except:
            return dict(message='An error occurred while creating the store'), 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        
        return dict(message=f'Store {name} deleted successfully')

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}