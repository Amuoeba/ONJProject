# -*- coding: utf-8 -*-
from processXML import Preprocess

with open ("./Data/1/1.1.text.xml","r") as data:      
      articles = Preprocess(data).Articles
      test = articles[0]
      

#import retinasdk
#retinasdk.lite_client("d1fc2890-db36-11e7-9586-f796ac0731fb")
#LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")
#LiteClient.getSimilarTerms("usage")