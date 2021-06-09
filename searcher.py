import nltk
import ast
import scorer
import heapq
import time

def main():
    print("Preparing the index. Please Wait...")
    file = open("DOC_ID_dict.txt")
    docIDs = ast.literal_eval(file.readline())
    file.close()
    keepGoing = True
    while keepGoing:
        query = input("Search Index (enter 'q' to exit): ")
        if query.lower() == 'q':
            print("Goodbye!")
            keepGoing = False 
        else:
            try:
                start = time.time()
                handleSearch(query, docIDs)
                end = time.time()
#                 print(end-start)
            except:
                print("No results found.")
                continue
            
def handleSearch(query:str, docIDs:dict()):
    """ Main searcher function """
    words = []                      # holds the stemmed words
    allPostings = []                # Gets all the postings of the words
    allData = {}                    # Gets every {docId:tf} of every word
    sw = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.SnowballStemmer('english')
    for word in query.split():
        stemmed = stemmer.stem(word.strip().lower())
        if stemmed not in words and stemmed not in sw:
            words.append(stemmed)
    for word in words: 
        allData[word[0]] = {word: scorer.getSpecificDict(word[0]+".txt",word)} #{docID: tf}
    for word in words:
        allPostings.append(getPostings(word, allData))
    TFIDF_of_query = scorer.calcQwordTFIDF(query,allData)
    results = getTopKResults(5, sorted(allPostings,key=len), TFIDF_of_query, allData)
    print("Your results are:")
    i=1
    for postings in results:
        print("\t"+str(i)+". "+docIDs[int(postings)])
        i+=1
        
def getTopKResults(k:int, allPostings:list(), query:dict(), allData:"{letter:{word:{docID:count}}") -> list():
    """returns the top k results of all the postings. First, it gets all the postings that contains all the words.
        if less than the threshold k, will return all the words-1, etc. """ # the last part of this function doesn't work as well
    if len(allPostings) < 1:
        return []
    elif len(allPostings) == 1:
        return handleSingleQuery(k, list(query.keys())[0], allData)
    else:
        i = 0
        similar = []                # holds all the postings that contain all the words
        while i<len(allPostings)-1: # because allPosting is sorted by length, gets the similar values of smallest value to 2nd smallest 
            if len(similar) == 0:
                similar = list(set(allPostings[i]) & set(allPostings[i+1]))
                i+=1                                                        
            else:
                similar = list(set(similar) & set(allPostings[i+1]))
                i+=1
        allTDIF = getTopKResultsHelper(similar, query, allData)
        result = {} # result are the docID with the cosine similarity
        for docID in allTDIF:
            temp = {}
            temp[docID] = allTDIF[docID]
            result[docID] = scorer.computeCosSim(query, temp)[docID]
        finalPostings = heapq.nlargest(k, result, key=result.get)
        if len(finalPostings) < k:
            i=1
            for _ in allPostings:
                added = getTopKResults(k-len(finalPostings),allPostings[0:len(allPostings)-i],query)
                if added != similar:
                    finalPostings = finalPostings+added  
                if k-len(similar) == 0:
                    break
        return finalPostings

def getTopKResultsHelper(similarPostings:list(), query:dict(), data:"{indexLetter:{word:{docID:count}}}") -> "{docID: {term:TFIDF}}":
    """ Only initiated when query is larger than 1 word. Takes all the words and
        gets the TFIDF and stores them as {docID: {"term":TFIDF}}
    """
    allTFIDF = {}
    allWords = list(query.keys())
    for docID in similarPostings:
        scorer.calcAllWords(allWords, int(docID), data, allTFIDF)
    return allTFIDF

def handleSingleQuery(k:int, word:str, data:"{letter:{word:{docID:count}}"):
    """ Only initiated when query is 1 word. Returns a list of postings that has the 
        highest term frequency
    """
    return heapq.nlargest(k, data[word[0]][word], key=data[word[0]][word].get)

def getPostings(word:str,allData:"{letter:{word:{docID:count}}") -> list():
    """ will get the postings of the word in its entirety
    """
    return list(allData[word[0]][word].keys())
    

if __name__ == "__main__":
    main()    
            