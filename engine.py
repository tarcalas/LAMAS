import numpy as np
from itertools import combinations
import copy

#I was thinking of representing the cards as numbers, with N%10 = 0 => A, N%10 = 1 => K, N%10 = 2 =>Q
#N/10 = 0 => Spades, N/10 = 1 => Hearts, N/10 = 2 => Diamonds, N/10 = 3 =>Clubs 
#So 0 = Ace of Spades, 31 = King of Clubs, etc.

#Also thinking about the different combinations as integers like 0 = 4 Aces, 1 = 4 Kings, etc.

#calculates the probability of winning from an agents perspective
# def probabilityOfWinning(agentsCards, visibleCards, agentsBestHand):
#     return probability

#deal cards
def dealInitialCards(deck):
    agent0Cards = np.array([])
    agent1Cards = np.array([])
    restOfDeck = deck

    #deal 1 card
    agent0Cards = np.append(agent0Cards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == agent0Cards[0]))

    #deal 1 card
    agent1Cards = np.append(agent1Cards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == agent1Cards[0]))

    #deal 1 card
    agent0Cards = np.append(agent0Cards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == agent0Cards[1]))

    #deal 1 card
    agent1Cards = np.append(agent1Cards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == agent1Cards[1]))

    return (agent0Cards, agent1Cards, restOfDeck)

#recursive approach is probably the best
# def bestHand(agentsCards, visibleCards, pickedCards):
#     return bestHandValue

def cardToName(card):
    suit = int(card/10)
    value = card%10

    if suit == 0:
        suitName = "Spades"
    elif suit == 1:
        suitName = "Hearts"
    elif suit == 2:
        suitName = "Diamonds"
    elif suit == 3:
        suitName = "Clubs"

    if value == 0:
        valueName = "Ace"
    elif value == 1:
        valueName = "King"
    elif value == 2:
        valueName = "Queen"

    return valueName + " of " + suitName

class Agent:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.possibleOpponentCards = []

    def setCards(self, cards):
        self.cards = cards

    def getCards(self):
        return self.cards

    def getName(self):
        return self.name

    def printCards(self):
        print(self.name + " has " + cardToName(self.cards[0]) + " and " + cardToName(self.cards[1]))

def calculatePossibleOpponentHands(agentsCards, visibleCards, deck):
    possibleOpponentCards = []

    for i in range(len(deck)):
        for j in range(i+1, len(deck)):
            possibleOpponentCards.append([deck[i], deck[j]])

    possibleOpponentCards = np.array(possibleOpponentCards)

    for i in range(len(agentsCards)):
        possibleOpponentCards = possibleOpponentCards[np.all(possibleOpponentCards != agentsCards[i], axis=1)]

    for i in range(len(visibleCards)):
        possibleOpponentCards = possibleOpponentCards[np.all(possibleOpponentCards != visibleCards[i], axis=1)]    

    return possibleOpponentCards

def calculateBestHand(hand1, hand2, visibleCards):
    #Quads > Trips > Two Pair > Pair > High Card

    #N%10 = 0 => A, N%10 = 1 => K, N%10 = 2 =>Q
    #N/10 = 0 => Spades, N/10 = 1 => Hearts, N/10 = 2 => Diamonds, N/10 = 3 =>Clubs 
    #So 0 = Ace of Spades, 31 = King of Clubs, etc.
    
    #check combinations of 5 cards in hand + visible cards
    hand1 = np.append(hand1, visibleCards)
    hand2 = np.append(hand2, visibleCards)

    hand_1_same_cards = -1
    hand_2_same_cards = -1
    value1 = -1
    value2 = -1

    for hand in combinations(hand1, 5):
        
        #check for quads
        hand_freqs = [card % 10 for card in hand]

        #convert to int 
        hand_freqs = np.array(hand_freqs, dtype=int) 

        hand_freqs = np.bincount(hand_freqs)
        if 4 in hand_freqs:
            if hand_1_same_cards < 4 or(hand_1_same_cards == 3 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 4
                value1 = np.argmax(hand_freqs)
        elif 3 in hand_freqs:
            if hand_1_same_cards < 3 or (hand_1_same_cards == 3 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 3
                value1 = np.argmax(hand_freqs)
        elif 2 in hand_freqs:
            if hand_1_same_cards < 2 or (hand_1_same_cards == 2 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 2
                value1 = np.argmax(hand_freqs)
        else:
            if hand_1_same_cards < 1 or (hand_1_same_cards == 1 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 1
                value1 = np.argmax(hand_freqs)

    for hand in combinations(hand2, 5):
        
        #check for quads
        hand_freqs = [card % 10 for card in hand]

        #convert to int 
        hand_freqs = np.array(hand_freqs, dtype=int)    

        hand_freqs = np.bincount(hand_freqs)
        if 4 in hand_freqs:
            if hand_2_same_cards < 4 or(hand_2_same_cards == 3 and value2 > np.argmax(hand_freqs)):
                hand_2_same_cards = 4
                value2 = np.argmax(hand_freqs)
        elif 3 in hand_freqs:
            if hand_2_same_cards < 3 or (hand_2_same_cards == 3 and value2 > np.argmax(hand_freqs)):
                hand_2_same_cards = 3
                value2 = np.argmax(hand_freqs)
        elif 2 in hand_freqs:
            if hand_2_same_cards < 2 or (hand_2_same_cards == 2 and value2 > np.argmax(hand_freqs)):
                hand_2_same_cards = 2
                value2 = np.argmax(hand_freqs)
        else:
            if hand_2_same_cards < 1 or (hand_2_same_cards == 1 and value2 > np.argmax(hand_freqs)):
                hand_2_same_cards = 1
                value2 = np.argmax(hand_freqs)

    if value1 == 0:
        valueName1 = "Ace"
    elif value1 == 1:
        valueName1 = "King"
    elif value1 == 2:
        valueName1 = "Queen"

    if value2 == 0:
        valueName2 = "Ace"
    elif value2 == 1:
        valueName2 = "King"
    elif value2 == 2:
        valueName2 = "Queen"

    if hand_1_same_cards > hand_2_same_cards:
        return 1
    elif hand_1_same_cards < hand_2_same_cards:
        return 2
    else:
        if value1 < value2:
            return 1
        elif value1 > value2:
            return 2
        else:
            return 0

def print_best_hand(agent, visibleCards):
    #Quads > Trips > Two Pair > Pair > High Card

    #N%10 = 0 => A, N%10 = 1 => K, N%10 = 2 =>Q
    #N/10 = 0 => Spades, N/10 = 1 => Hearts, N/10 = 2 => Diamonds, N/10 = 3 =>Clubs 
    #So 0 = Ace of Spades, 31 = King of Clubs, etc.
    
    #check combinations of 5 cards in hand + visible cards
    hand1 = agent.getCards()
    hand1 = np.append(hand1, visibleCards)
    print("\n")
    print("The combined hand of " + agent.getName() + " is: ")
    for i in range(len(hand1)):
        print(cardToName(hand1[i]))

    hand_1_same_cards = -1
    value1 = -1

    for hand in combinations(hand1, 5):
        
        #check for quads
        hand_freqs = [card % 10 for card in hand]

        #convert to int 
        hand_freqs = np.array(hand_freqs, dtype=int) 
        
        hand_freqs = np.bincount(hand_freqs)
        if 4 in hand_freqs:
            if hand_1_same_cards < 4 or(hand_1_same_cards == 3 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 4
                value1 = np.argmax(hand_freqs)
        elif 3 in hand_freqs:
            if hand_1_same_cards < 3 or (hand_1_same_cards == 3 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 3
                value1 = np.argmax(hand_freqs)
        elif 2 in hand_freqs:
            if hand_1_same_cards < 2 or (hand_1_same_cards == 2 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 2
                value1 = np.argmax(hand_freqs)
        else:
            if hand_1_same_cards < 1 or (hand_1_same_cards == 1 and value1 > np.argmax(hand_freqs)):
                hand_1_same_cards = 1
                value1 = np.argmax(hand_freqs)

    if value1 == 0:
        valueName1 = "Ace"
    elif value1 == 1:
        valueName1 = "King"
    elif value1 == 2:
        valueName1 = "Queen"

    print("\nThe best combination of cards agnt"   + agent.getName() + " has is: ")
    print(agent.getName() + " has " + str(hand_1_same_cards) + " " + valueName1 + "s")

def calculateWinningProbability(agent, visibleCards):

    games = 0
    wins = 0
    for hand in agent.possibleOpponentCards:
        if calculateBestHand(agent.getCards(), hand, visibleCards) == 1:
            wins += 1
        games += 1

    return wins/games

def calculateWinningProbabilityCards(myhand, opponentHands, visibleCards):
    games = 0
    wins = 0
    for hand in opponentHands:
        if calculateBestHand(myhand, hand, visibleCards) == 1:
            wins += 1
        games += 1

    return wins/games
    
def recalculatewinningProbability(agent, opponentPercentage, visibleCards, deck):
    tmp_hands = copy.deepcopy(agent.possibleOpponentCards)

    filtered_hands = []  # Create a new list to store valid hands

    # For each hand that the opponent might have
    for i in tmp_hands:

        # Generate the opponents' thoughts about my possible hands
        myPossibleHands = calculatePossibleOpponentHands(i, visibleCards, deck)


        # Use the generated possible hands to calculate the probability of winning
        percentage = calculateWinningProbabilityCards(i, myPossibleHands, visibleCards)
        if percentage == opponentPercentage:
            filtered_hands.append(i)  # Only add matching hands

    return filtered_hands

    
def main():
    #set random seed for demo
    np.random.seed(3)

    #initialize deck and comunity cards
    deck = np.array([0,1,2,10,11,12,20,21,22,30,31,32])
    visibleCards = np.array([])

    # initialize agents
    agent0 = Agent("Agent 0")
    agent1 = Agent("Agent 1")

    #deal initial cards
    agent0Cards, agent1Cards, restOfDeck = dealInitialCards(deck)

    agent0.setCards(agent0Cards)
    agent1.setCards(agent1Cards)

    agent0.printCards()
    agent1.printCards()

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    if input("Press enter to deal the flop...") == "exit":
        return

    #deal flop
    print("\nDealing the flop... ")
    for i in range(3):
        visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
        restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[i]))

    print("Flop: " + cardToName(visibleCards[0]) + ", " + cardToName(visibleCards[1]) + ", " + cardToName(visibleCards[2]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal turn
    visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[3]))

    if input("Press enter to deal the turn...") == "exit":
        return

    print("\nDealing the turn... ")
    print("Turn: " + cardToName(visibleCards[3]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal river
    visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[4]))

    if input("Press enter to deal the river...") == "exit":
        return

    print("\nDealing the river... ")
    print("River: " + cardToName(visibleCards[4]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #print best hand

    if input("Press enter to see the best hands...") == "exit":
        return

    print_best_hand(agent0, visibleCards)
    print_best_hand(agent1, visibleCards)
                           
    #calculate winning probability
    agent0WinningProbability = calculateWinningProbability(agent0, visibleCards)
    agent1WinningProbability = calculateWinningProbability(agent1, visibleCards)

    if input("Press enter to see the winning probabilities...") == "exit":
        return

    print(agent0.getName() + "'s winning probability is " + str(agent0WinningProbability))
    print(agent1.getName() + "'s winning probability is " + str(agent1WinningProbability))

    recalculatedHands0 = recalculatewinningProbability(agent0, agent1WinningProbability, visibleCards, deck)
    recalculatedHands1 = recalculatewinningProbability(agent1, agent0WinningProbability, visibleCards, deck)

    agent0.possibleOpponentCards = recalculatedHands0
    agent1.possibleOpponentCards = recalculatedHands1

    agent0WinningProbability = calculateWinningProbability(agent0, visibleCards)
    agent1WinningProbability = calculateWinningProbability(agent1, visibleCards)

    if input("Press enter to see the recalculated probabilities...") == "exit":
        return

    #print cards and possible opponent cards
    print("\nAgent 0's recalculated possible opponent's cards: ")
    for card in agent0.possibleOpponentCards:
        print(cardToName(card[0]) + ", " + cardToName(card[1]))

    print("\nAgent 1's recalculated possible opponent's cards: ")
    for card in agent1.possibleOpponentCards:
        print(cardToName(card[0]) + ", " + cardToName(card[1]))

    print(agent0.getName() + "'s winning probability is " + str(agent0WinningProbability))
    print(agent1.getName() + "'s winning probability is " + str(agent1WinningProbability))



if __name__ == "__main__":
    main()

