# -*- coding: utf-8 -*-
import random
from random import randint
import classes as cs
import nltk
from nltk.stem import WordNetLemmatizer as Lematizer
from nltk.corpus import wordnet

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
        return list1+list2
    
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
            