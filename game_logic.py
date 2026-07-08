import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop() if self.cards else None
    
    def remaining(self):
        return len(self.cards)

class Player:
    def __init__(self, uid, name, coins):
        self.uid = uid
        self.name = name
        self.coins = coins
        self.hand = []
    
    def add_card(self, card):
        self.hand.append(card)
    
    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False
    
    def card_count(self):
        return len(self.hand)
    
    def is_rummy(self):
        # Check if player has 13 cards that form valid sets/sequences
        return self.card_count() == 13 and self._can_form_sequences()
    
    def _can_form_sequences(self):
        # Placeholder for rummy validation logic
        return True

class RummyGame:
    def __init__(self, game_id, creator_id, creator_name, entry_fee=10):
        self.game_id = game_id
        self.creator_id = creator_id
        self.players = [Player(creator_id, creator_name, 0)]
        self.entry_fee = entry_fee
        self.status = "waiting"  # waiting, playing, finished
        self.deck = Deck()
        self.discard_pile = []
        self.current_player_index = 0
    
    def add_player(self, uid, name, coins):
        if len(self.players) < 6 and not any(p.uid == uid for p in self.players):
            self.players.append(Player(uid, name, coins))
            return True
        return False
    
    def start_game(self):
        if len(self.players) >= 2:
            self.status = "playing"
            self.deal_cards()
            return True
        return False
    
    def deal_cards(self):
        for player in self.players:
            player.hand = [self.deck.draw() for _ in range(13)]
    
    def get_current_player(self):
        return self.players[self.current_player_index] if self.players else None
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def draw_card(self):
        card = self.deck.draw()
        if card:
            self.get_current_player().add_card(card)
        return card
    
    def discard_card(self, card):
        current_player = self.get_current_player()
        if current_player.remove_card(card):
            self.discard_pile.append(card)
            return True
        return False
    
    def finish_game(self, winner_uid):
        self.status = "finished"
        return {
            "winner_uid": winner_uid,
            "prize_pool": self.entry_fee * len(self.players)
        }
