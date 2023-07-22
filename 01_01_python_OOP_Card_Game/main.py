from Player import *

if __name__ == "__main__":
    deck = Deck()
    # Show deck
    print("\nShow Deck")
    deck.show_deck()
    
    p1 = Player(name='player-1')
    p2 = Player(name='player-2')
    
    p1.draw_card_from_deck(deck=deck)
    p2.draw_card_from_deck(deck=deck)
    
    print('\nPlayer-1 show hand:')
    p1.show_hand()
    
    print('\nPlayer-2 show hand:')
    p2.show_hand()
    
    print("\nShow Deck")
    deck.show_deck()
    
    print('\n End of script')
    