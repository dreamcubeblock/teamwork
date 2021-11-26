import re
import os
#from database import myInsert
def importwords(path):
    english=[]
    chinese=[]
    with open(path, 'r',encoding="gbk") as f:
        file = f.readlines() 
    #file.split("\n")
    for data in file:
        words=re.sub('\n','',data).split()
#        data.split(" ")
        english.append(words[0])
        chinese.append(words[1])
    return english,chinese

import pymysql
def myInsert(username,english,chinese,book,zerolist):

   db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")#
 

   cursor = db.cursor()
#   try:


   sql = "INSERT INTO %s.word(english, chinese,book,state) VALUES(%s,%s,%s,%s);".format(username)
   val=[]
   for i in range(0,len(english)):
       val.append([english[i],chinese[i],list[i],zerolist[i]])

   cursor.executemany(sql,val)

   db.commit()
      # print("finishe!")
   #except BaseException:

    #  print('------faile!', word_name)
    #  db.rollback()
def createtable(username):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    sql="create table %s.word(create table group6.word(english char(50),chinese char(100),book char(50),state char(5));".format(username)
    cursor.execute(sql)
    db.commit()
def updatetable(username,word,state):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    if state:
        sql="update %s.word set state=1 where english=word;".format(username)
        cursor.excute(sql)
        db.commit()

def getanswer(username,word):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database=username)
    cursor=db.cursor()
    sql=" select  top  3  chinese  from  %s.word  order  by  newid() where english!=word;".format(username)
    cursor.excute(sql)
    #db.commit()
    results=cursor.fetchall()
    sql="select chinese from %s.word where english=word;".format(username)
    cursor.excute(sql)
    rightanswer=cursor.fetchall()
    return rightanswer,results

if __name__=='__main__':
    path='/home/四级单词表.txt'
    english,chinese=importwords(path)
    
    name=os.path.basename(path)
    list=[]
    length=len(english)
    name=name.split(".")[0]
    zerolist=[]
    for i in range(0,length):
        list.append(name)
        zerolist.append(0)

    print(type(zerolist[0]))

    myInsert(english,chinese,list,zerolist)
