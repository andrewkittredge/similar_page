'''
Created on Nov 27, 2011

@author: andrewkittredge
'''

import math
from collections import Counter
import xml.etree.ElementTree as ET

def decision_tree(data_set, attributes, parent_examples):
    '''From Russel & Norvig pp 702
    
    '''
    if all(example['class'] == data_set[0]['class'] for example in data_set):
        ET.SubElement(parent_examples, 'leaf_node' , {'class' : data_set[0]['class']})
    elif not attributes:
        most_frequent_class = plurality_value(data_set)
        ET.SubElement(parent_examples, 'leaf_node', {'class' : most_frequent_class})
    else:
        data_set_entropy = data_set.entropy
        purities = dict((attribute, data_set.impurity_eval(attribute)) for attribute in attributes)
        impurity_reduction = lambda attribute : data_set_entropy - purities[attribute]
        best_attribute = max(attributes, key=impurity_reduction)
        if impurity_reduction(best_attribute) < THRESHOLD:
            ET.SubElement(parent_examples, 'leaf_node', {'class' : plurality_value(data_set)})
        else:
            disjoint_subsets = data_set.subsets(best_attribute) 
            for subset in disjoint_subsets:
                decision_tree(subset, attributes - best_attribute, parent_examples)

            
            

            
def plurality_value(records):
    class_counter = Counter(record['class'] for record in records)
    return class_counter.most_common(1)[0]
    