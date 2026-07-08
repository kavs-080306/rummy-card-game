from flask import Blueprint, request, jsonify
from app.models.game import Game
from app.utils.storage import save_game, get_game, get_all_games

bp = Blueprint('games', __name__, url_prefix='/api')

@bp.route('/games', methods=['GET'])
def get_games():
    games = get_all_games()
    games_data = [game.to_dict() for game in games if game.status in ['waiting', 'playing']]
    return jsonify({"games": games_data}), 200

@bp.route('/create-game', methods=['POST'])
def create_game():
    data = request.json
    creator_id = data.get('creatorId')
    entry_fee = data.get('entryFee', 10)
    
    if not creator_id:
        return jsonify({"error": "Creator ID is required"}), 400
    
    game = Game(creator_id=creator_id, entry_fee=entry_fee)
    game.add_player({
        "id": creator_id,
        "name": data.get('name', 'Player'),
        "coins": data.get('coins', 0),
        "hand": []
    })
    
    save_game(game)
    return jsonify({"gameId": game.game_id, "game": game.to_dict()}), 201

@bp.route('/join-game', methods=['POST'])
def join_game():
    data = request.json
    game_id = data.get('gameId')
    player_id = data.get('playerId')
    
    game = get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    if game.status != "waiting":
        return jsonify({"error": "Game is no longer accepting players"}), 400
    
    player = {
        "id": player_id,
        "name": data.get('name', 'Player'),
        "coins": data.get('coins', 0),
        "hand": []
    }
    
    if game.add_player(player):
        save_game(game)
        
        # Auto-start if 2 players
        if len(game.players) >= 2 and game.status == "waiting":
            game.start_game()
            save_game(game)
        
        return jsonify({"message": "Joined game", "game": game.to_dict()}), 200
    
    return jsonify({"error": "Cannot join game"}), 400

@bp.route('/game/<game_id>', methods=['GET'])
def get_game_state(game_id):
    game = get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    return jsonify(game.to_dict()), 200

@bp.route('/game/<game_id>/play', methods=['POST'])
def play_cards(game_id):
    data = request.json
    game = get_game(game_id)
    
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    player_id = data.get('playerId')
    card_indices = data.get('cardIndices', [])
    
    current_player = game.get_current_player()
    if current_player['id'] != player_id:
        return jsonify({"error": "Not your turn"}), 403
    
    game.next_turn()
    save_game(game)
    
    return jsonify({"message": "Cards played", "game": game.to_dict()}), 200

@bp.route('/game/<game_id>/draw', methods=['POST'])
def draw_card(game_id):
    data = request.json
    game = get_game(game_id)
    
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    player_id = data.get('playerId')
    current_player = game.get_current_player()
    
    if current_player['id'] != player_id:
        return jsonify({"error": "Not your turn"}), 403
    
    card = game.deck.draw()
    if card:
        current_player['hand'].append(card)
    
    save_game(game)
    return jsonify({"message": "Card drawn", "game": game.to_dict()}), 200

@bp.route('/game/<game_id>/discard', methods=['POST'])
def discard_card(game_id):
    data = request.json
    game = get_game(game_id)
    
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    player_id = data.get('playerId')
    card_index = data.get('cardIndex')
    
    current_player = game.get_current_player()
    if current_player['id'] != player_id:
        return jsonify({"error": "Not your turn"}), 403
    
    if 0 <= card_index < len(current_player['hand']):
        card = current_player['hand'].pop(card_index)
        game.discard_pile.append(card)
    
    game.next_turn()
    save_game(game)
    
    return jsonify({"message": "Card discarded", "game": game.to_dict()}), 200
