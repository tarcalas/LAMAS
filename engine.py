import numpy as np
from itertools import combinations
import copy
import sys

def dealInitialCards(deck):
    """
    Deals the initial cards to the agents
    params:
        deck:   the deck of cards
    """


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

def cardToName(card):
    """
    Prints the name of a card
    params:
        card:   the card to print the name of
    """


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
    elif value == 3:
        valueName = "Jack"
    elif value == 4:
        valueName = "10"
    elif value == 5:
        valueName = "9"

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
    """
    Calculates the possible hands of the opponent given the cards of the agent and the visible cards
    params: 
        agentsCards:    the cards of the agent
        visibleCards:   the cards that are visible
        deck:           the deck of cards
    """

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
    """
    Calculates the best hand between two agents, used for comparison for winning
    params: 
        hand1:          the hand of the first agent
        hand2:          the hand of the second agent
        visibleCards:   the cards that are visible
    """
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
    """
    prints the best hand of an agent
    params: 
        agent:          the agent to print the best hand for
        visibleCards:   the cards that are visible
    """
    
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
    elif value1 == 3:
        valueName1 = "Jack"
    elif value1 == 4:
        valueName1 = "10"
    elif value1 == 5:
        valueName1 = "9"

    print("\nThe best combination of cards "   + agent.getName() + " has is: ")
    print(agent.getName() + " has " + str(hand_1_same_cards) + " " + valueName1 + "s")

def calculateWinningProbability(agent, visibleCards):
    """
    Calculates the probability of winning given the possible hands of the opponent
    params: 
        agent:          the agent to calculate the probability for
        visibleCards:   the cards that are visible
    """

    games = 0
    wins = 0
    for hand in agent.possibleOpponentCards:
        if calculateBestHand(agent.getCards(), hand, visibleCards) == 1:
            wins += 1
        games += 1

    if games == 0:
        return 0

    return wins/games

def calculateWinningProbabilityCards(myhand, opponentHands, visibleCards):
    """
    Calculates the probability of winning given the possible hands of the opponent
    params: 
        myhand:             the hand of the agent
        opponentHands:      the possible hands of the opponent
        visibleCards:       the cards that are visible
    """
    games = 0
    wins = 0
    for hand in opponentHands:
        if calculateBestHand(myhand, hand, visibleCards) == 1:
            wins += 1
        games += 1

    if games == 0:
        return 0
    
    return wins/games
    
def reclaculateHandsWithProbabilityDiscrete(agent, opponentPercentage, visibleCards, deck):

    """
    Recalculates the possible hands of the opponent given the probability of winning
    This function rounds to the nearest 0.1, thus modeling 10 atoms each representing 0.1 probability
    params: 
        agent:                  the agent to recalculate the hands for
        opponentPercentage:     the probability of the opponent winning
        visibleCards:           the cards that are visible
        deck:                   the deck of cards
    """
        
    tmp_hands = copy.deepcopy(agent.possibleOpponentCards)

    filtered_hands = []  # Create a new list to store valid hands

    # For each hand that the opponent might have
    for i in tmp_hands:

        # Generate the opponents' thoughts about my possible hands
        myPossibleHands = calculatePossibleOpponentHands(i, visibleCards, deck)

        # Use the generated possible hands to calculate the probability of winning
        percentage = calculateWinningProbabilityCards(i, myPossibleHands, visibleCards)

        if round(percentage, 1) == round(opponentPercentage, 1):
            filtered_hands.append(i)  # Only add matching hands

    return filtered_hands
    
def main():

    #argument for seed 
    if "seed" in sys.argv:
        seed = sys.argv[sys.argv.index("seed") + 1]
        np.random.seed(int(seed))


    #initialize deck and comunity cards
    deck = np.array([0,1,2,10,11,12,20,21,22,30,31,32])
    visibleCards = np.array([])

    #extended deck
    if "extended" in sys.argv:
        deck = np.append(deck, [3,4,5,13,14,15,23,24,25,33,34,35])

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

    print("\n")
    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    print("\n")
    if input("Press enter to deal the flop...") == "exit":
        return

    #deal flop
    for i in range(3):
        visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
        restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[i]))

    print("\n")
    print("Flop: " + cardToName(visibleCards[0]) + ", " + cardToName(visibleCards[1]) + ", " + cardToName(visibleCards[2]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal turn
    visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[3]))

    print("\n")
    if input("Press enter to deal the turn...") == "exit":
        return

    print("\nTurn: " + cardToName(visibleCards[3]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal river
    visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[4]))

    print("\n")
    if input("Press enter to deal the river...") == "exit":
        return

    print("\nRiver: " + cardToName(visibleCards[4]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #print best hand
    print("\n")
    if input("Press enter to see the best hands...") == "exit":
        return

    print_best_hand(agent0, visibleCards)
    print_best_hand(agent1, visibleCards)
                           
    #calculate winning probability
    agent0WinningProbability = calculateWinningProbability(agent0, visibleCards)
    agent1WinningProbability = calculateWinningProbability(agent1, visibleCards)
    print("\n")
    if input("Press enter to see the winning probabilities...") == "exit":
        return

    print(agent0.getName() + "'s winning probability is " + str(agent0WinningProbability))
    print(agent1.getName() + "'s winning probability is " + str(agent1WinningProbability))

    print("\n")
    if input("Press enter to see the recalculated probabilities...") == "exit":
        return
    
    oldAgent0WinningProbability = agent0WinningProbability
    oldAgent1WinningProbability = agent1WinningProbability

    recalculatedHands0 = reclaculateHandsWithProbabilityDiscrete(agent0, agent1WinningProbability, visibleCards, deck)
    recalculatedHands1 = reclaculateHandsWithProbabilityDiscrete(agent1, agent0WinningProbability, visibleCards, deck)

    agent0.possibleOpponentCards = recalculatedHands0
    agent1.possibleOpponentCards = recalculatedHands1

    agent0WinningProbability = calculateWinningProbability(agent0, visibleCards)
    agent1WinningProbability = calculateWinningProbability(agent1, visibleCards)

    steps_to_convergence = 1

    while (oldAgent0WinningProbability != agent0WinningProbability or oldAgent1WinningProbability != agent1WinningProbability) and steps_to_convergence < 100 and (agent0WinningProbability != 0 and agent1WinningProbability != 0):
        steps_to_convergence += 1
        recalculatedHands0 = reclaculateHandsWithProbabilityDiscrete(agent0, agent1WinningProbability, visibleCards, deck)
        recalculatedHands1 = reclaculateHandsWithProbabilityDiscrete(agent1, agent0WinningProbability, visibleCards, deck)

        agent0.possibleOpponentCards = recalculatedHands0
        agent1.possibleOpponentCards = recalculatedHands1

        oldAgent0WinningProbability = agent0WinningProbability
        oldAgent1WinningProbability = agent1WinningProbability

        agent0WinningProbability = calculateWinningProbability(agent0, visibleCards)
        agent1WinningProbability = calculateWinningProbability(agent1, visibleCards)
    
    print("\n")
    print("Converged in " + str(steps_to_convergence) + " steps")

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

