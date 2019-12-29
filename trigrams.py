from json import dump, load, dumps
from rutermextract import TermExtractor
from pymorphy2 import MorphAnalyzer 
from nltk import WordPunctTokenizer

from pprint import pprint

wpt = WordPunctTokenizer()
te = TermExtractor()
ma = MorphAnalyzer()

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

# pprint(messages)

ngrams = []
for message in messages:
    if message == "<|BEGIN|>":
        ngram = []
    elif message == "<|END|>":
        phrases = []
        for phrase in ngram:
            terms = list(set(te(phrase, strings=1, nested=1)))
            words = list(set([ ma.parse(w)[0].normal_form for w in wpt.tokenize(phrase) ]))
            phrases += [(terms, words, phrase)]
        ngrams += [phrases]
    else:
        ngram += [message]
    
#ngrams = set([ tuple(messages[i::i+3]) for i in range(len(messages) - 2)])

print(dumps(ngrams, ensure_ascii = 0, indent = 2))

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
