from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models import Item as ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        
        return {'message': 'item not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': 'A item with that name already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save()
        except:
            return dict(message="An error occurred inserting the item"), 500

        
        return {'message': 'Item created successfully'}, 201
    
    def delete(self, name):
        
        item = ItemModel.find_by_name(name)

        if item:
            item.delete()
        else:
            return dict(message=f"No item found with name {name}"), 400
        
        return dict(message=f'Item {name} deleted successfully'), 200
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']            
            item.store_id = data['store_id']            

        try:
            item.save()
        except:
            return dict(message="An error ocurred updating the item"), 500

        return item.json()


class ItemList(Resource):
    def get(self):
        
        items = ItemModel.query.all()
        if items:
            return {'items': [item.json() for item in items]}, 200
        
        return {'message': 'No items available'} , 400