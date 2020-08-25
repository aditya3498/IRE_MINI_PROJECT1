from math import log

import re, sys

from nltk.corpus import stopwords

import Stemmer

def tokenandcasefold(text):

	remrandom = ['\'','\'\'','[', '%', '+', '$', '-', ']', '{', '}', '#', '*', '<', '>', '=', '|', '(', ')', ',', '.', ':', ';', '!', '?', '\\', '/']

	remrandomdict = dict.fromkeys(remrandom, True)

	stop_words = stopwords.words('english')

	stopwords_dict = dict.fromkeys(stop_words, True)

	tokens = re.findall(r"\w+(?:'\w+)?|[^\w\s]", text)

	stopwordsrem = [w for w in tokens if w not in stopwords_dict]

	remrandomfinal = [w for w in stopwordsrem if w not in remrandomdict]

	finaltokens = []

	stemmer = Stemmer.Stemmer('english')

	for token in remrandomfinal:

		finaltokens.append(stemmer.stemWord(token))

	return finaltokens

def processQuery(text):

	finaltoken = tokenandcasefold(text.lower())

	return finaltoken

def readFile(file):

	f = open(file, 'r')

	line = f.readline()

	index = {}

	titles = {}

	while re.search(r'--Titles--', line) is None:

		splitting = line.split(':')

		word = splitting[0]

		index[word] = {}

		start = splitting[1]

		values = start.split("|")[:-1]

		for value in values:

			indexing = int(re.search(r'd(.*?)\-', value).group(0)[1:-1])

			index[word][indexing] = {'t':0, 'b':0, 'i':0, 'e':0, 'r':0, 'c':0, 'T':0}

			if re.search(r't([0-9]+)', value):

				index[word][indexing]['t'] = int(re.search(r't([0-9])+', value).group(0)[1:])

			if re.search(r'b([0-9]+)', value):

				index[word][indexing]['b'] = int(re.search(r'b([0-9])+', value).group(0)[1:])

			if re.search(r'c([0-9]+)', value):

				index[word][indexing]['c'] = int(re.search(r'c([0-9])+', value).group(0)[1:])

			if re.search(r'e([0-9]+)', value):

				index[word][indexing]['e'] = int(re.search(r'e([0-9])+', value).group(0)[1:])

			if re.search(r'i([0-9]+)', value):

				index[word][indexing]['i'] = int(re.search(r'i([0-9])+', value).group(0)[1:])

			if re.search(r'r([0-9]+)', value):

				index[word][indexing]['r'] = int(re.search(r'r([0-9])+', value).group(0)[1:])

			index[word][indexing]['T'] = index[word][indexing]['t'] + index[word][indexing]['c'] + index[word][indexing]['e'] + index[word][indexing]['b'] + index[word][indexing]['i'] + index[word][indexing]['r']

		line = f.readline()

	line = f.readline()

	while line:

		test = re.compile('([0-9]+):').split(line)

		titles[int(test[1])] = test[2].strip()

		line = f.readline()

	f.close()

	return index, titles

def fieldQuery(text):

	field = {}

	if re.search(r'title:([^:]*)(?!\S)', text):

		field['Title'] = processQuery(re.search(r'title:([^:]*)(?!\S)', text).group(0).split(':')[1].strip())

	if re.search(r'body:([^:]*)(?!\S)', text):

		field['Body'] = processQuery(re.search(r'body:([^:]*)(?!\S)', text).group(0).split(':')[1].strip())

	if re.search(r'ref:([^:]*)(?!\S)', text):

		field['References'] = processQuery(re.search(r'ref:([^:]*)(?!\S)', text).group(0).split(':')[1].strip())

	if re.search(r'category:([^:]*)(?!\S)', text):

		field['Category'] = processQuery(re.search(r'category:([^:]*)(?!\S)', text).group(0).split(':')[1].strip())

	if re.search(r'infobox:([^:]*)(?!\S)', text):

		field['Infobox'] = processQuery(re.search(r'infobox:([^:]*)(?!\S)', text).group(0).split(':')[1].strip())

	return field

def rankDocuments(index, words, titles, output):

	f = open(output, 'a')

	query = fieldQuery(words)

	rankings = {}

	if len(query):

		for key in query:

			for word in query[key]:

				for document in index[word].keys():

					if key == 'Title':

						TF = index[word][document]['t']

					elif key == 'Body':	

						TF = index[word][document]['b']

					elif key == 'Infobox':	

						TF = index[word][document]['i']

					elif key == 'References':	

						TF = index[word][document]['r']

					elif key == 'Category':	

						TF = index[word][document]['c']

					if TF > 0:

						TF = 1 + log(TF)
				
					else:
					
						TF = 0
				
					if document not in rankings:
					
						rankings[document] = TF
				
					else:
					
						rankings[document] += TF
		
		rankings = list(reversed(sorted(rankings.items(), key=lambda x: x[1])))[:10]

		for rank in rankings:

			f.write(titles[rank[0]] + '\n')
		
		f.write('\n')
		
	else:

		finalwords = processQuery(words)

		rankings = {}
	
		for word in finalwords:
		
			for document in index[word].keys():

				TF = index[word][document]['T']

				if TF > 0:

					TF = 1 + log(TF)
				
				else:
					
					TF = 0
				
				if document not in rankings:
					
					rankings[document] = TF
				
				else:
					
					rankings[document] += TF
		
		rankings = list(reversed(sorted(rankings.items(), key=lambda x: x[1])))[:10]

		for rank in rankings:

			f.write(titles[rank[0]] + '\n')

		f.write('\n')

	f.close()

if(__name__ == "__main__"):

	indexFile = str(sys.argv[1] + '/index.txt')

	inputFile = str(sys.argv[2])

	outputFile = str(sys.argv[3])

	indexDict, titleDict = readFile(indexFile)

	queries = []

	with open(inputFile) as f:

		queries = f.readlines()

	queries = [query.strip() for query in queries]

	for query in queries:
        	rankDocuments(indexDict, query, titleDict, outputFile)

