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
            
      def clean_text(self):
            cleaned = re.sub('(<.*?>|<\/.*?>)',' ',self.text)
            cleaned = re.sub('  ',' ',cleaned)
            return cleaned
      
      def find_entities(self):
            entities = []
            ent = re.findall("<entity id=\"(.*?)\">(.*?)<\/entity>",self.text)
            
            for i in ent:
                  entity = Entity(i[0],i[1])
                  entities.append(entity)
            
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
            return byWord
      
      def _detiled_print_(self):
            for ele in self.SplitText:
                  if isinstance(ele,Entity):
                        print("Entity ID: ",ele.ID," String: ",ele.entity)
                  elif isinstance(ele,Word):
                        print("Word: ",ele.word," POS tag: ",ele.posTag," WN representation: ",ele.WNRep)
                  else:
                        print("ERROR! at: ",ele)
      


class Entity():
       def __init__(self,ID,entity):
             self.ID = ID
             self.entity = entity
             
class Word():
      def __init__(self,word):
            self.word = word
            self.posTag = nltk.pos_tag([self.word])
            self.WNRep = wn.synsets(self.word)

#
#p = re.compile("<entity id=\"(.*?)\">(.*?)<\/entity>")
#for m in p.finditer(a.text):
#    print (m.start(), m.group(2),m.end())