#f = open ("yelp_labelled.txt", "r")
#f = open ("amazon_cells_labelled.txt", "r")
f = open ("imdb_labelled.txt", "r")

#pf = open ("yelp_pos.txt", "w")
#nf = open ("yelp_neg.txt", "w")

pf = open ("imdb_pos.txt", "w")
nf = open ("imdb_neg.txt", "w")

n_cnt = 0
p_cnt = 0
while True:
	line = f.readline()
	line = line.strip().lower()
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



