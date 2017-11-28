import urllib.request
from bs4 import BeautifulSoup
import re

class TextProcess:
        
    def __init__(self, url = None, filename = None, content_selector_dict = None):
        # url from where html will be fetched
        self._url = url
        # filename of file in which text will be stored
        self._filename = filename
        # html selector (id, class or data-...) which contains main content
        self._content_selector_dict = content_selector_dict
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
    def get_filtered_sentences(self):
        text = self.__get_text_from_html()
        sentences = self.__get_sentences(text)
        filtered_sentences = list(self.__get_filtered_sentence(sentence) for sentence in sentences if sentence)
        return filtered_sentences
        
    def __get_text_from_html(self):
        html = urllib.request.urlopen(self._url).read()
        soup = BeautifulSoup(html, "lxml")
        
        # Remove all scripts and style elements
        for script in soup(["script", "text"]):
            script.extract() 
        
        # Get title
        content_title = soup.find("h1").get_text()
        
        main_text = None
        
        if self._content_selector_dict:
            # get text from main div element that is marked by specfic selector (class or id)
            main_text = soup.find('div', self._content_selector_dict).get_text()
        else:
            # get text only from body if selector not provided
            main_text = soup.body.get_text()
        
#        # break into lines and remove leading or trailing space on each
        lines = (line.strip() for line in main_text.splitlines())
        
        # break multi-headlines into a line each
        chunks = list()
        for line in lines:
            for phrase in line.split("  "):
                chunks.append(phrase.strip())                
         
        # insert title at the beginning of text lines. Add '.' (dot) at the end to mark it as sentence
        chunks.insert(0, content_title.strip() + ".")
        
#        # remove blank lines
        return "\n".join(chunk for chunk in chunks if chunk)        
    
    def __get_sentences(self, text):
        # split by: (where word character is not before)(where big or small letter is not before)(where . or ? or ! is before)empty space character(where small letter is not after)
        return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s(?![a-z])", text)
        
    def __get_filtered_sentence(self, sentence): 
        # leaves only alphanumeric characters or space
        return "".join(c for c in sentence if c.isalnum() or c.isspace())
           
    
        
    