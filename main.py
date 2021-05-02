import random
import pprint
import numpy as np
# from mtgtools.MtgDB import MtgDB
# db = MtgDB("cards.fs")

# scryfall_cards = db.root.scryfall_cards
# print(scryfall_cards)

def commander_stats():
    deck = list(range(0,100))

    perfect_deck = perfect_shuffle(deck.copy())
    baseline_score = score_shuffle(deck)
    print(f"baseline: {baseline_score}")
    print(f"perfect deck score: {baseline_score/score_shuffle(perfect_deck)}")
    pprint.pprint(perfect_deck,compact=True)
    

def perfect_shuffle(deck):
    deck = deck.copy()

    for i in range(0,int(1e3)):
        i = random.randint(0,99)
        j = random.randint(0,99)

        if i == j:
            continue

        # print("swap")
        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp
    
    return deck
    
def score_shuffle(deck):
    deck = deck.copy()
    ndeck = np.array(deck)
    off_deck = np.roll(ndeck, 1)

    difference = ndeck.dot(off_deck)
    print(difference)
    agg = np.average(difference)
    return agg

commander_stats()