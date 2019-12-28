from json import dump, load
from rutermextract import TermExtractor
from pprint import pprint

te = TermExtractor()
data = load(open('./data/bashim.100.json', 'r'))

#dump(data, open('/tmp/out.json', 'w'), indent=4, ensure_ascii=0)

messages = ["<|BEGIN|>"]
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
        messages += ["<|END|>"]
        messages += ["<|BEGIN|>"]

messages = messages[:-1]

pprint(messages)

ngrams = []
for message in messages:
    if message == "<|BEGIN|>":
        ngram = []
    elif message == "<|END|>":
        ngrams += [ngram]
    else:
        ngram += [message]
    
#ngrams = set([ tuple(messages[i::i+3]) for i in range(len(messages) - 2)])

pprint(ngrams)

#rez = []
#
#for ngram in ngrams:
#    keys = []
#    for message in ngram:
#        
#        keys += [(message, terms)]
#    rez += [keys]
#    
#
#dump(rez, open('./data/trigrams.json', 'w'), indent=4, ensure_ascii=0)
