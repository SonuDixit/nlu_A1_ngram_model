import math
import nltk
from nltk.corpus import brown
import random

allSents=brown.sents()
totalNumSent = len(allSents)
allSentIndex=range(0,len(allSents))
trainSentIndex=random.sample(range(0,len(allSents)),int(0.85 * totalNumSent))
trainSent=[]
for i in range(0,len(trainSentIndex)):
    trainSent.append(allSents[trainSentIndex[i]])

#trainSent = allSents[trainSentIndex]
testSentIndex=[]
for i in range(0,len(allSentIndex)):
    if i not in trainSentIndex:
        testSentIndex.append(i)
testSent = []
for i in range(0,len(testSentIndex)):
    testSent.append(allSents[testSentIndex[i]])

#converting train and test to lower and removing punctuations
import string
punc = string.punctuation
#converting corpus to lowercase
trainSentLow = []
for i in range(0,len(trainSent)):
    empty=[]
    for j in range(0,len(trainSent[i])):
        if(trainSent[i][j] not in punc):
            empty.append(trainSent[i][j].lower())
    if(len(empty)>0):
        trainSentLow.append(empty)
testSentLow = []
for i in range(0,len(testSent)):
    empty=[]
    for j in range(0,len(testSent[i])):
        if(testSent[i][j] not in punc):
            empty.append(testSent[i][j].lower())
    if(len(empty)>0):
        testSentLow.append(empty)

#train Sents adding <unk> for out of vocab words:
totalWordTrain=0
for i in range(0,len(trainSentLow)):
    for j in range(0,len(trainSentLow[i])):
        totalWordTrain +=1
        
unkIndex=random.sample(range(0,totalWordTrain),int(0.10*totalWordTrain))
unkIndex.sort()
trainUn = []
x=0
indexUn=0
for i in range(0,len(trainSentLow)):
    empty=[]
    for j in range(0,len(trainSentLow[i])):
        if( indexUn<len(unkIndex)):
            if(x == unkIndex[indexUn] ):
                empty.append('<unk>')
                indexUn +=1
            else:
                empty.append(trainSentLow[i][j])
        else:
            empty.append(trainSentLow[i][j])
        
        x+=1
    trainUn.append(empty)

#creating all bigrams: 
biGramList=[]
for i in range(0,len(trainUn)):
    biGramList.append(['<s>',trainUn[i][0]])
    for j in range(1,len(trainUn[i])-1):
        biGramList.append([trainUn[i][j-1],trainUn[i][j]])
    biGramList.append([trainUn[i][len(trainUn[i])-1],'<e>'])
#biGramList=[]
#for i in range(0,len(trainSent)):
#    biGramList.append(['<s>',trainSent[i][0]])
#    for j in range(1,len(trainSent[i])-1):
#        biGramList.append([trainSent[i][j-1],trainSent[i][j]])
#    biGramList.append([trainSent[i][len(trainSent[i])-1],'<e>'])

from collections import Counter        
#Counter(biGramList)  #not working
for i in range(0,len(biGramList)):
    biGramList[i] = tuple(biGramList[i])
biCount = Counter(biGramList)
biCountDesc=biCount.most_common()

def uniGram(trainUn):
    uniGramList=[]
    for i in range(0,len(trainUn)):
        for j in range(0,len(trainUn[i])):
            uniGramList.append(trainUn[i][j])        
    
    uniCount = Counter(uniGramList)
    return uniCount,uniGramList

uniCount,uniGramList=uniGram(trainUn)

####calculating bigram perplexity of test

def perPlexityBi(uniCount,biCount,w0,w1):
    prob=0
    if (w0,w1) in biCount.keys():
        prob= biCount[(w0,w1)]/uniCount[w0]
    else:
        if (w0,'<unk>') in biCount.keys():
            prob= biCount[(w0,'<unk>')]/uniCount[w0]
        else:
            if(uniCount[w0]>0):
                prob= 1/uniCount[w0]
            else:
                prob=1/uniCount['<unk>']
    
    return math.log(1/prob)

perPlex=0
totWord=0
for i in range(0,len(testSentLow)):
    for j in range(0,len(testSentLow[i])-1):
        perPlex += perPlexityBi(uniCount,biCount,testSentLow[i][j],testSentLow[i][j+1])
        totWord += 1

print('perplexity of brownTest is:',math.exp(perPlex/totWord))

triGramList=[]
for i in range(0,len(trainUn)):
    if(len(trainUn[i])>2):
        triGramList.append(['<s>','<s>',trainUn[i][0]])
        triGramList.append(['<s>',trainUn[i][0],trainUn[i][1]])
        for j in range(2,len(trainUn[i])-2):
            triGramList.append([trainUn[i][j-2],trainUn[i][j-1],trainUn[i][j]])
        triGramList.append([trainUn[i][len(trainUn[i])-2],trainUn[i][len(trainUn[i])-1],'<e>'])
        triGramList.append([trainUn[i][len(trainUn[i])-1],'<e>','<e>'])

from collections import Counter        
#Counter(biGramList)  #not working
for i in range(0,len(triGramList)):
    triGramList[i] = tuple(triGramList[i])
triCount = Counter(triGramList)
triCountDesc=triCount.most_common()


def perPlexityTri(biCount,triCount,w0,w1,w2):
    prob=0
    if (w0,w1,w2) in triCount.keys():
        prob= triCount[(w0,w1,w2)]/biCount[w0,w1]
    else:
        if (w0,w1,'<unk>') in triCount.keys():
            prob= triCount[(w0,w1,'<unk>')]/biCount[w0,w1]
        else:
            if(biCount[w0,w1]>0):
                prob= 1/biCount[(w0,w1)]
            else:
                prob=1/biCount[('<unk>','<unk>')]
    
    return math.log(1/prob)

perPlexTri=0
totWordTri=0
for i in range(0,len(testSentLow)):
    for j in range(0,len(testSentLow[i])-2):
        perPlexTri += perPlexityTri(biCount,triCount,testSentLow[i][j],testSentLow[i][j+1],testSentLow[i][j+2])
        totWordTri += 1

print('perplexity of brownTest is:',math.exp(perPlexTri/totWordTri))
