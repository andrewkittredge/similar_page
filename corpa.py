from MicrosoftNgram import LookupService
from collections import Counter
from n_gram import word_n_grams

 
class Corpa(object):
    def __init__(self, order=3):
        self.lookup_service = LookupService()
        self.n_grams = Counter()
        self.order = order

    def add_n_grams(self, n_grams):
        self.n_grams.update(n_grams)
    
    @property
    def total_n_grams(self):
        return sum(self.n_grams.values())

    def consume_text(self, text):
        self.add_n_grams(word_n_grams(text, self.order))
        
    
    def variance_from_model(self):
        total_phrases = float(self.total_n_grams)
        indexes = {}
        for phrase, occurences in self.n_grams.iteritems():
            p_corpa = occurences  / total_phrases
            if any(phrase):
                phrase_string = ' '.join(phrase)
                p_model = 10 ** self.lookup_service.GetJointProbability(phrase_string)
                indexes[phrase] = p_corpa / p_model
        return indexes
    
    def __str__(self):
        format_n_gram_count = lambda n_gram_count : '%s : %s' % (', '.join(map(str, n_gram_count[0])), n_gram_count[1])
        return '\n'.join(map(format_n_gram_count, self.n_grams.most_common(50)))
        
import unittest
class TestCorpa(unittest.TestCase):
    def test_total_n_grams(self):
        n_grams = {'a' : 3, 'b' : 4, 'c' : 5}
        corpa = Corpa()
        corpa.add_n_grams(n_grams)
        self.assertEquals(corpa.total_n_grams, 12)
        #indexes = corpa.variance_from_model()
        print corpa
        
    
if __name__ == '__main__':
    unittest.main()
