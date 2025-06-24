# Michael Gingras
# NLP P3
# Answer Extraction


"""
Dictionary Structure
--------------------

qid{
    answer{
        freq
        docID
        score
    }
}

--------------------
"""

import preprocessing
import np_tagger
from string import punctuation
from ne_extractor import NE_extractor


def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def get_answers(qtype, chunk_list):
    a_list = []
    if qtype == 'When':
        for i in range(len(chunk_list)):
            a_list.append(np_tagger.tag(chunk_list[i],'WHEN'))
        return [item for sublist in a_list for item in sublist]
    elif qtype == 'Who':
        for i in range(len(chunk_list)):
            a_list.append(np_tagger.tag(chunk_list[i],'WHO'))
        return [item for sublist in a_list for item in sublist]
    else:
        for i in range(len(chunk_list)):
            a_list.append(np_tagger.tag(chunk_list[i],'WHERE'))
        return [item for sublist in a_list for item in sublist]

def get_freq(answer, answer_list):
    return answer_list.count(answer)

def parse_chunk(qid, chunks_dir):
    path = chunks_dir + '/'+str(qid)
    with open(path) as f:
        content = f.readlines()
    content = content[1:]
    return content


# d = {}
# d[295] = {}
# chunk_list = parse_chunk(295)
# answers = get_answers('WHERE',chunk_list)
# answer_list = []
# for answer in answers:
#     answer = answer.rstrip('\n')
#     if answer not in answer_list:
#         answer_list.append(answer)
# for chunk in chunk_list:
#     for answer in answer_list:
#         count = chunk.count(answer)
#         if count > 0:
#             split = chunk.split(" ")
#             d[295][answer] = [count,split[0],split[1]]
#
# print d

def answer_dict(chunks_dir):
    questions = preprocessing.pre_process('question.txt')
    d = {}
    for qid, val in questions.items():
        d[qid] = {}
        chunk_list = parse_chunk(qid, chunks_dir)
        answers = get_answers(val[0],chunk_list)
        answer_list = []
        for answer in answers:
            answer = answer.rstrip('\n')
            answer = strip_punctuation(answer)
            if answer not in answer_list:
                answer_list.append(answer)
        for chunk in chunk_list:
            for answer in answer_list:
                count = chunk.count(answer)
                if count > 0:
                    split = chunk.split(" ")
                    d[qid][answer] = [count,split[0],split[1]]

    return d
