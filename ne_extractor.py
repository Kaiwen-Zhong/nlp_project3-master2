from nltk.tokenize import TweetTokenizer
import nltk


class NE_extractor:

    def extractor(self, sent, type):
        tokens = nltk.tokenize.word_tokenize(sent.decode('utf8', errors='replace'))
        pos_tagged = nltk.pos_tag(tokens)
        ne_tagged = nltk.ne_chunk(pos_tagged, binary=False)

        return_set = []

        if type == "PERSON":
            f = lambda t: t.label() == "PERSON"
        elif type == "LOCATION":
            f = lambda t: t.label() in ['LOCATION', 'ORGANIZATION', 'GPE', 'FACILITY']
        else:
            f = lambda t: t.label() in ['DATE', "TIME"]

        for subtree in ne_tagged.subtrees(filter = f):
            for leave in subtree.leaves():
                return_set.append(leave[0])

        return return_set

n = NE_extractor()
n.extractor("I want to go to NYC on 11-11-2016, and go to Paris at 11:13p.m.", "TIME")
