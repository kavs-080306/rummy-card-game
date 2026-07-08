import random

class Deck:
    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        self.cards = [{"suit": suit, "rank": rank} for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop() if self.cards else None
    
    def remaining(self):
        return len(self.cards)
