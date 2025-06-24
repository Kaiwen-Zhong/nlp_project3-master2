# -*- coding: utf-8 -*-
"""
String Expansion 
Functions:
    combined stemmer
    get a list of synonyms 
Created on Fri Nov 11 22:17:30 2016

@author: kz54
"""

import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn

       
def c_stemmer(string):
    """ combined morphy and snowball stemmer based on pos of word
        @para: word string
        @return: stem of the string
    """
    sbst = SnowballStemmer("english")
    st = ''    
    p = nltk.pos_tag([string])[0][1] 
    if p in {'JJR', 'JJS', 'RBR', 'RBS'}:
        st = str(wn.morphy(string))
    elif p in {'JJ', 'NN', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ', 
               'NNPS', 'NNS', 'RB'}:
        st = str(sbst.stem(string))
        if st == string:
            st = str(wn.morphy(string))
    else:
        return string
    return st

def transform_pos(string):
    """ transform penn treebank tagger to wordnet tagger 
        using the below mapping rule
        @para: word string
        @return: wordbank tagger
        Mapping: 
        pos_dict = {'JJ': 'ADJ', 'JJR': 'ADJ', 'JJS': 'ADJ',
                    'RB': 'ADV', 'RBR': 'ADV', 'RBS': 'ADV', 
                    'NN': 'NOUN', 'NNS': 'NOUN', 
                    'VB': 'VERB', 'VBN': 'VERB', 'VBG': 'VERB', 
                    'VBD': 'VERB', 'VBP': 'VERB', 'VBZ': 'VERB', }
    """
    p = nltk.pos_tag([string])[0][1]    
    if p in {'NN', 'NNS'}:
        return wn.NOUN
    elif p.startswith('VB'):
        return wn.VERB
    elif p.startswith('JJ'):
        return wn.ADJ
    elif p.startswith('RB'):
        return wn.ADV

def get_syn(string):
    syn_list = [string]
    if nltk.pos_tag([string])[0][1] in {'JJ', 'JJR', 'JJS', 'RB', 
        'RBV', 'RBS', 'NN', 'NNS', 'VB', 'VBN', 'VBG', 'VBP', 'VBZ', 'VBD'}:
        for synset in wn.synsets(string, pos=transform_pos(string)):
            for lemma in synset.lemmas():
                if str(lemma.name()) not in syn_list:
                    syn_list.append(str(lemma.name()))
    syn_list_short = []
    for word in syn_list:
        if word.find('_')==-1:
            word = word.replace('-', " ")
            syn_list_short.append(word)
    return syn_list_short

def expand_word(string):
    expanded_list = [string]
    stem = c_stemmer(string)
    expanded_list.append(stem)
    syn_list = get_syn(string)
    for word in syn_list:
        if word not in expanded_list:
            expanded_list.append(word)
    return expanded_list

if __name__ =='__main__':
    # test expand_word
    wordList = ['located', 'invented', 'paper', 'clip', 
            'electric', 'leader', 'minister', 'killed',
            'won', 'teaching', 'tie', 'laces', 'buried', 
            'lobsters', 'born', 'wrote', 'aborigines', 
            "Ayer's", 'completed', 'found', 'religion', 
            'religious', 'founded', 'richest', 'established',
            'built', 'corpus', 'Boxing', 'eruption', 
            'president', 'character', 'novel', 'broke', 
            'service', 'shot', 'stole', 'founder', 'wedding',
            'produced', 'mined', 'bar-code', 'older', 
            'tallest', 'to']
    for word in wordList:
        print expand_word(word)
#    
## test get_syn
#    wordList = ['located', 'invented', 'paper', 'clip', 
#                'electric', 'leader', 'minister', 'killed',
#                'won', 'teaching', 'tie', 'laces', 'buried', 
#                'lobsters', 'born', 'wrote', 'aborigines', 
#                "Ayer's", 'completed', 'found', 'religion', 
#                'religious', 'founded', 'richest', 'established',
#                'built', 'corpus', 'Boxing', 'eruption', 
#                'president', 'character', 'novel', 'broke', 
#                'service', 'shot', 'stole', 'founder', 'wedding',
#                'produced', 'mined', 'bar-code', 'older', 
#                'tallest', 'to']
#    for word in wordList:
#        print get_syn(word)

#
### test c_stemmer
##    wordList = ['located', 'invented', 'paper', 'clip', 
##                'electric', 'leader', 'minister', 'killed',
##                'won', 'teaching', 'tie', 'laces', 'buried', 
##                'lobsters', 'born', 'wrote', 'aborigines', 
##                "Ayer's", 'completed', 'found', 'religion', 
##                'religious', 'founded', 'richest', 'established',
##                'built', 'corpus', 'Boxing', 'eruption', 
##                'president', 'character', 'novel', 'broke', 
##                'service', 'shot', 'stole', 'founder', 'wedding',
##                'produced', 'mined', 'bar-code', 'older', 
##                'tallest', 'to']
##                
##    for word in wordList:
##        print c_stemmer(word)