import re
import string

def slurp(f):
    with open(f, 'r') as input:
        contents = input.read()
        return contents


def cleanse(_string):
    '''Make the string more amiable to processing.

    '''
    #Remove repetitions of whitespace
    #'a'.translate(None, 'a')
    ret_string = _string.lower()
    allowed_chars = re.compile(u'[^a-z0-9_ ]')
    ret_string = allowed_chars.sub('', ret_string)
    #ret_string = _string.translate(None, string.punctuation)
    
    multiple_white_space = '\s{2,}'
    ret_string = re.sub(multiple_white_space, ' ', ret_string)
    #ret_string = ret_string.lower()

    return ret_string


def prep_e_tree_for_parsing(_node):
    node = _node.copy()
    serialize_attribs(node)
    for child_node in node.iter():
        serialize_attribs(child_node)
    return node
        
def serialize_attribs(node):
    for attrib, attrib_value in node.attrib.iteritems():
        node.attrib[attrib] = str(attrib_value)
    

import unittest
class PreprocessingTester(unittest.TestCase):
    def test_cleanse(self):
        test_string = u"""a   $  b$$$ 
                                c()d"""
        self.assertEqual('a b cd', cleanse(test_string))
    
    def test_prep_e_tree_for_processing(self):
        from xml.etree import ElementTree as ET
        root = ET.Element('root')
        ET.SubElement(root, 'tag_name', {'bool' : True, 'int' : 1, 'list' : [True, None, 1]})
        print_ready_node = prep_e_tree_for_parsing(root)
        print ET.tostring(print_ready_node)
        
        
if __name__ == '__main__':
    unittest.main()
