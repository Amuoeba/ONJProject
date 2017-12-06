# -*- coding: utf-8 -*-
import re
from classes import Abstract

class Preprocess():
      """Preprocesses the raw data for further analisis. Accepts raw xml anotated data
      as a python io.TextIOWrapper"""
      
      def __init__(self,RawData):
            self.RawData = list(RawData)
            self.RemoveNewLines()
            self.Segmented =None
            self.LinesByArticle = self.AssignLinesToArticle()
            self.Articles = self.CreateArticles()
            
            
            
      
      def RemoveNewLines(self):
            new = []
            for line in enumerate(self.RawData):                        
                  stripped=line[1].strip("\n")
                  if stripped != '':
                        new.append(stripped)
            self.RawData = new
#            self.Segmented = "".join(self.RawData)
#            segment = re.search('<text(.*?)>(.*?)<title>(.*?)<\/title>(.*?)<\/text>',self.Segmented)
#            self.Segmented = segment
            
      def AssignLinesToArticle(self):
            """Parses the initial xml to assign text to seperate articles"""
            data = list(self.RawData)
            linesByArticle = []            
            while data:
                  head = data[0]
                  start = re.search('<text(.*?)>',head)
                  
                  if start:
                        head = data[0]
                        stop = re.search('<\/text(.*?)>',head)
                        article = []
                        while(not stop):
                              article.append(data.pop(0))
                              head = data[0]
                              stop = re.search('<\/text(.*?)>',head)
                        article.append(data.pop(0))
                        article="".join(article)
                        linesByArticle.append(article)
                  else:
                        data.pop(0)
            return linesByArticle
      
      def CreateArticles(self):
            Abstracts = []
            for article in self.LinesByArticle:
                  atributes = re.search('<text(.*?)>(.*?)<title>(.*?)<\/title>(.*?)<\/text>',article)
                  abstract = Abstract(atributes.group(1),atributes.group(3),atributes.group(4))
                  Abstracts.append(abstract)
            return Abstracts
            
                        
            
            
      