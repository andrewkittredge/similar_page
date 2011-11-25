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



import unittest
class PreprocessingTester(unittest.TestCase):
    def test_cleanse(self):
        test_string = u"""a   $  b$$$ 
                                c()d"""
        self.assertEqual('a b cd', cleanse(test_string))

if __name__ == '__main__':
    unittest.main()
