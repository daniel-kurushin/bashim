from json import dump, load
from rutermextract import TermExtractor
from tkinter import *
from threading import Thread
from queue import Queue, Empty

te = TermExtractor()
rez = load(open('./data/trigrams.json', 'r'))
root = Tk()
tk_message = StringVar()
th = None
t = None
_in  = Queue()
_out = Queue()

def compare(S1,S2):
    ngrams = [S1[i:i+3] for i in range(len(S1))]
    count = 0
    for ngram in ngrams:
        count += S2.count(ngram)

    return count/max(len(S1), len(S2))

def speak():
    while 1:
        q_message = _in.get()
        q_terms = set(te(q_message, strings=1, nested=1))
        
        candidates = []
        
        for ngram in rez:
            for part in ngram:
                message, terms = part[0], set(part[1])
                l1 = compare(message.lower(), q_message.lower())
                try:
                    l2 = len(terms & q_terms) / max(len(terms), len(q_terms))
                except ZeroDivisionError:
                    l2 = 0
                
                candidates += [(l1 + l2, message, ngram)]
    
        out = sorted(candidates, key = lambda x: x[0])[-1]
        # print(q_terms, out, candidates)
        _out.put(out[1])

def check():
    global t
    global th
    try:
        out = str(_out.get(timeout = 0, block = 0))
        t.insert(END, "bashim: " + out + "\n")
    except Empty:
        root.after(500, check)
    
def ask(e):
    global t
    global th
    t.insert(END, "user: " + tk_message.get() + "\n")
    _in.put(tk_message.get())
    root.after(500, check)
    tk_message.set("")

def test():
    pass
    
th = Thread(target=speak)
th.setDaemon(1)
th.start()
e = Entry(root, textvariable = tk_message)
t = Text(root, width=25, height=40)
e.bind('<Return>', ask)
t.pack()
e.pack()
root.mainloop()
