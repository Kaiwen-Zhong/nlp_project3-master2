# CS 4740 - NLP
# Project 3 - QA
# October 29th 2016

import re

"""
returns a list of NP from a given string input and sentance type.
type WHO: looks for capitalized words
type WHERE: looks for capitalized words
type WHEN: looks for sequences of numbers or month names.

"""

date_cues = ["January", "February", "March", "April", "May", "June", "July",
"August","September","October","November","December", "Century", "Decade", "Sunday",
 "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

function_words = ["the", "there", "an", "a", "have", "had", "is", "are", "were", \
                    "was", "does", "do", "did", "should", "would", "could", "can"\
                    "shall", "will"]

suffix = ["ed", "ly", "ing"]

def is_dumbword(word):
    if word.lower() in function_words:
        return True
    elif word.endswith(tuple(suffix)):
        return True
    else:
        return False


def tag(line, type_of):
    np_list = []
    words = line.split(" ")

    if type_of == "WHO" or type_of == "WHERE":
        for i in range(1, len(words)):
            if words[i][0].isupper() and not is_dumbword(words[i]):
                np_list.append(words[i])
    else:
        for word in words:
            if word in date_cues:
                np_list.append(word)
            match = re.match('^[1-9]+.*',word)
            if match:
                np_list.append(match.group())

    return np_list

# some small scale tests

# print tag("Michael is brothers with Andrew and Matthew.", "WHO")
# print tag("Michael's birthday is January 19th 1996.", "WHEN")
# print tag("Listening to the music, Leo is coding.", "WHO")
# print tag("Excited about the upcoming event, Leo couldn't feel asleep.", "WHO")
# print tag("There should be a concert in Ithaca", "WHERE")
# print tag("Will they go to NYC this winter?", "WHERE")
