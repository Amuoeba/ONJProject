# -*- coding: utf-8 -*-
from random import randint

def SplitData(data,ratio=0.8):
      trainSize = round(len(data)*ratio)
      #testSize = len(data)-trainSize      
      
      train = []
      
      while(len(train) != trainSize):
            index = randint(0,len(data)-1)
            element = data.pop(index)
            train.append(element)
      
      test = data
      
      return {"train":train,"test":test}