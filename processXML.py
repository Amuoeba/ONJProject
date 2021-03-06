# -*- coding: utf-8 -*-
import re
from classes import Abstract

class Preprocess():
      """Preprocesses the raw data for further analisis. Accepts raw xml anotated data
      as a python io.TextIOWrapper"""
      
      def __init__(self,RawData):
            self.RawData = list(RawData)
            self.remove_new_lines()
            self.Segmented =None
            self.LinesByArticle = self.assign_lines_to_article()
            self.Articles = self.create_articles()
            
            
            
      
      def remove_new_lines(self):
            new = []
            for line in enumerate(self.RawData):                        
                  stripped=line[1].strip("\n")
                  if stripped != '':
                        new.append(stripped)
            self.RawData = new
#            self.Segmented = "".join(self.RawData)
#            segment = re.search('<text(.*?)>(.*?)<title>(.*?)<\/title>(.*?)<\/text>',self.Segmented)
#            self.Segmented = segment
            
      def assign_lines_to_article(self):
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
      
      def create_articles(self):
            """Create a list of Article classes"""
            Abstracts = []
            for article in self.LinesByArticle:
                  atributes = re.search('<text(.*?)>(.*?)<title>(.*?)<\/title>(.*?)<\/text>',article)
                  text = atributes.group(4)
                  text = re.sub('(<abstract>|<\/abstract>)','',text)
                  abstract = Abstract(atributes.group(1),atributes.group(3),text)
                  Abstracts.append(abstract)
            return Abstracts
            
                        
            
            
      