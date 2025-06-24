
import getopt, sys, os
import preprocessing
import sentenceCollecting
import np_tagger
from ne_extractor import NE_extractor

USAGE = "Usage: python %s [-q | --questions-path=] <path-to-questions> [-d | --documents-path=] <path-to-documents> [-a | --answers-path=] <path-to-answers>" % __file__

file_index = sys.argv.index(__file__)
opts, args = getopt.getopt(sys.argv[file_index + 1:], "q:d:a:", ["questions-path=", "documents-path=", "answers-path="])

# Obtain command-line arguments
questions_path = None
documents_path = None
answers_path = None
for opt, arg in opts:
	if opt in ('-q', '--questions-path'):
		questions_path = arg
	elif opt in ('-d', '--documents-path'):
		documents_path = arg
	elif opt in ('-a', '--answers-path'):
		answers_path = arg
	else:
		print USAGE
		sys.exit(2)

# Check if any of the required arguments are not given
if questions_path is None or documents_path is None or answers_path is None:
	print USAGE
	sys.exit(2)
else:
	print "Running baseline QA: answering questions in %s using the documents in %s." % (questions_path, documents_path)

# #########################################################################################
# ############################### PROCESSING STARTS HERE ##################################
# #########################################################################################

questions = preprocessing.pre_process(questions_path)
sentences = sentenceCollecting.sentence_collector(documents_path, questions)
ne_extractor = NE_extractor()

with open(answers_path, 'w') as answers_file:
	# Do the following for each question
	for question_id in questions:
		question_type, keywords = questions[question_id]

		answers_count = {}
		for document_id in sentences[question_id]:
			for sentence in sentences[question_id][document_id]:
				# for WHO and WHERE questions, we use ne_extractor to 
				# get potential NE's answers; we still use np_tagger
				# for WHEN questions ^.^
				if question_type.lower() ==  "who":
					np_tagged = tuple(ne_extractor.extractor(sentence, "PERSON"))
				elif question_type.lower() ==  "where":
					np_tagged = tuple(ne_extractor.extractor(sentence, "LOCATION"))
				else:
					# Answer is a tuple of document id, word tuple
					np_tagged = tuple(np_tagger.tag(sentence, question_type.upper()))

				# Ignore empty answers
				if len(np_tagged) == 0:
					continue

				# Strip answers off of punctuations
				np_tagged = tuple([x.strip(',.') for x in np_tagged])

				# Add the count of this answer
				answer = (document_id, np_tagged)
				if answer not in answers_count:
					answers_count[answer] = 0
				answers_count[answer] += 1


		# Sort the answers by their count
		answers_count_assoc_list = [(answer_tuple, count) for answer_tuple, count in answers_count.iteritems()]
		sorted_answers = sorted(answers_count_assoc_list, key=lambda x: x[1], reverse=True)

		# Get the top five answers according to count
		top_five_answers = []
		for i in range(min(len(sorted_answers), 5)):
			# Convert the word list into string (for printing to file)
			answer_string = ""
			for word in sorted_answers[i][0][1]:
				answer_string += word + " "
			answer_string = answer_string[:-1]

			# Append this answer to the top five
			top_five_answers.append("%s %s %s\n" % (question_id, sorted_answers[i][0][0], answer_string))

		# If we have less than five answers total, fill in dummy answers until we have five
		DUMMY_ANSWER = "%s nil \n" % question_id
		while len(top_five_answers) < 5:
			top_five_answers.append(DUMMY_ANSWER)

		# Write the answers out to file
		for top_answer in top_five_answers:
			answers_file.write(top_answer)
		answers_file.write("\n")
