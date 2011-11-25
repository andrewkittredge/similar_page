import urllib2
from BeautifulSoup import BeautifulSoup
import re
from preprocessing_utilities import cleanse

def process_url(url):
    page = urllib2.urlopen(url)
    page_soup = BeautifulSoup(page.read())
    page_text = visible_text(page_soup)
    page_text = cleanse(page_text)
    urls = [anchor['href'].strip() for anchor in page_soup.findAll('a') if anchor.has_key('href')]
   
    return page_text, urls

def visible_text(soup):
    #from http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    texts = soup.findAll(text=True)
    text_fragments = filter(visible, texts)
    return ''.join(text_fragments)

def visible(element):
    unwanted_parents = ['style', 'script', '[document]', 'head', 'title']
    if element.parent.name in unwanted_parents:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


import unittest
class TestProcessPage(unittest.TestCase):
    def test_process_page(self):
        text, links = process_url('http://patriotgetaways.com')
        self.assert_(text)
        self.assert_(links)
        print text, links
        
if __name__ == '__main__':
    unittest.main()