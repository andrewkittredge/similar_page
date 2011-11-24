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
    ret_string = string.translate(_string,
                                    table=None,
                                    deletions=string.punctuation)
    
    multiple_white_space = '\s{2,}'
    ret_string = re.sub(multiple_white_space, ' ', ret_string)
    ret_string = ret_string.to_lower()

    return ret_string

import unittest
class PreprocessingTester(unittest.TestCase):
    def test_cleanse(self):
        test_string = """a   $  b$$$ 
                                c()d"""
        self.assertEqual('a b cd', cleanse(test_string))

if __name__ == '__main__':
    unittest.main()
