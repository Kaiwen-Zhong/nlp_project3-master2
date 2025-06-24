# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:02:54 2016
answerScoring
@author: kz54
"""

from operator import itemgetter
import get_answers


"""
Take in a dictionary like below, and return answer.txt file
qid {
    answer{
        score
        Rank
        Freq
    }
    answer{
        score
        Rank
        Freq
    }
}
"""

def score(q_dict):
    """
    calculate the score of each answers
    @para: dictionary of one question
    @return: a dictionary of the scores of each answers in the question
    """
    score_dict = {}
    for answer in q_dict:
        answer = answer.strip('.,!')
        if answer[len(answer)-2:len(answer)] == "'s":
            answer = answer[:len(answer)-2]
        if answer in score_dict:
            score_dict[answer] = score_dict[answer] + (q_dict[answer][0]*q_dict[answer][2])
        else:
            score_dict[answer] = (q_dict[answer][0]*q_dict[answer][2])

    return score_dict


def rank_top_answers(q_dict):
    """
    rank the top 5 or less answers
    @para: dictionary of one question
    @return: a list of the top 5 or less answers
    """
    score_dict = score(q_dict)
    s_score_dict = sorted(score_dict.items(), key=lambda x: x[1], reverse = True)
    if len(s_score_dict) < 5:
        return s_score_dict
    else:
        return s_score_dict[:5]


def get_answer_rank(q_dict):
    """
    get file rank that the answer comes from
    @para: dictionary of one question, a list of top answers
    @return: list of the answer ranks
    """
    top_answers = rank_top_answers(q_dict)
    list = []
    for item in top_answers:
        list.append(q_dict[item[0]][1])
    return list


def qa_scoring(all_q):
    """
    main function
    sort by question id, score and rank all questions
    @para: dictionary of all the questions
    @return: nested list of [qid, answer file rank, answer]
    """
    qa_answers = []
    for qid in all_q:
        if len(all_q[qid])==0:
            answer = [qid, 1, 'nil']
            qa_answers.append(answer)
        else:
            top_answers = rank_top_answers(all_q[qid])
            top_files = get_answer_rank(all_q[qid])
            if len(top_files)<5:
                top = len(top_files)
            else:
                top = 5
            for i in range(top):
                answer = [qid, top_files[i], top_answers[i]]
                qa_answers.append(answer)
    s_qa_answers = sorted(qa_answers, key=itemgetter(0))
    qa_answers = []
    for line in s_qa_answers:
        answer = "%s %s %s\n" % (line[0], line[1], line[2][0])
        qa_answers.append(answer)
    return qa_answers


if __name__ =='__main__':
    q_test = {'89':{'a': [60, 1, 3],
                'b': [50, 7, 2],
                'c': [40, 18, 1],
                'e': [30, 29, 4],
                'f': [20, 38, 2],
                'g': [10, 47, 4]},
            '90':
                {'h': [11, 2, 3],
                'i': [22, 3, 5],
                'j': [33, 4, 7]},
            '91':
                {}
            }

    d = get_answers.answer_dict()
    top_answers = qa_scoring(d)
#
#    with open('dictionary.txt', 'rb') as handle:
#        answer_dict = pickle.load(handle)
#    print (answer_dict)
#
#
#
#
#    file = open('dictionary.txt', 'r')
#
#    answer_dict = file.read()
#
#    top_answers = qa_scoring(answer_dict)
#
    file = open("answer.txt", "w")

    for top_answer in top_answers:
    	file.write(str(top_answer))
    file.write("\n")
    file.close()
