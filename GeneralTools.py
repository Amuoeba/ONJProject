# -*- coding: utf-8 -*-
import random
from random import randint
import classes as cs
import nltk
from nltk.stem import WordNetLemmatizer as Lematizer
from nltk.corpus import wordnet
import pandas
import torch
import numpy as np
import torchwordemb
from torch.autograd import Variable
import sklearn as sk
import lstmModel
from sklearn.metrics import f1_score
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def SplitData(data,ratio=0.8,seed=None):
      if seed:
          random.seed(seed)
      trainSize = round(len(data)*ratio)
      #testSize = len(data)-trainSize      
      
      train = []
      
      while(len(train) != trainSize):
            index = randint(0,len(data)-1)
            element = data.pop(index)
            train.append(element)
      
      test = data
      
      return {"train":train,"test":test}
  
def AbstractNicePrint(abstract):
    assert isinstance(abstract,cs.Abstract)
    print("CLEAN TEXT: \n",abstract.cleanText)
    for ent in abstract.entities:
        ent = abstract.entities[ent]
        assert isinstance(ent,cs.Entity)
        print("EntityID: ", ent.entity," ",ent.ID," Before: ",[x.word if isinstance(x,cs.Word) else x.entity for x in ent.before], " After: ", [x.word if isinstance(x,cs.Word) else x.entity for x in ent.after])
        
    return None


class FindCommon():
    def __init__(self,abstractList):
        self.abstracts = abstractList
    
    def find_common_words(self):
        lematizer = Lematizer()
        comonPerRelType = {}
        for abstract in self.abstracts:
            assert isinstance(abstract,cs.Abstract)
            for rel in abstract.relations:
                assert isinstance(rel,cs.Relation)
                relType = rel.type
                ent1 = rel.entityOne
                ent2 = rel.entityTwo
                assert isinstance(ent1,cs.Entity)
                assert isinstance(ent2,cs.Entity)
                ent1List = [x._to_string_() for x in ent1.before] + [ent1._to_string_()] + [x._to_string_() for x in ent1.after]
                ent2List = [x._to_string_() for x in ent2.before] + [ent2._to_string_()] + [x._to_string_() for x in ent2.after]
                combined = self._find_overlap_(ent1List,ent2List)[1]
                
                combined = [x.split() for x in combined]
                combined = [x for y in combined for x in y]
                combined = [x.lower() for x in combined]
                combined = [x for x in combined if x.isalpha()]
                posCombined = nltk.pos_tag(combined)
                lematized = [lematizer.lemmatize(x[0],self._convert_to_wn_tag(x[1])) for x in posCombined]
                
                if relType not in comonPerRelType:
                    comonPerRelType[relType] = {}
                
                for word in lematized:
                    if word not in comonPerRelType[relType]:
                        comonPerRelType[relType][word] = 1
                    else:
                        comonPerRelType[relType][word] = comonPerRelType[relType][word] + 1      
        
        for rel in comonPerRelType:
            comonPerRelType[rel] = list(comonPerRelType[rel].items())
            comonPerRelType[rel].sort(key=lambda x:x[1],reverse=True)          
        
        return comonPerRelType
    
    def  _find_overlap_(self,list1,list2):
        med1 = []
        med2 = []
        overlap = None
        for i in range(max(len(list1),len(list2))):
            med1 = list1[-i:len(list1)]
            med2 = list2[:i]            
            if med1 == med2:
                overlap = med1
                return(overlap,list1[:len(list1)-i]+list2)            
        return (False,list1+list2)
    
    def _convert_to_wn_tag(self,tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

def PrintFrequencies(freq,n):
    headers  = []
    data = []
    
    for i in freq:
        headers.append(i)
        data.append(freq[i][:n])
            
    dt = pandas.DataFrame(data,headers).T
    return dt



class PrepareLSTMdata():
    def __init__(self,abstracts):
        self.abstracts = abstracts
        self.relTypeIndex ={cs.USAGE:0,cs.PART_WHOLE:1,cs.RESULT:2,cs.MODEL_FEATURE:3,cs.COMPARE:4,cs.TOPIC:5}
        self.data = []
        self.weights = None
        
    
    def extractRelationData(self):
        relStr = []
        for abstract in self.abstracts:
            assert isinstance(abstract,cs.Abstract)
            for relation in abstract.relations:
                assert isinstance(relation,cs.Relation)
                entOne = relation.entityOne
                entTwo = relation.entityTwo
                Type = relation.type
                assert isinstance(entOne,cs.Entity)
                assert isinstance(entTwo,cs.Entity)
                entOne = entOne.expand()
                entTwo = entTwo.expand()                
                relWords = FindCommon._find_overlap_(self,entOne,entTwo)[1]               
                relStr.append((relWords,Type))
                
        vocab, vec = torchwordemb.load_glove_text("./glove/glove.6B.50d.txt")
        
        for rel in relStr:
            words = rel[0]
            relType = rel[1]
            wordTensors = []
            for word in words:
                if word in vocab:
                    wordTensors.append(vec[vocab[word]])
            seqEmbeding = Variable(torch.stack(wordTensors))
            encodedRelType = self.relTypeIndex[relType]
            dataInstance = (seqEmbeding,encodedRelType)
            self.data.append(dataInstance)        
        return None
    
    def set_weights(self):
        totalCount = 0
        w = {}
        for item in self.data:
            tag = item[1]
            if tag not in w:
                w[tag] = 1
                totalCount += 1
            else:
                w[tag] = w[tag] +1
                totalCount += 1        
        for i in w:
            w[i] = totalCount/w[i]        
        l =[]
        for i in range(len(w)):
            l.append(w[i])            
        l = np.array(l,dtype="float32")
        w=torch.from_numpy(l)        
        self.weights = w
                
    
def dummytest(data,model):
    assert isinstance(model,lstmModel.LSTMTagger)
    assert isinstance(data,PrepareLSTMdata)
    h = model.init_hidden()
    truecount = 0
    falsecount = 0
    for item in data.data:
        sent = item[0]
        tag = item[1]
        model_out,_ = model(sent,h)
        prediction = np.argmax(model_out.data.numpy(),axis=1)[0]
        if prediction == tag:
#            print("True",tag)
            truecount += 1
        else:
#            print("False",tag)
            falsecount += 1
    return truecount,falsecount

def dummytest1(data,model):
    assert isinstance(model,lstmModel.LSTMTagger)
    assert isinstance(data,PrepareLSTMdata)
    h = model.init_hidden()
    truecount = 0
    falsecount = 0
    tagDict = {0:(0,0),1:(0,0),2:(0,0),3:(0,0),4:(0,0),5:(0,0)}
    F1Dict = {0:{"true":0,"alTrue":0,"all":0},1:{"true":0,"alTrue":0,"all":0},2:{"true":0,"alTrue":0,"all":0},
                3:{"true":0,"alTrue":0,"all":0},4:{"true":0,"alTrue":0,"all":0},5:{"true":0,"alTrue":0,"all":0}}
    
    rel_true = []
    rel_pred = []
    
    for item in data.data:
        sent = item[0]
        tag = item[1]
        rel_true.append(tag)
        model_out,_ = model(sent,h)
        prediction = np.argmax(model_out.data.numpy(),axis=1)[0]
        rel_pred.append(prediction)
        F1Dict[prediction]["alTrue"] = F1Dict[prediction]["alTrue"] +  1 
        if prediction == tag:
#            print("True",tag)
            truecount += 1
            tagDict[tag] = (tagDict[tag][0]+1,tagDict[tag][1]+1)
            F1Dict[prediction]["true"] = F1Dict[prediction]["true"] + 1
            F1Dict[prediction]["all"] = F1Dict[prediction]["all"] + 1            
        else:
#            print("False",tag)
            falsecount += 1
            tagDict[tag] = (tagDict[tag][0],tagDict[tag][1]+1)
            F1Dict[tag]["all"] = F1Dict[tag]["all"] +1
    
    F1Score = f1_score(rel_true,rel_pred,average=None)
    F1macro = f1_score(rel_true,rel_pred,average="macro")
    F1micro = f1_score(rel_true,rel_pred,average="micro")
                    
    return (truecount,falsecount,tagDict,F1Dict,F1Score,F1macro,F1micro)

def countRelations(abstracts):    
    relTypes = {cs.USAGE:0,cs.COMPARE:0,cs.PART_WHOLE:0,cs.RESULT:0,cs.TOPIC:0,cs.MODEL_FEATURE:0}    
    for a in abstracts:
        assert isinstance(a,cs.Abstract)
        for rel in a.relations:
            t = rel.type
            relTypes[t] = relTypes[t] +1
    return relTypes

def plottResults(data,name):
    if name[0].lower() == "f":
        y_label = "F1 score"
    elif name[:2].lower() =="mi":
        y_label = "micro average"
    elif name[:2].lower() == "ma":
        y_label = "macro average"
    else:
        y_label = "Average loss"
    x  = list(range(len(data)))
    y = data    
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.plot(x,y)
    ax.grid(True)
    ax.set_xlabel('epoch')
    ax.set_ylabel(y_label)
    fig.savefig(name)