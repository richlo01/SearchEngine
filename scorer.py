from collections import defaultdict
import math
import ast
import os
import nltk
from nltk.stem.snowball import SnowballStemmer

def calcWordTFIDF(word:str, document:int, data:"{word:{docID:count}}") -> "{word:score}":
    """ tf - term frequency: the number of times the term occurs in a document
        df - document frequency: the number of documents that contains the term
        idf - log10(size of collection/df)
        tf-idf = (1+log(tf)) * log(N/df) 
        Assuming that this is given a list of common documents that a query asks for, 
        this function will take in a word and the specific docID and will calculate TFIDF 
        for that document and word"""
    tf = data[word][document]
    df = len(data[word])
    idf = math.log((48962/df),10)
    return ((1+math.log(tf,10)) * idf)

def calcAllWords(words:list(),document:int, data:"{indexLetter:{word:{docID:count}}}", output:dict()) -> "{ docID: {word1:score, word2:score} }":
    """ Void: takes in multiple words and calculates all tfidf for each and makes the changes
        in the input dictionary """
    result = {}
    normalize_val = 0
    for word in words:
        result[word] = calcWordTFIDF(word, document, data[word[0]])
        normalize_val += result[word]*result[word]
    for word in result:
        result[word] = result[word]/math.sqrt(normalize_val)
    output[document] = result
    return None
    
def computeCosSim(query:dict(),docs:dict()) -> "{docID: score}":
    """ given a query of {"term":TFIDF"} and docs of {docID: {"term":TFIDF}}
        we will create the cosine similarity for every docID and return 
        a dict {docID: score}
    """ 
    output = {}
    for docID in docs:
        score = 0
        for term in list(query.keys()):
            score += docs[docID][term]*query[term]
        output[docID] = score
    return output

def getSpecificDict(file:str, word: str) -> dict():
    """ will open the text file, will only return the dict belonging to the word"""
    mypath = os.path.dirname(os.path.abspath(__file__))
    mypath += "\\index\\index\\" + file             
    file = open(mypath, "r")
    for lines in file.readlines():
        values = lines.split(" ",1)
        if values[0] == word:
            return ast.literal_eval(values[1]) 

def calcQwordTFIDF(query:str, allData: "{indexLetter:{word:{docID:count}}}") -> dict():
    """ Given a query, the function will calculate the tfidf of all the words in the 
        query and return them in a dict {"term":tfidf}"""
    m = defaultdict(int)
    df_holder = dict()
    output = {}
    sw = set(nltk.corpus.stopwords.words('english'))
    stemmer = SnowballStemmer('english')
    normalize_val = 0
    for words in query.split():
        stemmed = stemmer.stem(words)
        stemmed.lower()
        if stemmed not in sw:
            m[stemmed] += 1
    for words in m:
        try:
            df_holder[words] = len(allData[words[0]][words])
        except KeyError:
            continue
    for words in m:
        tfidf = (1+math.log(m[words],10)) * math.log((48962/df_holder[words]),10)
        output[words] = tfidf
        normalize_val += tfidf*tfidf
    for word in output:
        output[word] = output[word]/math.sqrt(normalize_val)
    return output
