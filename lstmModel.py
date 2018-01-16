# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import GeneralTools as gt

torch.manual_seed(1)



EMBEDDING_DIM = 50
HIDDEN_DIM = 64
TAGSET_SIZE = 6


class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, tagset_size,num_layers):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(embedding_dim, hidden_dim,num_layers) 
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        return (autograd.Variable(torch.zeros(self.num_layers, 1, self.hidden_dim)),
                autograd.Variable(torch.zeros(self.num_layers, 1, self.hidden_dim)))

    def forward(self, sentence,hidden):
#        print(sentence)
        embeding = sentence
#        print("Embeding ",embeds)
#        print("Flatten embeding: ",embeds.view(len(sentence), 1, -1))
        lstm_out, hidden = self.lstm(
            embeding.view(len(sentence), 1, -1), self.hidden)
        
#        print("LSTm OUT: ",lstm_out)
#        print("LSTm OUT FLATTENED: ",lstm_out.view(len(sentence),-1))

        type_space = self.hidden2tag(lstm_out[-1])
#        print("Tag space: ",type_space)
        tag_scores = F.log_softmax(type_space)
        return tag_scores,hidden
  


