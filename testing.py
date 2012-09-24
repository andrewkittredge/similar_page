from preprocessing_utilities import slurp, cleanse
from n_gram import word_n_grams
from corpa import Corpa

def test():
    input = slurp('/Users/andrewkittredge/Source/ai/similar_page/corpora/friendly_rentals.txt')
    cleansed_input = cleanse(input)
    n_grams = word_n_grams(cleansed_input, 1)
    corpa = Corpa()
    corpa.add_n_grams(n_grams)
    corpa.variance_from_model()
    
if __name__ == '__main__':
    test()