from collections import defaultdict
import glob
import os
import json
import ast
import re

# ===== Important info ==================================================
# tf - term frequency: the number of times the term occurs in a document
# df - document frequency: the number of documents that contains the term
#    idf - log10(size of collection/df)
# tf-idf - (1+log(tf)) * log(N/df)
# =======================================================================

def cleanify(file) -> dict():
    ''' takes a file name and reads its randomized data to clean them, 
        rewrites -> term: [docID] to the same file'''
    data = open(file,"r")
    newData = defaultdict(list)
    results = {"totalTerms":0, "totalIDs":0}
    
    for line in data:
        values = line.split(":")
        if values[0].strip() not in newData:
            newData[values[0].strip()].append(values[1].strip())
        elif values[1].strip() > newData[values[0].strip()][-1]:
            newData[values[0].strip()].append(values[1].strip())
    data.close()
    
    rewrite = open(file,'w')
    for terms in newData:
        results["totalTerms"]+=1
        if max([int(docID) for docID in newData[terms]]) > results["totalIDs"]:
            results["totalIDs"] = max([int(docID) for docID in newData[terms]])
        rewrite.write(terms+": "+str([int(docID) for docID in newData[terms]])+"\n")
    rewrite.close()
    return results

def cleanifyIndex2(file) -> dict():
    ''' takes a file name and reads its randomized data to clean them, 
        rewrites -> {term: {docID:tf} to the same file'''
    data = open(file,"r")
    newData = dict()
    results = {"totalTerms":0, "totalIDs":0}
    for line in data:
        values = line.split(":")
        if len(values) > 2:
            newValues = [""]*2
            newValues[0] = ":".join(values[0:-1])
            newValues[1] = values[-1]
            values = newValues
        term = re.sub(r'[^\x00-\x7f]',r'', values[0].strip())
        if term not in newData:
            newData[term]={int(values[1].strip()):1}
        else:
            if int(values[1].strip()) not in newData[term]:
                newData[term][int(values[1].strip())] = 1
            else:
                newData[term][int(values[1].strip())] += 1
    data.close()
    rewrite = open(file,'w')
    rewrite.write(str(newData))
    rewrite.close()
    return results
# cleanifyIndex2("strong.txt")

def cleanifyIndex3(file):
    ''' takes a file name and reads its randomized data to clean them, 
        rewrites -> "term {docID:tf}" to the same file'''
    data = open(file,"r")
    newData = dict()
    results = {"totalTerms":0, "totalIDs":0}
    for line in data:
        values = line.split(":")
        if len(values) > 2:
            newValues = [""]*2
            newValues[0] = ":".join(values[0:-1])
            newValues[1] = values[-1]
            values = newValues
        term = re.sub(r'[^\x00-\x7f]',r'', values[0].strip())
        if term not in newData:
            newData[term]={int(values[1].strip()):1}
        else:
            if int(values[1].strip()) not in newData[term]:
                newData[term][int(values[1].strip())] = 1
            else:
                newData[term][int(values[1].strip())] += 1
    data.close()
    rewrite = open(file,'w')
    for key,value in newData.items():
        line = ""
        line += key + " " + str(value) + "\n"
        rewrite.write(line)
    rewrite.close()
    return results
# cleanifyIndex3("example.txt")

def cleanifyIndex4(file, strong: "{word:{docID:tf}}"):
    ''' takes a file name and reads its randomized data to clean them, 
        rewrites -> "term {docID:tf}" to the same file'''
    data = open(file,"r")
    newData = dict()
    results = {"totalTerms":0, "totalIDs":0}
    for line in data:
        values = line.split(":")
        if len(values) > 2:
            newValues = [""]*2
            newValues[0] = ":".join(values[0:-1])
            newValues[1] = values[-1]
            values = newValues
        term = re.sub(r'[^\x00-\x7f]',r'', values[0].strip())
        if term not in newData:
            if term in strong and values[1].strip() in strong[term]:
                newData[term]={int(values[1].strip()):2*strong[term][values[1].strip()]}
                strong[term].pop(values[1].strip())
            else:
                newData[term]={int(values[1].strip()):1}
        else:
            if int(values[1].strip()) not in newData[term]:
                if term in strong and values[1].strip() in strong[term]:
                    newData[term][int(values[1].strip())] = 2*strong[term][values[1].strip()]
                    strong[term].pop(values[1].strip())
                else:
                    newData[term][int(values[1].strip())] = 1
            else:
                if term in strong and values[1].strip() in strong[term]:
                    newData[term][int(values[1].strip())] += 2*strong[term][values[1].strip()]
                    strong[term].pop(values[1].strip())
                else:
                    newData[term][int(values[1].strip())] += 1
    data.close()
    rewrite = open(file,'w')
    for key,value in newData.items():
        line = ""
        line += key + " " + str(value) + "\n"
        rewrite.write(line)
    rewrite.close()
    return results

def analyze(path):
    '''Takes in the path to a directory. It is the directory of all the ran-through text files ->
       (ex.) path = '/Users/academicallyhonestalex/Downloads/(folder with all the txt files)' '''
    results = {"grandtotalTerms":0, "grandtotalIDs":0, "grandtotalSize":0}
    strong = open("strong.txt","r")
    strongDict = ast.literal_eval(strong.read())
    for file in glob.glob(os.path.join(path, '*.txt')):
        cleanifyIndex4(file,strongDict)
#         results["grandtotalSize"]+=os.path.getsize(file)
#         results["grandtotalTerms"] += perFile["totalTerms"]
#         if perFile["totalIDs"] > results["grandtotalIDs"]:
#             results["grandtotalIDs"] =  perFile["totalIDs"]
        print("file finished.")
    return results
# analyze(r"C:\Users\rsl01\Documents\ICS\CS121\Assignment3\index\index")

def createDocIDDict():
    file = open("DOC_ID.txt","r")
    file_out = open("DOC_ID_dict.txt","w")
    dictOut = {}
    for line in file.readlines():
        data = line.split("->")
        dictOut[int(data[0])] = data[1].rstrip()
    file_out.write(str(dictOut))
    file.close()
    file_out.close()
# createDocIDDict()
    
    
