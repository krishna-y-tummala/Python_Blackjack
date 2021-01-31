#global variables
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}

playing = True

#card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

#deck class
class Deck:
    
    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck = ''
        for card in self.deck:
            deck += '\n'+ card.__str__()
        return 'The deck has: ' + deck

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card

#hand class
class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0    
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces>0:
            self.value -= 10
            self.aces -= 1

#chips class
class Chips:
    
    def __init__(self):
        self.total = int(input('Please enter the number of chips you have: '))
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total + self.bet
    
    def lose_bet(self):
        self.total -= self.bet

##FUNCTIONS
#take bet
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Please enter the number of chips you want to bet: '))
        except ValueError:
            print ('Sorry please enter the number in integers!')
        else:
            if chips.bet > chips.total:
                print (f'Sorry you cannot bet more than you have! You have {chips.total} chips!')
            else:
                break
    

#hit
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

#hit or stand
def hit_or_stand(deck,hand):
    global playing 
    
    while True:
        x = input("Would you like to hit or stand? Enter 'h' or 's': ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)
            
        elif x[0].lower() == 's':
            print ('You have chosen to stand! The dealer is now playing!')
            playing = False
        else:
            print ('Sorry! Please try again')
            continue
        break

#show cards
def show_some(player,dealer):
    print ("\nDealer's hand: ")
    print ('<card hidden>')
    print ('', dealer.cards[1])
    print ("Player's cards: ", *player.cards, sep = '\n ')
    
def show_all(player,dealer):
    print ("\nDealer's hand: ", *dealer.cards, sep = '\n')
    print ("Dealer's hand: ", dealer.value)
    print ("Player's cards: ", *player.cards, sep = '\n ')
    print ("Player's hand: ", player.value)
    
    
#end of game
def player_busts(player,dealer,chips):
    print ('Player busts!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print ('Player wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print ('Dealer busts!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print ('Dealer wins!')
    chips.lose_bet()
    
def push(player,dealer):
    print ("It's a push! Player and dealer are tied")

#GAME
while True:
    
    print ('Welcome to Blackjack! Your goal is to get as close to 21 as possible without going over.\n\
    Dealer hits until they reach 17. Face cards value 10, Aces count as 1 or 11! Good Luck')
    
    # Create & shuffle the deck
    deck = Deck()
    deck.shuffle()
           
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
           
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Place bet
    take_bet(player_chips)
    
    # Show some cards
    show_some(player_hand, dealer_hand)
    
    while playing:  
        
        hit_or_stand(deck, player_hand)
        
        # Show some cards 
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        #winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        
        else:
            push(player_hand,dealer_hand)
    
    
    print (f'\nPlayer chips stand at {player_chips.total}')
    # Ask to play again
    new_game = input('Would you like to play again? Enter Y or N: ')
           
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print ('Thanks for playing! Gambling is bad!')
        break

#END OF CODE