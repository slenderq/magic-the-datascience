import random
import pprint
import numpy as np
from PIL import Image
import math as m
# from mtgtools.MtgDB import MtgDB
# db = MtgDB("cards.fs")

# scryfall_cards = db.root.scryfall_cards
# print(scryfall_cards)

def commander_stats(shuffle_func):
    # play 100 games
    values = np.array([])

    for i in range(0,10000):
        deck = list(range(0,100))
        # shuffle time > 50
        shuffled_deck = shuffle_func(deck.copy(), shuffle_times=60)

        # baseline is without a shuffle
        baseline_score = score_shuffle(deck)
        
        # print(f"baseline: {baseline_score}")
        # print(f"perfect deck score: {baseline_score/score_shuffle(perfect_deck)}")
        # print(f"yugioh deck score: {baseline_score/score_shuffle(yugi_deck)}")
        
        values = np.append(values, baseline_score/score_shuffle(shuffled_deck))

        if i == 0:
            render_image_deck(deck, "baseline")
            render_image_deck(shuffled_deck, shuffle_func.__name__)

    
    return np.mean(values, axis=0)
    

def combo_shuffle(deck, shuffle_times=50):
    
    deck = yugioh_shuffle(deck, 10)
    deck = stack_shuffle(deck, 50)
    return deck

    # pprint.pprint(perfect_deck,compact=True)
def stack_shuffle(deck, shuffle_times=10):
    deck = deck.copy()
    ndeck = np.array(deck)
    cards = len(ndeck)

    n_stacks = 8 

    #does not work at the moment


    for i in range(0, m.floor(shuffle_times/50)):

        # stacks = np.empty([n_stacks,1])
        stacks = []
        for i in range(0, n_stacks):
            stacks.append([])
        # nstacks = np.array(stacks)
        stack_num = 0
        for card_num, elm in enumerate(np.nditer(ndeck)):

            stacks[stack_num].append(int(elm))

            stack_num += 1
            if n_stacks - 1 < stack_num:
                stack_num = 0
            
            
        # put them together
        ndeck = np.hstack(stacks)
    
    return ndeck


    
def yugioh_shuffle(deck, chunksize_coff=25, shuffle_times=10):
    deck = deck.copy()
    ndeck = np.array(deck)
    cards = len(ndeck)

    # adds random cards
    for i in range(0, shuffle_times):
        left = random.randint(1,99)
        right = left + random.randint(1, chunksize_coff)

        if right > cards: 
            right = cards 
            
        chunk = ndeck[left:right].copy()
        cut = np.delete(ndeck.copy(), slice(left, right))

        
        if random.choice([True, False]):
            ndeck =np.append(chunk, cut)
        else:
            ndeck = np.append(cut, chunk)

        if ndeck.size != 100:
            # ndeck = np.unique(ndeck)
            print(i)
            print(chunk)
            print(cut)
            print(left, right)
        
            print(f"{ndeck}")
            print(ndeck.size)

    # should not need this but we get extra cards!

    return ndeck
            
           
        
    # take a chunk
    # move it to the end or front
    ...

def perfect_shuffle(deck, shuffle_times = 10):
    deck = deck.copy()

    for i in range(0,int(shuffle_times)):
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
    # agg = np.average(difference)
    return difference

def render_image_deck(deck, shuffle_name):
    
    
    deck = deck.copy()
    ndeck = np.array(deck)

    # divede by some max 
    diveded = ndeck/(len(ndeck))
    image = diveded * 255
    
    # assuming deck is 100
    image= np.reshape(image, [10,-1])
    

    size = (1500,1500)
    image_ob = Image.fromarray(image).convert("L")
    image_ob = image_ob.resize(size, resample= Image.NEAREST)
    image_ob.save(f"{shuffle_name}.png",move='w')
    # multiply by 255
    # https://www.delftstack.com/howto/matplotlib/convert-a-numpy-array-to-pil-image-python/

    pass


print(f"combo shuffle {commander_stats(combo_shuffle)}")
print(f"stack shuffle {commander_stats(stack_shuffle)}")
print(f"perfect_shuffle {commander_stats(perfect_shuffle)}")
print(f"yugioh {commander_stats(yugioh_shuffle)}")