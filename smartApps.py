# -*- coding: utf-8 -*-

import retinasdk
import classes

LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")
FullClient = retinasdk.FullClient("d1fc2890-db36-11e7-9586-f796ac0731fb")

class RetinaRelationClassifier():
      def __init__(self,trainData,testData):
            self.trainData = trainData
            self.testData = testData
      
      def create_filters(self):
            positiveExamples = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
            negativeExamples = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
            
            for abstract in self.trainData:
                  assert isinstance(abstract,classes.Abstract)
                  
                  relations=abstract.relations
                  
                  for relation in relations:
                        assert isinstance(relation,classes.Relation)
                        entOne = relation.entityOne
                        entTwo = relation.entityTwo
                        relType = relation.type
                        assert isinstance(entOne,classes.Entity)
                        assert isinstance(entTwo,classes.Entity)
                        
                        relationText = entOne.before + [entOne] + entOne.after + entTwo.before + [entTwo] + entTwo.after
                        relationText = " ".join([x._to_string_() for x in relationText])
                        

                        
                        positiveExamples[relType].append(relationText)
                        for rel in negativeExamples:
                              if rel != relType:
                                    negativeExamples[rel].append(relationText)
                                    
            filters = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
            
            for rel in positiveExamples:
                  pos = positiveExamples[rel]
                  neg = negativeExamples[rel]
                  fingerprintFilter = FullClient.createCategoryFilter(rel,pos,neg)
                  filters[rel] = fingerprintFilter
            
            
            return filters
      
      def test_filters(self,fingerprintFilters):
            correct = 0
            false = 0
            total = 0
            
            for abstract in self.testData:
                   assert isinstance(abstract,classes.Abstract)
                   relations=abstract.relations
                  
                   for relation in relations:
                        assert isinstance(relation,classes.Relation)
                        entOne = relation.entityOne
                        entTwo = relation.entityTwo
                        relType = relation.type
                        assert isinstance(entOne,classes.Entity)
                        assert isinstance(entTwo,classes.Entity)
                        
                        relationText = entOne.before + [entOne] + entOne.after + entTwo.before + [entTwo] + entTwo.after
                        relationText = " ".join([x._to_string_() for x in relationText])
                        
                        predictions = []
                        
                        for fpFilter in fingerprintFilters:
                              score = LiteClient.compare(relationText,fingerprintFilters[fpFilter].positions)
                              predictions.append((fpFilter,score))
                        
                        prediction = max(predictions, key=lambda x:x[1])
                        
                        if prediction[0] == relType:
                              correct += 1
                              total += 1
                        else:
                              false += 1
                              total += 1
                              
            return (correct,false,total)
                        