class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def show_card(self):
        print(f"{self.value} of {self.suit}")
        
        
if __name__ == "__main__":
    c1 = Card(5, "Heart")
    c1.show_card()
    