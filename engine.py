import numpy as np

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

def main():

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

    print(agent0.getName() + " has " + cardToName(agent0.getCards()[0]) + " and " + cardToName(agent0.getCards()[1]))
    print(agent1.getName() + " has " + cardToName(agent1.getCards()[0]) + " and " + cardToName(agent1.getCards()[1]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal flop
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

    print("Turn: " + cardToName(visibleCards[3]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")

    #deal river
    visibleCards = np.append(visibleCards, np.random.choice(restOfDeck))
    restOfDeck = np.delete(restOfDeck, np.where(restOfDeck == visibleCards[4]))

    print("River: " + cardToName(visibleCards[4]))

    # calculate possible opponent hands
    agent0.possibleOpponentCards = calculatePossibleOpponentHands(agent0.getCards(), visibleCards, deck)
    agent1.possibleOpponentCards = calculatePossibleOpponentHands(agent1.getCards(), visibleCards, deck)

    print(agent0.getName() + "'s opponent has " + str(len(agent0.possibleOpponentCards)) + " possible hands")
    print(agent1.getName() + "'s opponent has " + str(len(agent1.possibleOpponentCards)) + " possible hands")
                           

    


    

if __name__ == "__main__":
    main()

