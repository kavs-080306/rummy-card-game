import uuid
from datetime import datetime
from app.models.deck import Deck

class Game:
    def __init__(self, game_id=None, creator_id=None, entry_fee=10):
        self.game_id = game_id or str(uuid.uuid4())
        self.creator_id = creator_id
        self.players = []
        self.entry_fee = entry_fee
        self.status = "waiting"
        self.created_at = datetime.now().isoformat()
        self.current_player_index = 0
        self.discard_pile = []
        self.deck = Deck()
    
    def add_player(self, player):
        if len(self.players) < 6 and all(p['id'] != player['id'] for p in self.players):
            self.players.append(player)
            return True
        return False
    
    def remove_player(self, player_id):
        self.players = [p for p in self.players if p['id'] != player_id]
    
    def start_game(self):
        if len(self.players) >= 2:
            self.status = "playing"
            self.deal_cards()
            return True
        return False
    
    def deal_cards(self):
        for player in self.players:
            player['hand'] = [self.deck.draw() for _ in range(13)]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def get_current_player(self):
        return self.players[self.current_player_index] if self.players else None
    
    def finish_game(self, winner_id):
        self.status = "finished"
        return {
            "winner_id": winner_id,
            "game_id": self.game_id,
            "prize_pool": self.entry_fee * len(self.players)
        }
    
    def to_dict(self):
        return {
            "gameId": self.game_id,
            "creatorId": self.creator_id,
            "players": self.players,
            "entryFee": self.entry_fee,
            "status": self.status,
            "createdAt": self.created_at,
            "currentPlayerIndex": self.current_player_index,
            "discardPile": self.discard_pile,
            "deckRemaining": self.deck.remaining()
        }
