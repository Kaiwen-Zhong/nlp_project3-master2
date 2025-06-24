import preprocessing
import get_answers
import answerScoring
import getopt, sys, os

USAGE = "Usage: python %s [-c | --chunk-dir=] <chunks-directory> [-q | --questions-path=] <path-to-questions> [-a | --answer-path=] <path-to-answers>" % __file__

file_index = sys.argv.index(__file__)
opts, args = getopt.getopt(sys.argv[file_index + 1:], "c:q:a:", ["--chunk-dir=", "--questions-path=", "--answer-path="])

chunk_dir = None
questions_path = None
answer_path = None
for opt, arg in opts:
	if opt in ('-c', '--chunk-dir'):
		chunk_dir = arg
	elif opt in ('-q', '--questions-path'):
		questions_path = arg
	elif opt in ('-a', '--answer-path'):
		answer_path = arg
	else:
		print USAGE
		sys.exit(2)

# Check if any of the required arguments are not given
if chunk_dir is None or questions_path is None or answer_path is None:
	print USAGE
	sys.exit(2)
else:
	print "Running final QA, using chunks in %s." % chunk_dir

questions = preprocessing.pre_process(questions_path)

dict = get_answers.answer_dict(chunk_dir)
# print dict[92]

answers = answerScoring.qa_scoring(dict)

with open(answer_path, 'w') as outfile:
	for answer in answers:
		outfile.write(answer)
