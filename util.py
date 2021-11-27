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
def myInsert(userid,english,chinese,book,zerolist):

   db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")#
 

   cursor = db.cursor()
#   try:


   sql = "INSERT INTO group6.word(english, chinese,book) VALUES(%s,%s,%s);"
   
   val=[]
   for i in range(0,len(english)):
       val.append([english[i],chinese[i],list[i]])

   cursor.executemany(sql,val)
   for i in range(0,len(english)):
    sql="insert into group6.user_"+str(userid)+"(status) values(%s);"
   #print(zerolist)
  # print(type(zerolist[0]))
   #zerolist=tuple(zerolist)
    cursor.execute(sql,['0'])
   db.commit()
def createusertable(userid):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    sql="create table group6.user_"+str(userid)+"(wordid int auto_increment primary key,status char(10));"
   # print(sql)
    cursor.execute(sql)
 #    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")#
 #    sql="insert into group6.user-%s(status) values(%s);".format(userid)
 #    cursor.execute(sql,zerolist)
  #   db.commit()
      # print("finishe!")
   #except BaseException:

    #  print('------faile!', word_name)
    #  db.rollback()

def createtable(userid):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    sql="create table group6.word(wordid int not null auto_increment primary key,english char(50),chinese char(100),book char(50));"
    #sql="create table group6.user-%s(wordid int identitiy,status char(10));".format(userid)
    cursor.execute(sql)
    db.commit()
def updatetable(userid,id,state):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    if state:
        sql="update group6.user_"+str(userid)+" set status='1' where wordid="+str(id)+";"
        #print(sql)
        cursor.execute(sql)
        db.commit()

def getanswer(word):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    sql=" select  chinese  from  group6.word where wordid!="+"'"+word+"'"+" order by rand() limit 3;"
    cursor.execute(sql)
    #db.commit()
    results=cursor.fetchall()
    sql="select chinese from group6.word where english="+"'"+word+"'"+";"
    print(sql)
    cursor.execute(sql)
    rightanswer=cursor.fetchall()
    return rightanswer,results
def getquestion(userid,number):
    db = pymysql.connect(host="localhost",user="root",password="28853379", database="group6")
    cursor=db.cursor()
    sql=" select wordid,english from group6.word where wordid in(select wordid from group6.user_"+str(userid)+" where status='0') order by rand() limit "+str(number)+";"
    #print(sql)
    cursor.execute(sql)
    #db.commit()
    results=cursor.fetchall()
    return results
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
        zerolist.append([str(0)])

    #print(type(zerolist[0]))
    #createtable(2)
    #createusertable(2)
    #myInsert(2,english,chinese,list,zerolist)
    #words=getquestion(2,50)
    #print(words)
  #  right,wrong=getanswer("abandon")
 #   print(right)
#    print(wrong)
#:    updatetable(2,4501,True)

