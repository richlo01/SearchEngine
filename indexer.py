from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
from simhash import Simhash, SimhashIndex
import json
from pathlib import Path
from bs4 import BeautifulSoup
import os.path
import re
from urllib.parse import urldefrag
import sys

input_path=Path(r'C:\Users\rione\Documents\UCI\CS 121\DEV') #replace with where DEV is stored
#input_path=Path(r'/Users/academicallyhonestalex/Downloads/DEV' )
save_path=Path(r'C:\Users\rione\Documents\UCI\CS 121\Indexer\spacetime-crawler4py\index')#replace with save_path
print("Creating list of files")
files=list(input_path.rglob("*.json"))#list of all files
print("Created list of files")
objs=[] #list of DOC_ID and Simhash
urls=set()
#for x in files:
#    print(x)
#print(len(files)) #around 55300 files
STOPWORDS=set("""
a
about
above
after
again
against
all
am
an
and
any
are
aren't
as
at
be
because
been
before
being
below
between
both
but
by
can't
cannot
could
couldn't
did
didn't
do
does
doesn't
doing
don't
down
during
each
few
for
from
further
had
hadn't
has
hasn't
have
haven't
having
he
he'd
he'll
he's
her
here
here's
hers
herself
him
himself
his
how
how's
i
i'd
i'll
i'm
i've
if
in
into
is
isn't
it
it's
its
itself
let's
me
more
most
mustn't
my
myself
no
nor
not
of
off
on
once
only
or
other
ought
our
ours
""".split("\n"))
STOPWORDS.update({"the","to","|","with","&","will","this",
                 ",","by","-","that","your","=","by",
                 "was"})
DOC_ID=0 #counter for each url
INDEX_DICT=defaultdict(str) #Use this to store {doc_id(int):url}
BUFFER=[]
for i in range(28):
    BUFFER.append("")
def stem_word(word:str):
    """Snowball stemmer which we can implement if needed"""
    ks=SnowballStemmer("english")
    return ks.stem(word)


#assuming that the files are already open and created
#print(files)
for doc in files:
    print(os.path.getsize(doc))
    if os.path.getsize(doc)>20000000:
        continue
    page=json.load(open(doc))
    url=urldefrag(page["url"])[0]
    if "content" in page:
        #print(page["content"].title)
        soup = BeautifulSoup(page["content"],features="html.parser")
        data=soup.get_text()
        simmed=Simhash(data)
        index=SimhashIndex(objs,k=3)
        regex=re.compile(r'^[\W_]+|[\W_]+$')
        if url not in urls and len(index.get_near_dups(simmed))==0:
            DOC_ID+=1
            INDEX_DICT[DOC_ID]=url
            urls.add(url)
            print(DOC_ID,INDEX_DICT[DOC_ID])
            objs.append((DOC_ID,simmed))
            strong=soup.find_all(["h1", "h2" ,"h3","title", "strong"])
            txt=[s.get_text() for s in strong]
            for t in txt:
                for word in t.split():
                    word=regex.sub("",word.lower())
                    if word.lower() not in STOPWORDS:
                        text_to_write=stem_word(word)+":"+str(DOC_ID)+"\n"
                        BUFFER[27]=BUFFER[27]+text_to_write
            for word in (data.split()):
                word=regex.sub("",word.lower())
                if word.lower() not in STOPWORDS:
                    if word[0].isalpha():
                        text_to_write=stem_word(word)+":"+str(DOC_ID)+"\n"
                        try:
                            index=ord(word[0].lower())-97
                        except:
                            text_to_write=stem_word(word)+":"+str(DOC_ID)+"\n"
                            BUFFER[26]=BUFFER[26]+text_to_write
                            continue
                        #print(index)
                        if index<26:
                            BUFFER[index]=BUFFER[ord(word[0].lower())-97]+text_to_write
                    else:
                        text_to_write=stem_word(word)+":"+str(DOC_ID)+"\n"
                        BUFFER[26]=BUFFER[26]+text_to_write
            print(sys.getsizeof(BUFFER[26]))
            if sys.getsizeof(BUFFER[26])>75000:
                print("Writing")
                for string in range(26):
                    file_name=chr(string+97)+".txt"
                    current_file=open(os.path.join(save_path,file_name), "a+",errors="ignore")
                    current_file.write(BUFFER[string])
                    current_file.close()
                current_file=open(os.path.join(save_path,"other.txt"), "a+",errors="ignore")
                current_file.write(BUFFER[26])
                current_file.close()
                current_file=open(os.path.join(save_path,"strong.txt"), "a+",errors="ignore")
                current_file.write(BUFFER[27])
                current_file.close()
                for i in range(28):
                    BUFFER[i]=""
                objs=[]
for string in range(26):
    file_name=chr(string+97)+".txt"
    current_file=open(os.path.join(save_path,file_name), "a+",errors="ignore")
    current_file.write(BUFFER[string])
    current_file.close()
current_file=open(os.path.join(save_path,"other.txt"), "a+",errors="ignore")
current_file.write(BUFFER[26])
current_file.close()
current_file=open(os.path.join(save_path,"strong.txt"), "a+",errors="ignore")
current_file.write(BUFFER[27])
current_file.close()

current_file=open(os.path.join(save_path,"DOC_ID.txt"), "a+",errors="ignore")
for k,v in INDEX_DICT.items():
    current_file.write(str(k)+"->"+v+"\n")
current_file.close()

                        

       


