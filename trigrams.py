from json import dump, load
from rutermextract import TermExtractor

te = TermExtractor()
data = load(open('./data/bashim.json', 'r'))

#dump(data, open('/tmp/out.json', 'w'), indent=4, ensure_ascii=0)

messages = []
n = 0
for quo in data:
    try:
        for message in range(100):
            try:
                s = quo["(%s, 0)" % message]
            except KeyError:
                s = quo["(%s, 1)" % message]
            messages += s
    except KeyError:
        pass
    
ngrams = set([ tuple(messages[i:i+3]) for i in range(len(messages) - 2)])

rez = []

for ngram in ngrams:
    keys = []
    for message in ngram:
        terms = list(set(te(message, strings=1, nested=1)))
        keys += [(message, terms)]
    rez += [keys]
    

dump(rez, open('./data/trigrams.json', 'w'), indent=4, ensure_ascii=0)
