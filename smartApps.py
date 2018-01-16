# -*- coding: utf-8 -*-

import retinasdk
import classes
import GeneralTools as gt
from sklearn.metrics import f1_score


LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")
FullClient = retinasdk.FullClient("d1fc2890-db36-11e7-9586-f796ac0731fb")

class RetinaRelationClassifier():
      def __init__(self,trainData,testData):
            self.trainData = trainData
            self.freqWords = gt.FindCommon(trainData).find_common_words()
            self.freqFilters = self.filtersFromFrequet(30)
            self.relTypeIndex ={classes.USAGE:0,classes.PART_WHOLE:1,classes.RESULT:2,classes.MODEL_FEATURE:3,classes.COMPARE:4,classes.TOPIC:5}
            
      def filtersFromFrequet(self,n):
          filters = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
          for relation in self.freqWords:
              examples = self.freqWords[relation][:n]
              examples = [x[0] for x in examples]
              print(examples)
              rel_filter = FullClient.createCategoryFilter(relation,examples)
              filters[relation] = rel_filter
          return filters
      
    
      def freqFilterTest(self):
            
            rel_true = []
            rel_pred = []
            
            for item in self.trainData:
                assert isinstance(item,classes.Abstract)
                for rel in item.relations:
                    assert isinstance(rel,classes.Relation)
                    rel_t = rel.type
                    rel_true.append(self.relTypeIndex[rel_t])
                    ent1 = rel.entityOne
                    ent2 = rel.entityTwo
                    ent1List = [x._to_string_() for x in ent1.before] + [ent1._to_string_()] + [x._to_string_() for x in ent1.after]
                    ent2List = [x._to_string_() for x in ent2.before] + [ent2._to_string_()] + [x._to_string_() for x in ent2.after]
                    sentence = " ".join(self._find_overlap_(ent1List,ent2List)[1])
                    max_score = 0
                    rel_predicted = None
                    for i in self.freqFilters:
                        rel_p = self.relTypeIndex[i]
                        score = LiteClient.compare(self.freqFilters[i].positions,sentence)
                        if score > max_score:
                            max_score = score
                            rel_predicted = rel_p
                    rel_pred.append(rel_predicted)
                    
            F1Score = f1_score(rel_true,rel_pred,average=None)
            F1macro = f1_score(rel_true,rel_pred,average="macro")
            F1micro = f1_score(rel_true,rel_pred,average="micro")
                            
            return (F1Score,F1macro,F1micro)
            
            
                    
                
#            
#
        
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
            return (False,list1+list2)
      
#      def create_filters(self):
#            positiveExamples = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
#            negativeExamples = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
#            
#            for abstract in self.trainData:
#                  assert isinstance(abstract,classes.Abstract)
#                  
#                  relations=abstract.relations
#                  
#                  for relation in relations:
#                        assert isinstance(relation,classes.Relation)
#                        entOne = relation.entityOne
#                        entTwo = relation.entityTwo
#                        relType = relation.type
#                        assert isinstance(entOne,classes.Entity)
#                        assert isinstance(entTwo,classes.Entity)
#                        
#                        relationText = entOne.before + [entOne] + entOne.after + entTwo.before + [entTwo] + entTwo.after
#                        relationText = " ".join([x._to_string_() for x in relationText])                     
#
#                        
#                        positiveExamples[relType].append(relationText)
#                        for rel in negativeExamples:
#                              if rel != relType:
#                                    negativeExamples[rel].append(relationText)
#                                    
#            filters = {classes.USAGE:[],classes.PART_WHOLE:[],classes.COMPARE:[],classes.RESULT:[],classes.TOPIC:[],classes.MODEL_FEATURE:[]}
#            
#            for rel in positiveExamples:
#                  pos = positiveExamples[rel]
#                  neg = negativeExamples[rel]
#                  fingerprintFilter = FullClient.createCategoryFilter(rel,pos,neg)
#                  filters[rel] = fingerprintFilter
#            
#            
#            return filters
      
      def test_filters(self,fingerprintFilters):
            performance = {}
            
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
                        
                        print(prediction[0])
                        
                        if relType not in performance:
                              performance[relType] = (0,0,0)
                              if prediction[0] == relType:
                                    performance[relType] = (performance[relType][0]+1,
                                               performance[relType][0],performance[relType][2]+1)
                              else:
                                    performance[relType] = (performance[relType][0],
                                               performance[relType][0]+1,performance[relType][2]+1)
                        else:
                              if prediction[0] == relType:
                                    performance[relType] = (performance[relType][0]+1,
                                               performance[relType][0],performance[relType][2]+1)
                              else:
                                    performance[relType] = (performance[relType][0],
                                               performance[relType][0]+1,performance[relType][2]+1)     
                              
            return performance
        

    
                        
      
      
      