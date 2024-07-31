
#
#   Takes in a bunch of keywords, and will rank some sentence to how well it fits to the keywords
#

import spacy

class Ranker:
    
    def __init__(self):
        
        print('Loading SpaCy model')
        self.nlp = spacy.load('en_core_web_md')
        self.keywords = None
    
    def load_keywords(self, keywords):
        keywordString = " ".join(keywords);
        self.keywords = self.nlp(keywordString)

    def rank_sentence(self, sentence):

        # Compute similarity between the sentence and keywords
        sentence_doc = self.nlp(sentence)
        similarity = sentence_doc.similarity(self.keywords)
        
        return similarity
