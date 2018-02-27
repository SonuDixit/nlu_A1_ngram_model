import math
import nltk
from nltk.corpus import gutenberg
import random
from nltk.corpus import brown


allSents_guten=gutenberg.sents()
totalNumSent_guten = len(allSents_guten)
import string
punc = string.punctuation

allSents=brown.sents()

import string
punc = string.punctuation


allSents= allSents + allSents_guten

totalNumSent = len(allSents)
trainSent = []
for i in range(0,totalNumSent):
    empty=[]
    for j in range(0,len(allSents[i])):
        if(allSents[i][j] not in punc):
            empty.append(allSents[i][j].lower())
    if(len(empty)>0):
        trainSent.append(empty)

biGramList=[]
for i in range(0,len(trainSent)):
    biGramList.append(['<s>',trainSent[i][0]])
    if(len(trainSent[i])>1):
        for j in range(1,len(trainSent[i])-1):
            biGramList.append([trainSent[i][j-1],trainSent[i][j]])
    biGramList.append([trainSent[i][len(trainSent[i])-1],'<e>'])

from collections import Counter        
#Counter(biGramList)  #not working
for i in range(0,len(biGramList)):
    biGramList[i] = tuple(biGramList[i])
biCount = Counter(biGramList)
biCountDesc=biCount.most_common()
#print('line 53')

def minimumFind(count):
    minV=count[0]
    minIndex=0
    for i in range(0,len(count)):
        if(count[i]<minV):
            minV=count[i]
            minIndex=i
    return minV,minIndex

def genWordVec(word,biCount):
    predict=['','','','','']
    count=[0,0,0,0,0]
    minV=0
    minIndex=0
    for k,v in biCount.items():
        if(word == k[0]):
            if(v>minV):
                count[minIndex]=v
                predict[minIndex]=k[1]
                minV,minIndex=minimumFind(count)
    
    x=[]
    for i in range(0,len(predict)):
        if not (predict[i]==''):
            x.append(predict[i])
#    print(x)
    
    if(len(x)==0):
#        print('not even unigram::do some changes')
        x.append('the')
    return x
            
#print('line 84')
def sentGenBigram(start,total,biCount):
    sent=start
    word=start
    for i in range(1,total):
        w1=genWordVec(word,biCount)
        index=random.sample(range(0,len(w1)),1)
        word=w1[index[0]]
        sent +=' '+ word 
    return sent


#biCount[('hi','jay')]
#print(sentGenBigram('hi',15,biCount))


triGramList=[]
for i in range(0,len(trainSent)):
    if(len(trainSent[i])>2):
        triGramList.append(['<s>','<s>',trainSent[i][0]])
        triGramList.append(['<s>',trainSent[i][0],trainSent[i][1]])
        for j in range(2,len(trainSent[i])-2):
            triGramList.append([trainSent[i][j-2],trainSent[i][j-1],trainSent[i][j]])
        triGramList.append([trainSent[i][len(trainSent[i])-2],trainSent[i][len(trainSent[i])-1],'<e>'])
        triGramList.append([trainSent[i][len(trainSent[i])-1],'<e>','<e>'])

from collections import Counter        
#Counter(biGramList)  #not working
for i in range(0,len(triGramList)):
    triGramList[i] = tuple(triGramList[i])
triCount = Counter(triGramList)
triCountDesc=triCount.most_common()


def genWord3gramVec(w1,w2,triCount,biCount):
    predict=['','','','','']
    count=[0,0,0,0,0]
    minV=0
    minIndex=0
    for k,v in triCount.items():
        if(k[0]==w1 and k[1]==w2):
            if(v>minV):
                count[minIndex]=v
                predict[minIndex]=k[2]
                minV,minIndex=minimumFind(count)
    
    x=[]
    for i in range(0,len(predict)):
        if not (predict[i]==''):
            x.append(predict[i])
#    print(x)
    if(len(x)==0):
#        x.append('the')
#        print('going to bigrams')
        x=genWordVec(w2,biCount)
    return x

#print('line 154')
def sentGenTrigram(w1,w2,total,triCount,biCount):
    sent=w1+' '+w2
    for i in range(1,total):
        w3=genWord3gramVec(w1,w2,triCount,biCount)
        index=random.sample(range(0,len(w3)),1)
        sent +=' '+ w3[index[0]]
        w1=w2
        w2=w3[index[0]]
    return sent


#print(sentGenTrigram('<s>','<s>',12,triCount,biCount))

#generate 4gram
##trigram
quadGramList=[]
for i in range(0,len(trainSent)):
    if(len(trainSent[i])>3):
        quadGramList.append(['<s>','<s>','<s>',trainSent[i][0]])
        quadGramList.append(['<s>','<s>',trainSent[i][0],trainSent[i][1]])
        quadGramList.append(['<s>',trainSent[i][0],trainSent[i][1],trainSent[i][2]])
        for j in range(3,len(trainSent[i])-3):
            quadGramList.append([trainSent[i][j-3],trainSent[i][j-2],trainSent[i][j-1],trainSent[i][j]])
        quadGramList.append([trainSent[i][len(trainSent[i])-3],trainSent[i][len(trainSent[i])-2],trainSent[i][len(trainSent[i])-1],'<e>'])
        quadGramList.append([trainSent[i][len(trainSent[i])-2],trainSent[i][len(trainSent[i])-1],'<e>','<e>'])
        quadGramList.append([trainSent[i][len(trainSent[i])-1],'<e>','<e>','<e>'])
from collections import Counter        
#Counter(biGramList)  #not working
for i in range(0,len(quadGramList)):
    quadGramList[i] = tuple(quadGramList[i])
quadCount = Counter(quadGramList)
quadCountDesc=quadCount.most_common()

#print('line 198')
def genWord4gramVec(w1,w2,w3,quadCount,triCount,biCount):
    predict=['','','','','']
    count=[0,0,0,0,0]
    minV=0
    minIndex=0
    for k,v in quadCount.items():
        if(k[0]==w1 and k[1]==w2 and k[2]==w3):
            if(v>minV):
                count[minIndex]=v
                predict[minIndex]=k[3]
                minV,minIndex=minimumFind(count)
    
    x=[]
    for i in range(0,len(predict)):
        if not (predict[i]==''):
            x.append(predict[i])
#    print(x)
    if(len(x)==0):
        #x.append('the')
#        print('going to trigrams')
        x=genWord3gramVec(w2,w3,triCount,biCount)
        if(len(x)==0):
            x=genWordVec(w3,biCount)
    return x
#print('line 222')
def sentGen4gram(w1,w2,w3,total,quadCount,triCount,biCount):
    sent=w1+' '+w2+' '+w3
    for i in range(1,total):
        w4=genWord4gramVec(w1,w2,w3,quadCount,triCount,biCount)
        index=random.sample(range(0,len(w4)),1)
        if(i>10):
            if('<e>' in w4):
                break
        
        if(w4[index[0]]=='<e>'):
            if(i>10):
#                print('end generated')
                break
            else:
                if(len(w4)>1):
                    newIndex=random.sample(range(0,len(w4)),1)
                    if(newIndex[0]==index[0]):
                        index=random.sample(range(0,len(w4)),1)
                    else:
                        index=newIndex
        #print('w4 is',w4)
        sent +=' '+ w4[index[0]]
        w1=w2
        w2=w3
        w3=w4[index[0]]
        
    return sent

#print('all words are:')
sentGen=sentGen4gram('<s>','<s>','<s>',25,quadCount,triCount,biCount)
#print(sentGen[12:])
words=nltk.word_tokenize(sentGen)
sentPrint=''
if(len(words)>21):
    for i in range(9,21):
        sentPrint += words[i]
        sentPrint += ' ' 
    
    print(sentPrint)
else:
    print(sentPrint)