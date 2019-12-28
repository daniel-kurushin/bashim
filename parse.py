import re

from bs4 import BeautifulSoup
from requests import get
from json import dump
from sys import stderr

re_friends = re.compile("(^\d+:)|(^\<?.*?\>)|(^\w+:)|(^-\s?)")

URL = './bash/%s'
MIN = 1
MAX = 3068
#MAX = 300 # временно

data = []

for n in range(MIN, MAX+1):
    print("Обработка %s .." % (URL % n), file = stderr, flush = 1, end = '')
    try:
        bash = BeautifulSoup(open(URL % n).read(), 'lxml')
        quotes = bash('div', {'class':'quote__body'})
        for quote in quotes:
            strings = []
            for child in quote.children:
                try:
                    s = child.text
                except AttributeError:
                    s = str(child)
                s = s.replace('\n',' ').strip(' ')
                if s and ('Комикс по мотивам цитаты' not in s and "Комиксы по мотивам цитаты" not in s):
                    strings += [s]
            friends = set()
            for x in strings:
                try:
                    for m in re.match(re_friends, x).groups():
                        friends |= {m}
                    friends -= {None}
                except AttributeError:
                    pass
            friends = list(friends)
            try:
                assert len(friends) == 2, 'Dialog is for two'
                quo = {'url': URL % n}
                m = 0
                for s in strings:
                    for friend in friends:
                        try:
                            p = s.index(friend)
                            assert p == 0
                            l = len(friend)
                            n = friends.index(friend)
                            quo.update({"(%s, %s)" % (m,n):[s[l:].strip()]})
                            m += 1
                        except (AssertionError, ValueError):
                            pass
            except AssertionError:
                pass
                
            data += [quo]
        print(". сделано.", file = stderr)
    except FileNotFoundError as e:
        print(". ошибка! %s" % e, file = stderr)
dump(data, open('./data/bashim.json', 'w'), indent=4, ensure_ascii=0)
