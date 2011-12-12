def word_n_grams(string, order, max_word_len=40):
    '''Word level n grams from a string of words seperated by spaces.

    '''
    tokens = string.split(' ')
    tokens = [token for token in tokens if len(token) <= max_word_len]
    #Sentry values
    tokens = [None,] + tokens + [None,]
    for i in range(len(tokens) - (order - 1)):
        yield tuple(tokens[i:i + order])

        
import unittest
class TestNGramFunctions(unittest.TestCase):
    def test_word_n_grams(self):
        string = 'the dog smelled like a skunk averylongworddddddddddddddddddddddddddddddddddddddddddddddddddddd'
        expected_results = [(None, 'the', 'dog'),
                        ('the', 'dog', 'smelled'),
                        ('dog', 'smelled', 'like'),
                        ('smelled', 'like', 'a'),
                        ('like', 'a', 'skunk'),
                        ('a', 'skunk', None)]

        results = list(word_n_grams(string, 3))
                        
        self.assertListEqual(results, expected_results)

if __name__ == '__main__':
    unittest.main()
