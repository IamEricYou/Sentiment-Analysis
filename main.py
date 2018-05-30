import sys
import collections, re

#Read words from txt file by words
#Ref: https://stackoverflow.com/questions/13259288/returning-a-list-of-words-after-reading-a-file-in-python

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

if __name__ == '__main__':
    print "Train the data"

    #texts = ['Hello how are you im fine and you']

    #bags = [collections.Counter(re.findall(r'\w+',txt)) for txt in texts]
    #print bags[0]

    training_data = read_words('trainingSet.txt')
    print training_data