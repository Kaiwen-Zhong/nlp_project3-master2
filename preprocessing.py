# CS 4740 - NLP
# Project 3 - QA
# October 29th 2016

import os
import queryExpansion
from nltk.corpus import stopwords
from string import punctuation

path = "question.txt"
stop = set(stopwords.words('english'))

"""
returns a string without punctuation.
source: stackoverflow.
"""
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


"""
returns a dictionary from a list of questions where keys
are question IDs (integers) and values are questions (word lists)
"""
def pre_process(file_name):

    with open(file_name) as f:
	    content = f.read()

	# d is a dictionary of ID: Question
    d = {}

    questions = content.split("<top>")
    for question in questions:
        lines = question.split("\n")
        for line in lines:
            # gets the question ID
            if "<num>" in line:
                line = line.split(" ")
                qID = line[2].rstrip()
            # gets the question text
            if "?" in line:
                q = line
                # searches for part of question that may be in quotations
                quote_string = ""
                tokens = q.rstrip('?').split()
                for j in range(len(tokens)):
                    if tokens[j][0] == '"':
                        for k in range(j,len(tokens)):
                            quote_string = quote_string + " " + tokens[k]
                            if tokens[k][-1] == '"':
                                break

                # d[int(qID)] = (tokens[0], [(strip_punctuation(word)) for word in tokens[1:] if word not in stop])
                d[int(qID)] = (tokens[0], [queryExpansion.expand_word(strip_punctuation(word)) for word in tokens[1:] if (word not in stop and len(word) > 3) ])

                #last list (in list of lists) is the string in quotes, if this
                # question was one that contained a quoted subset.
                if quote_string != "":
                    d[int(qID)][1].append([(strip_punctuation(quote_string)).lstrip(' ')])

    return d
