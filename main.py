# -*- coding: utf-8 -*-
from processXML import Preprocess

with open ("./Data/1/1.1.text.xml","r") as data:      
      articles = Preprocess(data).Articles
      test = articles[0]
      

