import sys
import csv
import numpy as np

alphabet_list = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#Remove int from the list
#Ref: https://stackoverflow.com/questions/3159155/how-to-remove-all-integer-values-from-a-list-in-python
def remove_int(li):
    return [x for x in li if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

def get_data(data):
    bag_of_words = []
    bag_of_int = []

    for line in data:
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

def pre_processing(sentences, classification):
    vocab = []
    vocabLength = 0;
    featureInclude = []
    # creates sorted vocabulary
    for x in range(0,len(sentences)):
        for y in range(0,len(sentences[x])):
            if sentences[x][y] not in vocab:
                vocab.append(sentences[x][y])
    vocab = sorted(vocab)
    vocabLength = len(vocab)
    vocab.append("class Label")

    if vocab[0] == "": del vocab[0]
    
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
    
    return vocab, featureInclude

def make_txt(sentence, vocab, feature, filetype):
    if filetype == "train":
        with open("preprocessed_train.txt", "w") as csvfile:
            w = csv.writer(csvfile, delimiter=",")
            w.writerow(vocab)
            for item in feature:
                w.writerow(item)
        csvfile.closed
    else:
        with open("preprocessed_test.txt", "w") as csvfile:
            w = csv.writer(csvfile, delimiter=",")
            w.writerow(vocab)
            for item in feature:
                w.writerow(item)
        csvfile.closed

def main():
    #Pre-processing step
    training_data = open('trainingSet.txt','r')
    testing_data = open('testSet.txt','r')

    sentences, classification = get_data(training_data)
    sentences_ts, classification_ts = get_data(testing_data)
    
    vocab, featureInclude = pre_processing(sentences, classification)
    vocab_ts, featureInclude_ts = pre_processing(sentences_ts, classification_ts)

    make_txt(sentences, vocab,featureInclude,"train")
    make_txt(sentences_ts, vocab_ts,featureInclude_ts,"test")

    vocabLength = len(vocab)

    # calculating P(CD)
    NumRecords = len(sentences)
    NumRecCDFalse = 0
    NumRecCDTrue = 0

    for c in range(0,len(sentences)):
        if featureInclude[c][-1] == 1:
            NumRecCDTrue+=1
        elif featureInclude[c][-1] == 0:
            NumRecCDFalse+=1

    Pcd= [math.log(Decimal(NumRecCDTrue)/Decimal(NumRecords)),math.log(Decimal(NumRecCDFalse)/Decimal(NumRecords))]

    #calculating vocab conditional probability
    VocabCondProb =[]

    for v in range(0,len(vocab)):
        temp = []
        NumRecXTrueCDTrue = 1
        NumRecXTrueCDFalse = 1
        NumRecXFalseCDTrue = 1
        NumRecXFalseCDFalse = 1

        # index v will be vocab index
        for c in range(0,len(sentences)):
            if featureInclude[c][-1] == 1 and featureInclude[c][v] == 1:
                NumRecXTrueCDTrue+=1
            elif featureInclude[c][-1] == 0 and featureInclude[c][v] == 1:
                NumRecXTrueCDFalse+=1
            elif featureInclude[c][-1] == 1 and featureInclude[c][v] == 0:
                NumRecXFalseCDTrue+=1
            elif featureInclude[c][-1] == 0 and featureInclude[c][v] == 0:
                NumRecXFalseCDFalse+=1

        temp = [math.log(Decimal(NumRecXTrueCDTrue)/Decimal(NumRecCDTrue+vocabLength)),
        math.log(Decimal(NumRecXTrueCDFalse)/Decimal(NumRecCDFalse+vocabLength)),
        math.log(Decimal(NumRecXFalseCDTrue)/Decimal(NumRecCDTrue+vocabLength)),
        math.log(Decimal(NumRecXFalseCDFalse)/Decimal(NumRecCDFalse+vocabLength))]
        VocabCondProb.append(temp)

    #calculations
    PClass1=Pcd[0]
    PClass0=Pcd[1]


    print vocabLength
    for m in range(0,100):
        if vocab[m] in sentences_ts[0]:
            PClass1 = PClass1 * VocabCondProb[m][0]
            PClass0 = PClass0 * VocabCondProb[m][1]
        else:
            PClass1 = PClass1 * VocabCondProb[m][2]
            PClass0 = PClass0 * VocabCondProb[m][3]

    print PClass0
    print PClass1

main()
