import re
import os
from database import myInsert
def importwords(path):
    english=[]
    chinese=[]
    with open(path, 'r') as f:
        file = f.readlines() 
    #file.split("\n")
    for data in file:
        words=re.sub('\n','',data).split()
#        data.split(" ")
        english.append(words[0])
        chinese.append(words[1])
    return english,chinese

if __name__=='__main__':
    path='C:\\Users\\dream\\Downloads\\Compressed\\english4jdc_downcc\\英语四级单词表.txt'
    english,chinese=importwords(path)
    name=os.path.basename(path)
    name=name.split(".")
    myInsert(english[0],chinese[0],name[0])