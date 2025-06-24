import getopt, sys, os, time
import preprocessing
import sentenceCollecting

"""
# keywords
docID, matched keywords, chunk.

"""


USAGE = "Usage: python %s [-d | --destination=] [-q | --questions-path=] <path-to-questions> [-p | --documents-path=] <path-to-documents> [-c | --chunk-size=] <chunk-size> [-t | --percent-threshold] <%%threshold> [-o | --overwrite] [-s | --simple]" % __file__

file_index = sys.argv.index(__file__)
opts, args = getopt.getopt(sys.argv[file_index + 1:], "d:q:p:c:t:os", ["destination=", "questions-path=", "documents-path=", "chunk-size=", "percentage-threshold="])

# Obtain command-line arguments
destination = None
questions_path = None
documents_path = None
chunk_size = None
threshold = None
overwrite = False
simple = False
for opt, arg in opts:
	if opt in ('-d', '--destination'):
		destination = arg
	elif opt in ('-q', '--questions-path'):
		questions_path = arg
	elif opt in ('-p', '--documents-path'):
		documents_path = arg
	elif opt in ('-c', '--chunk-size'):
		try:
			chunk_size = int(arg)
			if chunk_size < 1:
				print "Invalid chunk size: must be positive."
				sys.exit(1)
		except:
			print "Invalid chunk size: must be an integer."
			sys.exit(1)
	elif opt in ('-t', '--percentage-threshold'):
		try:
			threshold = float(arg)
			if threshold < 0 or threshold > 1:
				print "Invalid threshold: must be between 0 and 1."
				sys.exit(1)
		except:
			print "Invalid threshold: must be a float."
			sys.exit(1)
	elif opt in ('-o', '--overwrite'):
		overwrite = True
	elif opt in ('-s', '--simple'):
		simple = True
	else:
		print USAGE
		sys.exit(2)

# Check if any of the required arguments are not given
if destination is None or questions_path is None or documents_path is None or chunk_size is None or threshold is None:
	print USAGE
	sys.exit(2)
else:
	print "Generating chunks: writing chunks to %s." % destination

created_dir = False
if not os.path.isdir(destination):
	os.mkdir(destination)
	created_dir = True

# #########################################################################################
# ############################### GENERATING STARTS HERE ##################################
# #########################################################################################

# Keep track of runtime
before = time.time()

TYPE_TO_NE = {"who" : "PERSON", "where" : "LOCATION", "when" : "TIME"}

def keywords_in_chunk(chunk, keyword_sets):
	num_keywords_in_chunk = 0
	for kset in keyword_sets:
		for token in chunk:
			if token in kset:
				num_keywords_in_chunk += 1
				break
	return num_keywords_in_chunk

if created_dir or (not created_dir and overwrite):
	# Get the preprocessed questions
	print "Preprocessing questions..."
	questions = preprocessing.pre_process(questions_path)

	for question_id in questions:
		print "Generating chunks for question %d, using the %s chunk method." % (question_id, "simple" if simple else "smart")
		question_type, keywords = questions[question_id]
		keyword_sets = []
		for syn_list in keywords:
			keyword_sets.append(set(syn_list))

		apos = question_type.find('\'')
		if apos > 0:
			question_type = question_type[:apos]
		ne_type = TYPE_TO_NE[question_type.lower()]

		# Get the chunks for this question's documents
		# Each chunk is a (word sequence, document id) tuple
		if simple:
			text_chunks, score_dict = sentenceCollecting.simple_get_chunks_for_question(documents_path + "/" + str(question_id), chunk_size)
		else:
			text_chunks, score_dict = sentenceCollecting.get_chunks_for_question(documents_path + "/" + str(question_id), ne_type, chunk_size)

		with open(destination + "/" + str(question_id), 'w') as outfile:
			outfile.write("%d\n" % len(keywords))
			for chunk, doc_id in text_chunks:
				num_keywords = keywords_in_chunk(chunk, keyword_sets)
				if len(keyword_sets) > 0 and float(num_keywords) / len(keyword_sets) >= threshold:
					outfile.write("%d %f %d %s\n" % (doc_id, score_dict[doc_id], num_keywords, ' '.join(chunk)))
else:
	print "Chunks already exist in %s. Use the overwrite option \"-o\" to overwrite them." % destination
	sys.exit(0)

after = time.time()
elapsed = after - before
print "\nChunk generation completed. Total runtime is %d minutes %d seconds." % (elapsed / 60, elapsed % 60)
