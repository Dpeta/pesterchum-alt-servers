import random

kbloc = [[x for x in "1234567890-="],
         [x for x in "qwertyuiop[]"],
         [x for x in "asdfghjkl:;'"],
         [x for x in "zxcvbnm,.>/?"]]
kbdict = {}
for (i, l) in enumerate(kbloc):
    for (j, k) in enumerate(l):
        kbdict[k] = (i, j)

sounddict = {"a": "e", "b": "d", "c": "k", "d": "g", "e": "eh",
             "f": "ph", "g": "j", "h": "h", "i": "ai", "j": "ge",
             "k": "c", "l": "ll", "m": "n", "n": "m", "o": "oa",
             "p": "b", "q": "kw", "r": "ar", "s": "ss", "t": "d",
             "u": "you", "v": "w", "w": "wn", "x": "cks", "y": "uy", "z": "s"}
             

def mispeller(word):
    if len(word) <= 6:
        num = 1
    else:
        num = random.choice([1,2])
    wordseq = range(0, len(word))
    random.shuffle(wordseq)
    letters = wordseq[0:num]
    def mistype(string, i):
        l = string[i]
        if not kbdict.has_key(l):
            return string
        lpos = kbdict[l]
        newpos = lpos
        while newpos == lpos:
            newpos = ((lpos[0] + random.choice([-1, 0, 1])) % len(kbloc),
                      (lpos[1] + random.choice([-1,0,1])) % len(kbloc[0]))
        string = string[0:i]+kbloc[newpos[0]][newpos[1]]+string[i+1:]
        return string
    def transpose(string, i):
        j = (i + random.choice([-1,1])) % len(string)
        l = [c for c in string]
        l[i], l[j] = l[j], l[i]
        return "".join(l)
    def randomletter(string, i):
        string = string[0:i+1]+random.choice("abcdefghijklmnopqrstuvwxyz")+string[i+1:]
        return string
    def randomreplace(string, i):
        string = string[0:i]+random.choice("abcdefghijklmnopqrstuvwxyz")+string[i+1:]
        return string
    def soundalike(string, i):
        try:
            c = sounddict[string[i]]
        except:
            return string
        string = string[0:i]+c+string[i+1:]
        return string
    func = random.choice([mistype, transpose, randomletter, randomreplace,
                          soundalike])
    for i in letters:
        word = func(word, i)
    return word
