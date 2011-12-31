from process_page import process_url, PageProcessingException
from corpa import Corpa
from urlparse import urlparse, urljoin
import logging
import urllib


def process_domain(domain, n_gram_builder=Corpa(order=3), desired_n_grams=10000):
    page_stack = ['']
    neighbors = set()
    crawled_pages = set()
    while page_stack and n_gram_builder.total_n_grams < desired_n_grams:
        page = page_stack.pop()
        crawled_pages.add(page)
        url = urljoin('http://' + domain, page)
        try:
            page_text, page_urls = process_url(url)
            logging.info('Opened %s' % url)
        except PageProcessingException:
            continue
        domain_links, neighboring_domains = filter_links(page_urls, domain)
        
        new_pages = set(p for p in domain_links if p not in crawled_pages and p not in page_stack)
        page_stack.extend(new_pages)
        neighbors.update(neighboring_domains)
        n_gram_builder.consume_text(page_text)

    return n_gram_builder, neighbors

def sanitize_page_path(page_path):
    old_page_path = page_path
    page_path = urllib.quote(page_path, safe='/%')
    if page_path != old_page_path:
        logging.info('%s became %s' % (old_page_path, page_path))
    return page_path


def filter_links(urls, domain):
    domain_pages = set()
    neighboring_domains = []
    for url in urls:
        if '@' in url:
            logging.info('%s looks like an email, skipping' % url)
            continue
            
        o = urlparse(url)
        if not o.netloc or domain in o.netloc:
            page = sanitize_page_path(o.path)
            if len(page) > 100:
                logging.info('%s is very long, probably not a good url.' % page)
                continue 
            domain_pages.add(page)
        else:
            neighboring_domains.append(o.netloc)
        
    return domain_pages, neighboring_domains


import unittest
class ProcessDomainTester(unittest.TestCase):
    def test_process_domain(self):
        corpa = Corpa()
        n_grams, neighbors = process_domain('patriotgetaways.com', corpa)
        #print n_grams
        pass
    def test_filter_links(self):
        pass
if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    
    n_grams, neighbors = process_domain('patriotgetaways.com')
    pass
    #unittest.main()