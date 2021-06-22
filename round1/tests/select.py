import sys
from distance import levenshtein


def unrepeated(s, sentences):
    for sen in sentences:
        if levenshtein(sen.split(), s.split()) < 5:
            return False
    return True


counter = 0
max_len = round(int(sys.argv[2]) * 1.3)
min_len = round(int(sys.argv[2]) * 0.7)
sentences = []

for sentence in open(sys.argv[1]):
    s = sentence.split('\t')[1]
    if counter >= 2000:
        break
    elif (len(s.split()) <= max_len and len(s.split()) >= min_len
          and unrepeated(s, sentences)):
        print(sentence.strip())
        sentences.append(s)
        counter += 1
