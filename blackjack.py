import random
try:
    import tkinter
except ImportError:  #Python 2
    import Tkinter as tkinter


def load_images(card_images):
    suits = ['heart', 'spade', 'diamond', 'spade']
    face_cards = ['jack', 'queen','king']
    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'
    # for each suit, retrieve image for the cards
    for suit in suits:
        # first the number cards from 1 to 10
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card),suit,extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

            # next the face cards
            for card in face_cards:
                name = 'cards/{}_{}.{}'.format(str(card),suit,extension)
                image = tkinter.PhotoImage(file=name)
                card_images.append((10,image,))


def deal_card(frame):
    # pop the next card off the deck
    next_card = deck.pop(0)
    # add it back to the pack
    deck.append(next_card)
    # add the image to the label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calculate the total score of all cards in the list,
    # Only one ace can have the value of 11, and this will reduce to 1 if the hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 1
        score += card_value
        # if we would bust,check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
        return score


def deal_dealer():
    dealer_score = score_hand(dealer_hands)
    while 0 < dealer_score < 17:
        dealer_hands.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hands)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hands)
    if player_score > 21:
        result_text.set("Dealer wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
    else:
        result_text.set("Draw!!!")


def deal_player():
    player_hands.append(deal_card(player_card_frame))
    player_score = score_hand(player_hands)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer  wins!")


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hands
    global player_hands
    # embedded frame to hold card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='we', rowspan=2)

    # embedded frame to hold the images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    # Creating a list to store dealer's and player's hands
    dealer_hands = []
    player_hands = []

    deal_player()
    dealer_hands.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hands))
    deal_player()


    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # player_score += card_value
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # if the player bust check if there is an Ace and subtract
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")
def shuffle():
    random.shuffle(deck)


mainWindow = tkinter.Tk()

mainWindow.title("Blackjack")
mainWindow.geometry('640x480')
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='we', columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)

# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='we', rowspan=2)

player_score_label = tkinter.IntVar()
# player_score = 0
# player_ace = False
tkinter.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0,  columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text='Dealer', command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)

newGame_button = tkinter.Button(button_frame, text="New Game", command=new_game)
newGame_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)
# load cards
cards = []
load_images(cards)
print(cards)

# To create a new deck of cards and shuffle them
deck = list(cards) + list(cards) + list(cards)    # making use of 3 packs 
shuffle()

# Creating a list to store dealer's and player's hands
dealer_hands = []
player_hands = []

new_game()

mainWindow.mainloop()

