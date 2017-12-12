# -*- coding: utf-8 -*-
import re
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import wordnet as wn
import nltk

class Abstract():
      def __init__(self,ID,title,text):
            self.title = title
            self.text = text
            self.ID = ID
            self.cleanText = self.clean_text()
            self.SplitText = self.split_text()
            self.entities = self.find_entities()
            self.relations = None
            
      def clean_text(self):
            cleaned = re.sub('(<.*?>|<\/.*?>)',' ',self.text)
            cleaned = re.sub('  ',' ',cleaned)
            return cleaned
      
      def find_entities(self):
            entities = []
            for ele in self.SplitText:
                  if isinstance(ele,Entity):
                        entities.append(ele)            
            return entities
      
      def split_text(self):
            byWord = []
            entityRegex = re.compile("(<.*?<\/entity>)")
            split = entityRegex.split(self.text)
            tokenizer = TreebankWordTokenizer()
            for ele in split:
                  if not re.match(entityRegex,ele):
                        words = tokenizer.tokenize(ele)
                        for i in words:
                              byWord.append(Word(i))
                  else:
                        ent = re.findall("<entity id=\"(.*?)\">(.*?)<\/entity>",ele)
                        for i in ent:
                              entity = Entity(i[0],i[1])
                              byWord.append(entity)
            
            self.set_surrounding(byWord,n=5)
            
            return byWord
      
      def set_surrounding(self,wordList,n=5):
             for ele in enumerate(wordList):
                   if isinstance(ele[1],Entity):
                         if ele[0] < n:
                               beforeIndex = 0
                         else:
                               beforeIndex = ele[0]-(n-1)                         
                         beforeList = []
                         while (beforeIndex != ele[0]):
                               beforeList.append(wordList[beforeIndex])
                               beforeIndex += 1
                         
                         if len(wordList) - ele[0] <n:
                               endIndex = len(wordList)-1
                         else:
                               endIndex = ele[0] + (n-1)
                         
                         afterList = []
                         start = ele[0]
                         while (start != endIndex):
                               afterList.append(wordList[start + 1])
                               start += 1
                               
                         ele[1].set_before(beforeList)
                         ele[1].set_after(afterList)             
             return None
      
      def set_relations(self,relationsData):
            
      
      def _detiled_print_(self):
            for ele in self.SplitText:
                  if isinstance(ele,Entity):
                        print("Entity ID: ",ele.ID," String: ",ele.entity)
                        print("Before: ",[x._to_string_() for x in ele.before])
                        print("After: ",[x._to_string_() for x in ele.after])
                        print("############################################\n")
                  elif isinstance(ele,Word):
                        print("Word: ",ele.word," POS tag: ",ele.posTag," WN representation: ",ele.WNRep)
                        print("############################################\n")
                  else:
                        print("ERROR! at: ",ele)
      


class Entity():
       def __init__(self,ID,entity):
             self.ID = ID
             self.entity = entity
             self.before = None
             self.after = None
             
       def set_before(self,beforeList):
             self.before = beforeList
             
       def set_after(self,afterList):
             self.after = afterList
             
       def _to_string_(self):
             return self.entity
       
		   
             
class Word():
      def __init__(self,word):
            self.word = word
            self.posTag = nltk.pos_tag([self.word])
            self.WNRep = wn.synsets(self.word)
            
      def _to_string_(self):
             return self.word

class Relation():
      def __init__(self,Type,entityOne,entityTwo,reverse=False):
            self.type = Type
            self.entityOne = entityOne
            self.entityTwo = entityTwo
            self.reverse = reverse
      
      
#
#p = re.compile("<entity id=\"(.*?)\">(.*?)<\/entity>")
#for m in p.finditer(a.text):
#    print (m.start(), m.group(2),m.end())