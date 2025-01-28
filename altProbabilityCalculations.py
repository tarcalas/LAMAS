from itertools import combinations
import copy
import random
import numpy as np
from engine import *

def recalculateHandsWithProbability(agent, opponentPercentage, visibleCards, deck):
    """
    Recalculates the possible hands of the opponent given the probability of winning
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
        if percentage == opponentPercentage:
            filtered_hands.append(i)  # Only add matching hands

    return filtered_hands

def reclaculateHandsWithProbabilityThreshold(agent, opponentPercentage, visibleCards, deck):
    """
    Recalculates the possible hands of the opponent given the probability of winning
    This function uses a threshold to determine if the probability is high or low
    params: 
        agent:                  the agent to recalculate the hands for
        opponentPercentage:     the probability of the opponent winning
        visibleCards:           the cards that are visible
        deck:                   the deck of cards
    """

    threshold = 0.5
    if opponentPercentage > threshold:
        high = True
    else:
        high = False
        
    tmp_hands = copy.deepcopy(agent.possibleOpponentCards)

    filtered_hands = []  # Create a new list to store valid hands

    # For each hand that the opponent might have
    for i in tmp_hands:

        # Generate the opponents' thoughts about my possible hands
        myPossibleHands = calculatePossibleOpponentHands(i, visibleCards, deck)

        # Use the generated possible hands to calculate the probability of winning
        percentage = calculateWinningProbabilityCards(i, myPossibleHands, visibleCards)
        if percentage > threshold:
            calculated_high = True
        else:
            calculated_high = False

        if calculated_high == high:
            filtered_hands.append(i)  # Only add matching hands

    return filtered_hands
