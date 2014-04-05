from model.dish import Dish
from model.dict_entry import Dict_Entry 
from model.food_word import Food_Word 
from model.base import db_session
import config
import datetime as dt

from timing import time_elapsed

CHAINS = {}

def find_words(text):
    """Find all combinations of sequential characters within a string of characters."""
    print "finding combinations"
    length = len(text)
    n = length - 1
    num_combos = 2 ** (length - 1)

    bins = []
    for i in range(num_combos):
        num = bin(i).rsplit('b', 1)[1]
        num_str = num.zfill(n)
        bins.append(num_str)

    total_combos = []
    for binary_num in bins:
        combo = []
        for i in range(n):
            if binary_num[i] == '1':
                combo.append(text[i])
                combo.append(',')
            else:
                combo.append(text[i])

        combo.append(text[-1])
        combo = ''.join(combo)
        combo = combo.split(',')
        total_combos.append(combo)

    return total_combos

def check_words(combinations):
    """Go through all the combinations of words and find their definitions using
    food_words and the dictionary."""
    translations = []
    for c in combinations:
        translation = []
        found_def = True
        for char in c:
            food_word = Food_Word.find_match(char)
            if food_word:
                translation.append(food_word.get_json())
            else:
                entries = Dict_Entry.find_matches(char)
                if entries != []:
                    for entry in entries:
                        translation.append(entry.get_json())
                elif len(char) == 1:
                    # If the character isn't in the dictionary (usually punctuation)
                    d = {
                        "char": char,
                        "pinyin": "",
                        "english": "" 
                    }
                    translation.append(d)
                else:
                    found_def = False
                    break
        if found_def:
            return translation

def translate(text):
    """Attempt to translate text using food_words and then the CEDICT dictionary."""
    start = dt.datetime.now()
    words = find_words(text)
    start = time_elapsed("Find words", start)
    results = check_words(words)
    start = time_elapsed("Check words", start)
    return results


def search_dish_name(text):
    """Searches for text in the dishes database. If not found, translates text and
    looks for similar dishes in database. Returns JSON data for dish or search results."""

    # timing information, can delete later.
    start = dt.datetime.now()

    results = {}
    if type(text) != unicode:
        text = text.decode('utf-8')
    if len(text) > 10:
        # Most dish names are 3-5 characters. 
        # If Tesseract returned more than 10 characters, something probably went wrong.
        print "Input text is too long."
        return None
    else:
        # Find a matching dish, if it exists.
        match = Dish.find_match(text)
        if match:
            # If result is found, return JSON representation of dish.
            results = match.get_json()
            start = time_elapsed("Dish lookup", start)
        else:
            # If no dish is found, return translation data and similar dishes, if they exist.
            translation = translate(text)
            start = time_elapsed("Translation", start)
            results['translation'] = translation

            # Find similar dishes and add to results.
            if len(text) > 1:
                similar_dishes = Dish.find_similar(text)
                start = time_elapsed("Similar dish lookup", start)
                similar_json = []            
                for similar_dish in similar_dishes:
                    dish_data = similar_dish.get_json_min()
                    print dish_data
                    similar_json.append(dish_data)

                if similar_json != []:
                    results['similar'] = similar_json

    return results

##### UNUSED FUNCTIONS #######
# I was contemplating using Markov chains for text correction, but 
# I haven't implemented that yet.
def find_substitutes(text):
    """Try to guess what incorrect characters might be..."""
    if CHAINS == {}:
        generate_food_chains()

    candidates = []
    subs = []
    for i in range(len(text)):
        char = text[i]
        if CHAINS.get(char):
            print "found char %s" % char
            candidates = []
            candidates = CHAINS[char]
        else:
            print "didn't find char %s" % char
            if candidates != []:
                # choose the most popular option from candidates
                counts = {}
                for candidate in candidates:
                    if counts.get(candidate):
                        counts[candidate] += 1
                    else:
                        counts[candidate] = 1
                max_count = 0
                chosen = None
                for candidate, count in counts.iteritems():
                    if count > max_count:
                        max_count = count
                        chosen = candidate
                if chosen:
                    subs.append((chosen, i))

                candidates = []
    return subs

def generate_food_chains():
    words = []
    food_words = Food_Word.get_all_words()
    dishes = Dish.get_all_dishes()
    words.extend(food_words)
    words.extend(dishes)

    # Generate Markov chains. 
    # Since dish names are short, I'm using an n-gram size of 1.
    for i in range(len(words)):
        word = words[i]
        for j in range(len(word) - 1):
            char = word[j]
            next = word[j + 1]
            if CHAINS.get(char):
                CHAINS[char].append(next)
            else:
                CHAINS[char] = [next]


 
