'''
Created on Nov 27, 2011

@author: andrewkittredge
'''

import math
from collections import Counter
import xml.etree.ElementTree as ET

THRESHOLD = 0.0

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
            node = ET.SubElement(parent_node, 'decision_node', {'attribute' : best_attribute})
            
            disjoint_subsets = data_set.attribute_value_subsets(best_attribute)
            for attribute_value, subset in disjoint_subsets:
                ET.SubElement(node, 'branch_node', {'attribute_value' : str(attribute_value)})
                decision_tree(subset, attributes - set([best_attribute]), node)
                            
def plurality_value(records):
    class_counter = Counter(record['class'] for record in records)
    return class_counter.most_common(1)[0][0]
    
    
import unittest
from data_set import DataSet
class Tester(unittest.TestCase):
    def setUp(self):
        from data_set import build_liu_test_records
        self.data_set = DataSet(build_liu_test_records())
    
    
    def test_decision_tree(self):
        data_set = self.data_set
        root_node = ET.Element('root')
        decision_tree(data_set, data_set.attributes, root_node)
        with open('loan_decision_tree.xml', 'wb') as out:
            out.write(ET.tostring(root_node))
            
    def test_norvig_data(self):
        from data_set import build_norvig_test_records
        data_set = DataSet(build_norvig_test_records())
        root_node = ET.Element('root')
        decision_tree(data_set, data_set.attributes, root_node)
        with open('norvig_decision_tree.xml', 'wb') as out:
            out.write(ET.tostring(root_node))
        
        
        
    def test_dummy_tree(self):
        dummy_data = [{'age' : 'y', 'class' : True},
                      {'age' : 'o', 'class' : False}]
        dummy_data_set = DataSet(dummy_data)
        root_node = ET.Element('root')
        decision_tree(dummy_data_set, dummy_data_set.attributes, root_node)
        
        print ET.tostring(root_node)