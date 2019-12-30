from json import dump, load, dumps
from rutermextract import TermExtractor
from pymorphy2 import MorphAnalyzer 
from nltk import WordPunctTokenizer
from time import time

from pprint import pprint

wpt = WordPunctTokenizer()
te = TermExtractor()
ma = MorphAnalyzer()

data = load(open('./data/bashim.json', 'r'))

#dump(data, open('/tmp/out.json', 'w'), indent=4, ensure_ascii=0)

messages = ["<|BEGIN|>"]
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
n, m = 0, 0
t = int(time())
l = len(messages)

for message in messages:
    if message == "<|BEGIN|>":
        ngram = []
    elif message == "<|END|>":
        phrases = []
        for phrase in ngram:
            terms = set(te(phrase, strings=1, nested=1))
            words = list(set([ ma.parse(w)[0].normal_form for w in wpt.tokenize(phrase) ]))
            idx = []
            for word in words:
                w = 1 if word in terms else .5
                idx += [(w, word)]
            phrases += [(idx, phrase)]
        ngrams += [phrases]
    else:
        ngram += [message]
    n += 1
    if time() - t > 1:
        print("%s of %s, %s / sec" % (m, l, n))
        m += n
        n = 0
        t = int(time())
    
dump(ngrams, open('./data/trigrams.json', 'w'), indent=2, ensure_ascii=0)
