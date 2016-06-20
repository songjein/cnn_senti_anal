import re
#f = open ("yelp_labelled.txt", "r")
#f = open ("amazon_cells_labelled.txt", "r")
f = open ("imdb_labelled.txt", "r")

#pf = open ("yelp_pos.txt", "w")
#nf = open ("yelp_neg.txt", "w")

pf = open ("imdb_pos.txt", "w")
nf = open ("imdb_neg.txt", "w")

def pad_sentences(sentences, padding_word="<PAD/>"):
	for i in range(len(sentences)):
			sentence = sentences[i]
			padded_sentences.append(new_sentence)
	return padded_sentences


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


n_cnt = 0
p_cnt = 0
padding_word ="<PAD/>" 
while True:
	line = clean_str(f.readline())
	if not line: break
	if len(line.split()) > 55:
		print len(line.split())
		continue
	if line[-1] == "0":
		nf.write(line[:-1] + "\n")
		n_cnt += 1
	if line[-1] == "1":
		pf.write(line[:-1] + "\n")
		p_cnt += 1
	
print n_cnt, p_cnt



