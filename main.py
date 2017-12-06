# -*- coding: utf-8 -*-
from processXML import Preprocess

with open ("./Data/1/1.1.text.xml","r") as data:
      
      raw = Preprocess(data)
      print(raw.RawData)
#      for i in raw.RawData:
#            print(i)
      

