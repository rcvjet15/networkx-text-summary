import urllib.request
from bs4 import BeautifulSoup
import re

class TextProcess:
  
    def __init__(self, url = None, filename = None):
        self._url = url
        self._filename = filename
        self._text = None
        self._sentences = None
    
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        
    @property
    def filename(self):
        return self._filename
    
    # method that start text processing process
    def start_process(self):
        text = self.__get_text_from_html()
        sentences = self.__getSentences(text)
        return sentences
        
    def __get_text_from_html(self):
        html = urllib.request.urlopen(self._url).read()
        soup = BeautifulSoup(html, "lxml")
        
        # Remove all scripts and style elements
        for script in soup(["script", "text"]):
            script.extract() 
                
        # get text only from body
        body_text = soup.body.get_text()
        
#        # break into lines and remove leading or trailing space on each
        lines = (line.strip() for line in body_text.splitlines())
        
        # break multi-headlines into a line each
        chunks = list()
        for line in lines:
            for phrase in line.split("  "):
                chunks.append(phrase.strip())                
                
#        # remove blank lines
        return "\n".join(chunk for chunk in chunks if chunk)        
    
    def __getSentences(self, text):
        return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
        
    
        
        
    