'''
Created on Nov 27, 2011

@author: andrewkittredge
'''

import math
from collections import Counter
import xml.etree.ElementTree as ET

THRESHOLD = 0.1

def decision_tree(data_set, attributes, parent_node):
    '''From Russel & Norvig pp 702
    
    '''
    if all(example['class'] == data_set[0]['class'] for example in data_set):
        ET.SubElement(parent_node, 'leaf_node' , {'class' : str(data_set[0]['class'])})
    elif not attributes:
        most_frequent_class = plurality_value(data_set)
        ET.SubElement(parent_node, 'leaf_node', {'class' : str(most_frequent_class)})
    else:
        data_set_entropy = data_set.entropy
        purities = dict((attribute, data_set.impurity_eval(attribute)) for attribute in attributes)
        impurity_reduction = lambda attribute : data_set_entropy - purities[attribute]
        best_attribute = max(attributes, key=impurity_reduction)
        if impurity_reduction(best_attribute) < THRESHOLD:
            ET.SubElement(parent_node, 'leaf_node', {'class' : str(plurality_value(data_set))})
        else:
            disjoint_subsets = data_set.subsets(best_attribute) 
            for subset in disjoint_subsets:
                decision_tree(subset, attributes - set([best_attribute]), parent_node)
                            
def plurality_value(records):
    class_counter = Counter(record['class'] for record in records)
    return class_counter.most_common(1)[0][0]
    
    
import unittest
class Tester(unittest.TestCase):
    def setUp(self):
        from data_set import build_test_records, DataSet
        self.data_set = DataSet(build_test_records())
    def test_decision_tree(self):
        data_set = self.data_set
        root_node = ET.Element('root')
        tree = decision_tree(data_set, data_set.attributes, root_node)
        print ET.tostring(root_node)