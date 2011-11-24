from process_page import process_page
from corpa import Corpa
def process_domain(domain, n_gram_builder):
    page_stack = [domain]
    neighbors = set()
    crawled_pages = set()
    while page_stack:
        page = page_stack.pop()
        page_text, page_links = process_page(page)
        this_page_links, page_neighbors = filter_links(page_links, domain)
        new_pages = (p for p in this_page_links if p not in crawled_pages)
        page_stack.extend(new_pages)
        neighbors.update(page_neighbors)
        n_gram_builder.consume_text(page_text)

    return n_gram_builder.n_grams, neighbors

def filter_links(links, domain):
    return [], []

import unittest
class ProcessDomainTester(unittest.TestCase):
    def test_process_domain(self):
        corpa = Corpa()
        n_grams, neighbors = process_domain('http://patriotgetaways.com', corpa)
        #print n_grams
        pass
        
if __name__ == '__main__':
    unittest.main()