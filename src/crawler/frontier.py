'''
Created on Dec 30, 2011

@author: akittredge
'''

EDGE_OF_FRONTIER = 1000


class Frontier(object):
    def __init__(self):
        self.queue = {}
        self.explored = set()
        
    def put(self, domain, priority):
        if domain not in self.explored:
            self.queue[domain] = min(priority, self.queue.get(domain, EDGE_OF_FRONTIER))
        
    def pop(self):
        next_domain, distance = sorted(self.queue.items(), 
                             key=lambda domain_priority : domain_priority[1])[0]
        self.explored.add(next_domain)
        self.queue.pop(next_domain)
        return next_domain, distance
    
    def empty(self):
        return not self.queue
        
    
import unittest
class FrontierTester(unittest.TestCase):
    def test_frontier(self):
        f = Frontier()
        f.put('google.com', 1)
        f.put('msn.com', 2)
        f.put('yahoo.com', 3)
        self.assertEqual(f.pop(), ('google.com', 1))
        