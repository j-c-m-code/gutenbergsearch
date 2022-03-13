"""
Practice for the Youtube channel
Python Tutorials for Digital Humanities
"""
# first system modules
import os

# then third-party modules
import spacy

os.chdir(r"C:\Users\james\OneDrive\Corpora\James novels corpus")
with open("./Wings_of_the_Dove.txt", "r", encoding="utf-8") as f:
    text = f.read()
nlp = spacy.load("en_core_web_lg")
# as of March 2022, there are four English models to choose from:
# small, medium, large, and "trf"

# the novel is too long for the default, so increase allocated memory
nlp.max_length = len(text) + 100

doc = nlp(text)
sentences = list(doc.sents)

for sent in sentences:
    print(sent)
    print()

# named entities were already recognized as part of the nlp(text) command

##unique_ent_text = []

# makes a list of unique named entities (strips metadata, keeps only text)
##for ent in doc.ents:
##    if ent.text not in unique_ent_text:
##        unique_ent_text.append(ent.text)
##
##chunks = (list(doc.noun_chunks))
##
##print(chunks)
##
##patterns = [[{"POS": "NOUN"}, {"POS": "VERB"}, {"POS": "ADV"}]]
##verb_phrases = textacy.extract.token_matches(doc, patterns=patterns)
##
##for verb_phrase in verb_phrases:
##    print(verb_phrase)
##
##html = displacy.render(doc, style="ent")
