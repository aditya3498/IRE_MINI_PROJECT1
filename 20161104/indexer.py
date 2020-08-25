import xml.sax, re, sys

from nltk.corpus import stopwords

import Stemmer

finaltext = {}
invertIndex = {}

def extractInfobox(text):

    data = re.sub(r'http[^\ ]*\ ', r' ',text)
    #data = re.sub(r'\<ref(.*)\<\/ref\>', r' ', text)
    data = text.split('\n')
    flag = 0
    finaldata = []
    starti = 0
    endi = 0
    info = []
    for i in range(len(data)):
        if re.match(r'\{\{infobox', data[i]):
            flag = 1
            starti = i
            info.append(re.sub(r'\{\{infobox(.*)', r'\1', data[i]))
        elif flag == 1:
            if data[i] == '}}':
                flag = 0
                endi = i
                continue
            info.append(data[i])

    return starti, endi, " ".join(info)

def extractCategories(text):
        
    data = re.sub(r'http[^\ ]*\ ', r' ', text)
    #data = re.sub(r'\<ref(.*)\<\/ref\>', r' ', text)
    data = text.split('\n')
    categories = []
    for line in data:
        if re.match(r'\[\[category', line):
            categories.append(re.sub(r'\[\[category:(.*)\]\]', r'\1', line))

    data = ' '.join(categories)
    return data

def extractBody(start, end, text):

    data = re.sub(r'http[^\ ]*\ ', r' ', text)
    #data = re.sub(r'\<ref(.*)\<\/ref\>', r' ', text)

    data = data.split('\n')

    body = []

    if end == 0:

        return data

    if start == 0:

        body = data[end+1:]

    else:
        
        body = data[0:start-1]
        
        body.extend(data[end+1:])

    return body

def extractReferences(text):

        data = re.sub(r'http[^\ ]*\ ', r' ', text)
        data = text.split('\n')
        refs = []
        for line in data:
            if re.search(r'<ref', line):
                refs.append(re.sub(r'.*title[\ ]*=[\ ]*([^\|]*).*', r'\1', line))

        return ' '.join(refs) 

def extractExternalLinks(text):
        links = []
        data = text.split("==external links==")
        if len(data) != 1:
            #finaldata = []
            data = data[1]
            #print(data)
            #data = data.split('\n')
            data = re.sub(r'http[^\ ]*\ ', r' ', data)
            #data = re.sub(r'\<ref(.*)\<\/ref\>', r' ', data)
            data = data.split('\n')
            #links = []
            for line in data:
                if re.match(r'\*\s*\{\{(.*)\}\}', line):
                    links.append(re.sub(r'\*\s*\{\{(.*)\}\}', r'\1', line))
                if re.match(r'\*\s*\[(.*)\]', line):
                    links.append(re.sub(r'\*\s*\[(.*)\]', r'\1', line))

        return links

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

def invertedIndex(finaltext):

    for key in finaltext:

        title = finaltext[key]['Title']

        body = finaltext[key]['Body']

        externallinks = finaltext[key]['External_Links']

        categories = finaltext[key]['Categories']

        references = finaltext[key]['References']

        infobox = finaltext[key]['Infobox']

        for word in title:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['t'] += 1

        for word in body:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['b'] += 1

        for word in externallinks:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['e'] += 1

        for word in infobox:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['i'] += 1

        for word in categories:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['c'] += 1

        for word in references:

            if word not in invertIndex:

                invertIndex[word] = {}

            if key not in invertIndex[word]:

                invertIndex[word][key] = {'t' : 0, 'b' : 0, 'i' : 0, 'c' : 0, 'e' : 0, 'r' : 0}

            invertIndex[word][key]['r'] += 1

    return invertIndex

def writeIndex(indexInvert, file):

    f = open(file, 'w+')

    for key in indexInvert:

        word = key + ':'

        for index in indexInvert[key]:

            word += 'd' + str(index) + '-'

            if indexInvert[key][index]['t']:

                word += 't' + str(indexInvert[key][index]['t'])

            if indexInvert[key][index]['b']:

                word += 'b' + str(indexInvert[key][index]['b'])

            if indexInvert[key][index]['i']:

                word += 'i' + str(indexInvert[key][index]['i'])

            if indexInvert[key][index]['c']:

                word += 'c' + str(indexInvert[key][index]['c'])

            if indexInvert[key][index]['e']:

                word += 'e' + str(indexInvert[key][index]['e'])

            if indexInvert[key][index]['r']:

                word += 'r' + str(indexInvert[key][index]['r'])      

            #word += 'T' + str(indexInvert[key][index]['t'] + indexInvert[key][index]['b'] + indexInvert[key][index]['i'] + indexInvert[key][index]['c'] + indexInvert[key][index]['e'] + indexInvert[key][index]['r']) + '|'
            
            word += '|'

        f.write(word + '\n')

    f.close()

    return

def appendTitles(final, file):

    f = open(file, 'a')

    f.write("--Titles--" + '\n')

    for key in final:

        f.write(str(key) + ':' + final[key]['TitlewithoutToken'] + '\n')

    f.close()

    return

#writeIndex(invertedIndex(), 'Index.txt')
#appendTitles(finaltext, 'Index.txt')

class WikipediaHandler( xml.sax.ContentHandler ):
    #finaltext = {}

    def __init__(self):
        self.CurrentData = ""
        self.page = ""
        self.page_no = 0
        self.title = ""
        self.id = ""
        self.text = ""
        self.id_no = 0
        self.start = 0
        self.end = 0
        self.data = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if self.CurrentData == "page":
            self.page_no += 1

    def endElement(self, tag):
        if tag == "page":
            #print(self.text.split('==References==')[0])
            self.start, self.end, self.data = extractInfobox(self.text.split("==References==")[0].lower())
            #print(self.text)
            finaltext[self.page_no] = {"Title" : tokenandcasefold(self.title.lower()), "TitlewithoutToken" : self.title.strip(), "Id" : self.id, 
            "Infobox" : tokenandcasefold(self.data), "Categories" : tokenandcasefold(extractCategories(self.text.lower())), 
            "Body" : tokenandcasefold(' '.join(extractBody(self.start, self.end, self.text.split("==References==")[0].lower()))), 
            "References" : tokenandcasefold(extractReferences(self.text.split("==External Links==")[0].lower())), 
            "External_Links" : tokenandcasefold(" ".join(extractExternalLinks(self.text.lower())))}
            self.CurrentData = ""
            self.text = ""
            self.title = ""
            self.id = ""
            self.id_no = 0

    def characters(self, content):
        if self.CurrentData == "page":
            self.page = content
        elif self.CurrentData == "title":
            self.title += content
        elif self.CurrentData == "text":
            #self.text = re.sub(r'\s+', '', self.text)
            self.text += content
            #self.updatedtext = re.sub(r'^\s+$', '', self.text)
            #self.updatedtext = re.sub(r'\', '', self.text)
        elif self.CurrentData == "id" and self.id_no == 0:
            self.id = content
            self.id_no = 1
  
if ( __name__ == "__main__"):
   
   parser = xml.sax.make_parser()
   
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   Handler = WikipediaHandler()
   
   parser.setContentHandler( Handler )
   
   parser.parse(str(sys.argv[1])) 

   invertIndex = invertedIndex(finaltext)

   writeIndex(invertIndex, str(sys.argv[2]) + '/index.txt') 

   appendTitles(finaltext, str(sys.argv[2]) + '/index.txt')
