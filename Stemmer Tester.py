# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:57:47 2016

stemmer tester

@author: kz54
"""
import nltk
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

pst = PorterStemmer()
sbst = SnowballStemmer("english")
lst = LancasterStemmer()
wnl = WordNetLemmatizer()

def stemmerTester(string):
    
    print (string)
    
    print nltk.pos_tag([string])[0][1]

    print 'porter, ', pst.stem(string)

    print 'snowball, ', sbst.stem(string)

    print 'lancaster, ', lst.stem(string)
    
    print 'morphy, ', wn.morphy(string)
    
    print 'lemmatizer, ', wnl.lemmatize(string) 
    
    print '---------------------------'


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
            'tallest']
            
for word in wordList:
    stemmerTester(word)
            
"""
Verdict: 
snowball is the best one; 
It is faster, not too gentle and not too aggressive
But certain words such as won, built, wrote, richest, 
cannot be dealt with by snowball
In this case, morphy is better.
Algo - if after snowball it is same as original, 
use morphy
"""

            
#210
            