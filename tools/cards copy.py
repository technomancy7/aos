from enum import Enum
from random import shuffle

class Suits(Enum):
    NULL = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

    def as_string(self):
        return [
            "null",
            "hearts",
            "diamonds",
            "clubs",
            "spades"
        ][self.value]

class Hand:
    def __init__(self):
        self.cards = []

    def draw_from(self, deck):
        if issubclass(deck.__class__, Deck):
            self.cards.append(deck.draw())
            
    def append(self, card):
        self.cards.append(card)  

    @property
    def length(self):
        return len(self.cards)

class PlayingCard:
    def __init__(self, suit, value):
        self.suit_id = suit
        self.value = value

    def to_hand(self, hand):
        if issubclass(hand.__class__, Hand):
            hand.cards.append(self)

    @property
    def colour(self):
        if self.suit == Suits.DIAMONDS or self.suit == Suits.HEARTS:
            return "red"
        else:
            return "black"

    @property
    def value_name(self):
        if self.value == 1:
            return "ace"
        elif self.value == 11:
            return "jack"
        elif self.value == 12:
            return "queen"
        elif self.value == 13:
            return "king"
        else:
            return str(self.value)

    @property
    def suit(self):
        return Suits(self.suit_id)

    @property
    def suit_name(self):
        return Suits(self.suit_id).as_string()

    def __repr__(self):
        return f"{self.value_name} of {self.suit_name}"

class Deck:
    def __init__(self):
        self.cards = []

        for value in range(1, 14):
            for suit in range(1, 5):
                self.cards.append(PlayingCard(suit, value))

    def append(self, card):
        self.cards.append(card)  

    @property
    def length(self):
        return len(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop()