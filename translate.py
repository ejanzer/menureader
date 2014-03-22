from model.dish import Dish
from model.dict_entry import Dict_Entry 
from model.food_word import Food_Word 
from model.base import db_session

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
    for c in combinations:
        found_def = True
        translation = []
        for char in c:
            food_word = Food_Word.find_match(char)
            if food_word:
                translation.append(food_word.get_json())
            else:
                entries = Dict_Entry.find_matches(char)
                if entries != []:
                    for entry in entries:
                        translation.append(entry.get_json())
                else:
                    found_def = False
                    break
            
        if found_def:
            return translation

def translate(text):
    """Attempt to translate text using food_words and then the CEDICT dictionary."""
    words = find_words(text)
    results = check_words(words)
    return results


def get_results_json(text):
    print "Searching for text", text
    results = {}
    if type(text) != unicode:
        text = text.decode('utf-8')
    if len(text) > 10:
        print "Input text is too long."
        return None
    else:
        # Find a matching dish, if it exists.
        match = Dish.find_match(text)
        print "match is", match
        if match:
            results = match.get_json()
        else:
            translation = translate(text)
            results['translation'] = translation

            # Find similar dishes and add to results.
            similar_dishes = Dish.find_similar(text)
            similar_json = []            
            for similar_dish in similar_dishes:
                similar_json.append(similar_dish.get_json())
                
            results['similar'] = similar_json

    return results
