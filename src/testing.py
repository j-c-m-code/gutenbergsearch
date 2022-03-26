import os
import spacy
nlp = spacy.load("en_core_web_lg")
from use_matcher import write_results
test = 'Test one. Test two. Test three. Test four. Test five. Test six.'
doc = nlp(test)
sentences = list(doc.sents)
matchlist = [1,3,5]
short_name = 'test'
# write_results(sentences, matchlist, short_name)