# -*- coding: utf-8 -*-
import re

class Abstract():
      def __init__(self,ID,title,text):
            self.title = title
            self.text = text
            self.ID = ID
            self.cleanText = self.CleanText()
            
      def CleanText(self):
            cleaned = re.sub('(<.*?>|<\/.*?>)','',self.text)
            return cleaned

     