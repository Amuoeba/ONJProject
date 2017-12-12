# -*- coding: utf-8 -*-
from processXML import Preprocess
import classes as cs

with open ("./Data/1/1.1.text.xml","r") as text:      
      abstracts = Preprocess(text).Articles
      test = abstracts[0]
      
      
with open ("./Data/1/1.1.relations.txt") as relations:
      print(list(relations))
      
      
#retinasdk.lite_client("d1fc2890-db36-11e7-9586-f796ac0731fb")
#LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")
#LiteClient.getSimilarTerms("usage")