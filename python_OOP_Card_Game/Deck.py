from card_elements import *

class Deck(object):
    def __init__(self):
        self.cards = []
        self.create_deck()
        
    def create_deck(self):
        # A deck contains 13 cards of four suit ['Heart', 'Diamond', 'Spade', 'Club']
        pack = ['Heart', 'Diamond', 'Spade', 'club']
        
        for suit in pack:
            for i in range(1, 14):
                self.cards.append(Card(suit=suit, value=i))
    
    def draw_card(self):
        return(self.cards.pop())
    
    def add_card(self, card):
        self.cards.append(card)
        
    
    def show_deck(self):
        for card in self.cards:
            card.show_card()
            
    def shuffle_deck(self):
        pass
            
# Test script
if __name__ == '__main__':
    deck = Deck()
    deck.show_deck()
    
