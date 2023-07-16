from Deck import *
class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    def draw_card_from_deck(self, deck):
        self.hand.append(deck.draw_card())
        
    def show_hand(self):
        for card in self.hand:
            card.show_card()

if __name__ == "__main__":
    from Deck import *
    
    deck = Deck()
    p1 = Player("player-1")
    p1.draw(deck=deck)
    p1.draw(deck=deck)
    p1.show_hand()