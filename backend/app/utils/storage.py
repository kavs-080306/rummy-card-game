# In-memory game storage (for development)
# In production, use Firestore

games_storage = {}

def save_game(game):
    games_storage[game.game_id] = game

def get_game(game_id):
    return games_storage.get(game_id)

def get_all_games():
    return list(games_storage.values())

def delete_game(game_id):
    if game_id in games_storage:
        del games_storage[game_id]
