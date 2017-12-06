# -*- coding: utf-8 -*-

class Preprocess():
      """Preprocesses the raw data for further analisis. Accepts raw xml anotated data
      as a python io.TextIOWrapper"""
      
      def __init__(self,RawData):
            self.RawData = list(RawData)
            self.RemoveNewLines()
      
      def RemoveNewLines(self):
            for line in enumerate(self.RawData):                        
                  stripped=line[1].strip("\n")
                  self.RawData[line[0]] = stripped
            
            new =[]
            for line in enumerate(self.RawData):
                  if line[1] != '':
                        new.append(line[1])
            self.RawData = new