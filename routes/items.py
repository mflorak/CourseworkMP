from flask import Blueprint, request, jsonify
from models import db, Item
from auth import auth

items_bp = Blueprint('items', __name__)


@items_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': i.id, 'name': i.name, 'price': i.price,
        'size': i.size, 'color': i.color
    } for i in items])


@items_bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({'id': item.id, 'name': item.name, 'price': item.price})


@items_bp.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'message': 'Bad Request'}), 400

    if Item.query.get(data['id']):
        return jsonify({'message': 'Exists'}), 400

    new_item = Item(
        id=data['id'], name=data.get('name', 'NoName'),
        price=data.get('price', 0), size=data.get('size'), color=data.get('color')
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Created'}), 201


@items_bp.route('/items/<int:id>', methods=['PUT'])
@auth.login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify({'message': 'Updated'})


@items_bp.route('/items/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'})