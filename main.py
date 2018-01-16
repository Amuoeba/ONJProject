# -*- coding: utf-8 -*-
from processXML import Preprocess
import classes as cs
import GeneralTools as gt
import re
import smartApps as sa
import retinasdk
import torchwordemb
import lstmModel as lstm
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim




with open ("./Data/1/1.1.text.xml","r") as text:      
      abstracts = Preprocess(text).Articles
      example = abstracts[0]
      
      
with open ("./Data/1/1.1.relations.txt") as relations:
      relations = list(relations)

#set up relations in abstracts   
for abst in abstracts:
      abst.set_relations(relations)

dataSplit=gt.SplitData(abstracts,seed=4)


train = dataSplit["train"]
test = dataSplit["test"]
      
      
#retinaClassifier=sa.RetinaRelationClassifier(train,test)
#filters = retinaClassifier.create_filters()
#
#performance = retinaClassifier.test_filters(filters)
#LiteClient = retinasdk.LiteClient("d1fc2890-db36-11e7-9586-f796ac0731fb")

common=gt.FindCommon(train)
d = common.find_common_words()
gt.PrintFrequencies(d,30)




######### RUN LSTM MODEL ##################
trainData = gt.PrepareLSTMdata(train)
trainData.extractRelationData()
trainData.set_weights()

testData = gt.PrepareLSTMdata(test)
testData.extractRelationData()

model = lstm.LSTMTagger(lstm.EMBEDDING_DIM, lstm.HIDDEN_DIM, lstm.TAGSET_SIZE,1)
loss_function = nn.NLLLoss(weight=trainData.weights)#weight=trainData.weights

optimizer = optim.Adam(model.parameters(), lr=0.00001)
h = model.init_hidden()

inputs = trainData.data[0][0]
tag_scores,_ = model(inputs,h)
print(tag_scores)
print(gt.dummytest1(testData,model))

accF1Scores = []
accLoss = []
accMacro = []
accMicro = []
for epoch in range(10):  # again, normally you would NOT do 300 epochs, it is toy data
    avg_loss  = 0
    for sentence, target in trainData.data:
        model.zero_grad()        
        model.hidden = model.init_hidden()        
#        print(sentence_in)
        target = [target]
        target = torch.LongTensor(target)
        target = autograd.Variable(target)
        hidden = model.init_hidden()
        tag_scores,_ = model(sentence,hidden)
#        print("Targets ",target)
#        print("TagScores ",tag_scores)
        loss = loss_function(tag_scores, target)
        avg_loss += loss.data[0]
#        print("Epoch: ",epoch,"Loss: ",loss)
        loss.backward()
        optimizer.step()
        
    t = gt.dummytest1(testData,model)
    F1 = t[4]
    F1macro = t[5]
    F1micro = t[6]
    accF1Scores.append(F1)
    accLoss.append(avg_loss/len(trainData.data))
    accMacro.append(F1macro)
    accMacro.append(F1micro)
    print(F1,"Average loss: ",avg_loss / len(trainData.data))

# See what the scores are after training

tag_scores = model(inputs,h)

print(tag_scores)

####################### Runing the retina classification
print("Running retina classification")

retina_model = sa.RetinaRelationClassifier(train,test)
scores = retina_model.freqFilterTest()


#loading word2vec
#vocab, vec = torchwordemb.load_glove_text("./glove/glove.6B.100d.txt")
#vocabW2V, vecW2V = torchwordemb.load_word2vec_bin("./word2vec/GoogleNews-vectors-negative300.bin")

#print(vec.size())
#print(vec[vocab["apple"] ] )

#print(vec[ vocab["apple"] ] )
#print(vecW2V[ w2v.vocabW2V["apple"] ] )