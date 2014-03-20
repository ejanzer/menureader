from model.dish import Dish
from model.dict_entry import Dict_Entry 
from model.food_word import Food_Word 
from model.base import db_session

def find_words(text):
    """Find all combinations of sequential characters within a string of characters."""
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
        chars = []
        for char in c:
            food_word = Food_Word.find_match(char)
            #food_word = db_session.query(Food_Word).filter_by(simplified=char).first()
            if food_word:
                chars.append(food_word)
            else:
                entry = Entry.find_match(char)
                #entry = session.query(Entry).filter_by(simplified=char).first()
                if entry:
                    chars.append(entry)
                else:
                    found_def = False
                    break
            
        if found_def:
            return chars

def translate(text):
    """Attempt to translate text using food_words and then the CEDICT dictionary."""
    words = find_words(text)


def search(text):
    if type(text) != unicode:
        print "Oops, what went wrong here?"
        return None
    elif len(text) > 10:
        print "Input text is too long."
        return None
    else:
        match = Dish.find_match(text)

        if match:
            return match
        else:
            translations = translate(text)
            similar = Dish.find_similar(text)


