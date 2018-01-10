# -*- coding: utf-8 -*-
from processXML import Preprocess
import classes as cs
import GeneralTools as gt
import re
import smartApps as sa
import retinasdk


with open ("./Data/1/1.1.text.xml","r") as text:      
      abstracts = Preprocess(text).Articles
      example = abstracts[0]
      
      
with open ("./Data/1/1.1.relations.txt") as relations:
      relations = list(relations)

#set up relations in abstracts   
for abst in abstracts:
      abst.set_relations(relations)

dataSplit=gt.SplitData(abstracts,seed=1)


train = dataSplit["train"]
test = dataSplit["test"]
      
      
#retinaClassifier=sa.RetinaRelationClassifier(train,test)
#filters = retinaClassifier.create_filters()
#
#performance = retinaClassifier.test_filters(filters)



LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")

