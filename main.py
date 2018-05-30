import sys
import numpy as np
import collections, re

alphabet_list = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#Remove int from the list
#Ref: https://stackoverflow.com/questions/3159155/how-to-remove-all-integer-values-from-a-list-in-python
def remove_int(li):
    return [x for x in li if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

def get_data(data):
    bag_of_words = []
    bag_of_int = []

    for line in training_data:
        lines = line.split() # splie the line by whitespace
        read_line = [n for n in lines]
        bag_of_int.append(int(read_line[-1][0]))
        read_line = remove_int(read_line) #Remove int from the list
        temp_list = []
        for item in read_line:
            item = ''.join(filter(alphabet_list.__contains__, item)) #Only alphabet will be considered
            temp_list.append(item)
        temp_list = [x.lower() for x in temp_list] #Uppercase -> lowercase
        bag_of_words.append(temp_list)

    return bag_of_words, bag_of_int


if __name__ == '__main__':
    sentences = [["wow","loved","the","place"], ["not","tasty","and", "the", "texture", "was", "just", "nasty"]]
    classification = [1,0]

    vocab = []
    vocabLength = 0;
    featureInclude = []

    training_data = open('trainingSet.txt','r')

    sentences, classification = get_data(training_data)

    # creates sorted vocabulary
    for x in range(0,len(sentences)):
        for y in range(0,len(sentences[x])):
            if sentences[x][y] not in vocab:
                vocab.append(sentences[x][y])
    vocab = sorted(vocab)
    vocabLength = len(vocab)
    vocab.append("class Label")

    # feature count array
    for c in range(0,len(sentences)):
        temp = []
        for d in range(0,vocabLength):
            if vocab[d] in sentences[c]:
                temp.append(1)
            else:
                temp.append(0)
        temp.append(classification[c])
        featureInclude.append(temp)

    print vocab
    # for elem in featureInclude:
    #     print elem
