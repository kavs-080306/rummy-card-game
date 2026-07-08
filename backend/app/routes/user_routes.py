from flask import Blueprint, request, jsonify

bp = Blueprint('users', __name__, url_prefix='/api')

@bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # TODO: Get user from Firestore
    return jsonify({"userId": user_id}), 200

@bp.route('/user/<user_id>/coins', methods=['GET'])
def get_user_coins(user_id):
    # TODO: Get coins from Firestore
    return jsonify({"coins": 1000}), 200

@bp.route('/user/<user_id>/coins', methods=['POST'])
def update_coins(user_id):
    data = request.json
    amount = data.get('amount', 0)
    # TODO: Update coins in Firestore
    return jsonify({"message": "Coins updated", "newBalance": 1000 + amount}), 200
