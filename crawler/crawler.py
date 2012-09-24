'''
Created on Dec 26, 2011

@author: akittredge
'''


from frontier import Frontier
from process_domain import process_domain

class Crawler(object):
    def __init__(self, scorer, domain_processor, seed_domains):
        self.scorer = scorer
        self.frontier = Frontier()
        self.domain_processor = domain_processor
        self.matching_domains = set()
        self.process_seed_domains(seed_domains)
        
    def run(self):
        frontier = self.frontier
        while not frontier.empty():
            domain, distance = frontier.pop()
            n_grams, neighbors = self.process_domain(domain)
            if self.scorer.matches(n_grams):
                self.matching_domains.add(domain)
                for neighbor in neighbors:
                    frontier.put(neighbor, 1)
            else:
                for neighbor in neighbors:
                    frontier.put(neighbor, distance + 1)
        
def process_seed_domains(self, seed_domains):
    neighboring_domains = []
    records = []
    for domain in seed_domains:
        domain_records, domain_neighbors = process_domain(domain)
        neighboring_domains.extend(domain_neighbors)
     
        records.append(domain_records)
    return records, set(neighboring_domains)

#def build_decision_tree_from_domains(domains):
    

import unittest
class CrawlerTester(unittest.TestCase):
    def test_set_up(self):
        domains = ['patriotgetaways.com', 'ivylettings.com']
        crawler = Crawler(scorer = lambda domain : True,
                          domain_processor=process_domain,
                          seed_domains=domains)
        crawler.process_seed_domains(())