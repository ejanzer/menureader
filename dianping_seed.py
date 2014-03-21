import translate
import json
import codecs

with open('model/seeds/dianping_unknown.txt') as f:
    dishes = f.readlines()

w = codecs.open('model/seeds/dianping_translations.txt', 'a', encoding='utf-8')

for dish in dishes:
    dish = dish.strip('\n')
    dish = dish.decode('utf-8')
    results = translate.get_results_json(dish)
    print results['translation']

    w.write(dish)
    w.write(" : ")

    definition = ""
    for word in results['translation']:
        definition += " " + word['english']

    w.write(definition)
    w.write("\n")

w.close()