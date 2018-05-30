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
    print "Train the data"

    #texts = ['Hello how are you im fine and you']
    #bags = [collections.Counter(re.findall(r'\w+',txt)) for txt in texts]
    #print bags[0]

    training_data = open('trainingSet.txt','r')
    
    bag_of_words, bag_of_int = get_data(training_data) 

    print bag_of_words[0] #Just for showing the list.
    print bag_of_int[0]