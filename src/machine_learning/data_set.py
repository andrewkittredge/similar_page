'''
Created on Nov 27, 2011

@author: andrewkittredge

from Liu pp64
'''
from collections import Counter, defaultdict
from itertools import groupby
from math import log


def information_gain(data_set, attribute):
    return data_set.entropy - data_set.partition(attribute).entropy

class DataSet(object):
    def __init__(self, records=[]):
        self.records = list(records)
        self.classes = Counter(record['class'] for record in records)
        
    @property
    def entropy(self):
        bits = 0.0
        for _class in self.classes.keys():
            class_probability = float(self.classes[_class]) / sum(self.classes.values()) 
            bits -= class_probability * log(class_probability, 2)
            
        return bits
    
    def impurity_eval(self, attribute):
        
        bits = 0.0
        total_records = len(self.records)
        record_groups = self.subsets(attribute)
        for attribute_records in record_groups:
            subset_entropy = DataSet(attribute_records).entropy
            bits += float(len(attribute_records)) / total_records * subset_entropy
        return bits
    
    def subsets(self, attribute):
        record_attribute_getter = lambda record : record[attribute]
        sorted_records = sorted(self.records, key=record_attribute_getter)
        record_groups = groupby(sorted_records, record_attribute_getter)
        return [DataSet(group) for _, group in record_groups]
    
    def attribute_value_subsets(self, attribute):
        groups = defaultdict(list)
        for record in self.records:
            groups[record[attribute]].append(record)
        for attribute_value, records in groups.iteritems():
            yield attribute_value, DataSet(records)
        
    
    @property
    def attributes(self):
        return set(self.records[0].keys()) - set(['class'])
    
    def __iter__(self):
        return iter(self.records)
    
    def __getitem__(self, key):
        return self.records[key]
    
    def __len__(self):
        return len(self.records)
        
import unittest
class DataSetTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_basic_entropy(self):
        records = [{'class' : True},
                   {'class' : True},
                   {'class' : False},
                   {'class' : False}]
        
        data_set = DataSet(records)
        self.assertEquals(data_set.entropy, 1.0)
        
        records.extend({'class' : False} for _ in range(6))
        data_set = DataSet(records)
        self.assertAlmostEqual(data_set.entropy, 0.722, 2)
        records = [{'class'  : True} for _ in range(10)]
        data_set = DataSet(records)
        self.assertEqual(data_set.entropy, 0)
        
    def test_infromation_gain(self):
        records = build_liu_test_records()
        data_set = DataSet(records)

        self.assertAlmostEqual(data_set.entropy, 0.971, 1)
        self.assertAlmostEqual(data_set.impurity_eval('age'), .888, 3)
        self.assertAlmostEqual(data_set.impurity_eval('own_house'), .551, 3)
        self.assertAlmostEqual(data_set.impurity_eval('has_job'), .647, 3)
        self.assertAlmostEqual(data_set.impurity_eval('credit_rating'), .608, 3)
    
    def test_data_set_class(self):
        data_set = DataSet(build_liu_test_records())
        self.assertSetEqual(data_set.attributes, set(('age',
                                                     'has_job',
                                                     'own_house',
                                                     'credit_rating')))    
    
    def test_norvig_data(self):
        data_set = DataSet(build_norvig_test_records())
        self.assertAlmostEqual(1.0 - data_set.impurity_eval('patrons'), .541, 3)
        self.assertAlmostEqual(1.0 - data_set.impurity_eval('type'), 0.0, 3)
        
def build_liu_test_records():
    #from Liu, pg 56    
        loan_application_attributes = ('age',
                                       'has_job',
                                       'own_house',
                                       'credit_rating',
                                       'class')
        
        record_lines = [
                   ('y', False, False, 'f', False),
                   ('y', False, False, 'g', False),
                   ('y', True,  False, 'g', True ),
                   ('y', True,  True,  'f', True ),
                   ('y', False, False, 'f', False),
                   ('m', False, False, 'f', False),
                   ('m', False, False, 'g', False),
                   ('m', True,  True,  'g', True ),
                   ('m', False, True,  'e', True ),
                   ('m', False, True,  'e', True ),
                   ('o', False, True,  'e', True ),
                   ('o', False, True,  'g', True ),
                   ('o', True,  False, 'g', True ),
                   ('o', True,  False, 'e', True ),
                   ('o', False, False, 'f', False)]
        
        records = []
        for record in record_lines:
            records.append(dict(zip(loan_application_attributes, record)))
        return records

def build_norvig_test_records():
    #from Norvig pg 700
    attributes = ('alt',
                  'bar',
                  'friday',
                  'hungry',
                  'patrons',
                  'price',
                  'rain',
                  'reservation',
                  'type',
                  'estimated_wait',
                  'class')
    record_lines = [
            (True,  False, False, True,  'some', '$$$', False, True,  'french',  10, True ),
            (True,  False, False, True,  'full', '$',   False, False, 'thai',    60, False),
            (False, True,  False, False, 'some', '$',   False, False, 'burger',  10, True ),
            (True,  False, True,  True,  'full', '$',   True,  False, 'thai',    30, True,),
            (True,  False, True,  False, 'full', '$$$', False, True,  'french',  61, False),
            (False, True,  False, True,  'some', '$$',  True,  True,  'italian', 10, True ),
            (False, True,  False, False, 'none', '$',   True,  False, 'burger',  10, False),
            (False, False, False, True,  'some',  '$$', True,  True,  'thai',    10, True ),
            (False, True,  True,  False, 'full', '$',   True,  False, 'burger',  61, False),
            (True,  True,  True,  True,  'full', '$$$', False, True,  'italian',30, False),
            (False, False, False, False, 'none', '$',   False, False, 'thai',    10, False),
            (True,  True,  True,  True,  'full', '$',   False, False, 'burger',  60, True)]
    records = []
    for record in record_lines:
        records.append(dict(zip(attributes, record)))
    return records
    
    
if __name__ == '__main__':
    unittest.main()