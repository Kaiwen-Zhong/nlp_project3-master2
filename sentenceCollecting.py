import os
from ne_extractor import NE_extractor

directory_path = "doc_dev/"

# Returned by Michael
# questions = {ID: question}

relevant_tags = {"<TEXT>" : "</TEXT>", "<LP>" : "</LP>", "<LEADPARA>" : "</LEADPARA>", "<P>" : "</P>"}

# Find the text content in the file
def text_finder(file_path):
	res = []
	score = None
	inside_tag = False
	curr_open_tag = None
	with open(file_path, "r") as f:
		for line in f:
			if score is None:
				score = float(line[line.index("SCORE:") + 6:])
				continue
			if not inside_tag:
				# Check if current line contains opening tag
				for open_tag in relevant_tags:
					if open_tag in line:
						curr_open_tag = open_tag
						break
				if curr_open_tag is None:
					continue
			if not inside_tag and curr_open_tag is not None:
				# If an opening tag is encountered
				i = line.index(curr_open_tag)
				res.append(line[i + len(curr_open_tag):])
				inside_tag = True
			elif relevant_tags[curr_open_tag] in line:
				# If a closing tag is encountered
				j = line.index(relevant_tags[curr_open_tag])
				res.append(line[:j])
				inside_tag = False
				curr_open_tag = None
			else:
				res.append(line)
	return (score, " ".join(res))

# Retrieve fixed-size chunks of tokens from text
def text_to_chunk(text, question_type, chunk_size, document_id):
	doc_id = int(document_id)
	nee = NE_extractor()
	named_entities = set(nee.extractor(text, question_type))
	chunks = []
	tokens = text.split()
	for i in range(len(tokens)):
		curr_token = tokens[i]
		if curr_token in named_entities:
			chunks.append((tuple(tokens[max(0, i - chunk_size):i + 1]), doc_id))
			chunks.append((tuple(tokens[max(0, i - chunk_size / 2):min(len(tokens), i + chunk_size / 2 + 1)]), doc_id))
			chunks.append((tuple(tokens[i:min(len(tokens), i + chunk_size)]), doc_id))
	return chunks

# Get the chunks from a particular directory (one question)
def get_chunks_for_question(question_document_path, question_type, chunk_size):
	chunks = []
	files = os.listdir(question_document_path)
	doc_id_to_score = {}
	for file in files:
		score, file_text = text_finder(question_document_path + "/" + file)
		chunks += text_to_chunk(file_text, question_type, chunk_size, file)
		doc_id_to_score[int(file)] = score
	return (chunks, doc_id_to_score)

# A dumb but WAY faster way of getting chunks
def simple_get_chunks_for_question(question_document_path, chunk_size):
	chunks = []
	files = os.listdir(question_document_path)
	doc_id_to_score = {}
	for file in files:
		score, file_text = text_finder(question_document_path + "/" + file)
		tokens = file_text.split()
		for i in range(len(tokens) / chunk_size):
			chunks.append((tuple(tokens[chunk_size*i:chunk_size*(i + 1)]), int(file)))
		doc_id_to_score[int(file)] = score
	return (chunks, doc_id_to_score)

# Retrieve sentences from the text
def text_to_sentences(text):
	sentences = []
	s = ""
	for word in text.split():
		if word[-1] not in [".", "!"]:
			s = s + word + " "
		else:
			s += word
			sentences.append(s)
			s = ""
	return sentences

# Find out relevant sentences to that specific question
# defined by keywords
def relevant_sentence(key_words, temp_sentences):
	return_set = []
	for sentence in temp_sentences:
		for word in key_words:
			if word in sentence:
				return_set.append(sentence)
				break
	return return_set

# Main Process
def sentence_collector(directory_path, keyword_dictionary):
	sentences = {}
	for question_index in range(89, 321):
		question_dir_path = directory_path + "/" + str(question_index)
		files = os.listdir(question_dir_path)
		sentences[question_index] = {}
		for file in files:
			# print question_index
			# print file
			file_path = question_dir_path + "/" + file
			# All sentences in the file
			temp_sentences = text_to_sentences(text_finder(file_path))
			# Find out relevant sentences
			possible_sentences = relevant_sentence(keyword_dictionary[question_index][1], temp_sentences)
			sentences[question_index][file] = possible_sentences

	return sentences

# file_path = directory_path + "92/77"
# print text_finder(file_path)
