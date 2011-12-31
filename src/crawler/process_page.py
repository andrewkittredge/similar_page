import urllib2
from BeautifulSoup import BeautifulSoup
import re
from preprocessing_utilities import cleanse
from shove import Shove
import logging
import tempfile

pages_cache = Shove('file://%s' % tempfile.gettempdir())


def process_url(url):
    page = get_page_contents(url)
    page_soup = BeautifulSoup(page)
    page_text = visible_text(page_soup)
    page_text = cleanse(page_text)
    try:
        urls = [anchor['href'].strip() for anchor in page_soup.findAll('a') if anchor.has_key('href')]
    except Exception as e:
        print e
    return page_text, urls

page_failure_token = 'CouldNotOpenPage'
def get_page_contents(url):
    if url not in pages_cache:
        logging.info('Cache miss %s' % url)
        try:
            f = urllib2.urlopen(url)
            try:
                pages_cache[url] = f.read()
            except KeyError:
                logging.warning('KeyError on %s' % url)
                raise PageProcessingException()
                
        except urllib2.HTTPError:
            logging.warning('HTTPError opening %s' % url)
            try:
                pages_cache[url] = page_failure_token
            except KeyError:
                logging.warning('KeyError on %s' % url)
                raise PageProcessingException()
        except urllib2.URLError:
            logging.warning('URLError opening %s' % url)
            try:
                pages_cache[url] = page_failure_token
            except KeyError:
                logging.warning('KeyError on %s' % url)
                raise PageProcessingException()
    if pages_cache[url] == page_failure_token:
        raise PageProcessingException()
    return pages_cache[url]
    #return pages_cache.setdefault(url, urllib2.urlopen(url).read())

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

class PageProcessingException(Exception):
    pass

import unittest
class TestProcessPage(unittest.TestCase):
    def test_process_page(self):
        text, links = process_url('http://patriotgetaways.com')
        self.assert_(text)
        self.assert_(links)
        
    def test_exception_page(self):
        self.assertRaises(PageProcessingException, process_url, 'http://not a url.com')
        
    def test_key_error(self):
        process_url('http://patriotgetaways.com/pigeon-forge-luxury-cabins/')
if __name__ == '__main__':
    unittest.main()
