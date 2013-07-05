#! /usr/bin/env python
#coding=utf-8

import urllib
from bs4 import BeautifulSoup
import socket
import time
import MySQLdb
import sys
import jieba,jieba.analyse

reload(sys)
sys.setdefaultencoding('utf-8')

timeout = 15                        # 网络较好时不需要
socket.setdefaulttimeout(timeout)
sleep_download_time = 30
time.sleep(sleep_download_time) 

url_scnews=[]; html_scnews=[]; templist_scnews=[] 

url_scnews0 = 'http://roll.ent.sina.com.cn/ent_more/mxqjc/ndqd/index.shtml'
html_scnews0 = BeautifulSoup(urllib.urlopen(url_scnews0).read(),from_encoding='gb18030')   
newslist_scnews0 = html_scnews0.find("ul",{"class":"list_009"}).findAll("a")

newslist_scnews = newslist_scnews0 
 
hlink_scnews=[]
for i in newslist_scnews: 
    hlink_scnews.append(i['href']) 
    
title_scnews=[]
for i in newslist_scnews: 
    title_scnews.append(i.get_text())   
   
temp_scnews=[]
for i in hlink_scnews :
    try:
        temp_scnews.append(BeautifulSoup(urllib.urlopen(i).read(),from_encoding="gb18030").find("div",{"id":"artibody"}).findAll("p"))
    except:
        temp_scnews.append("")
    
tscnews=[]
for i in range(len(temp_scnews)):
    if temp_scnews[i] !="":
        tscnews.append([])
        t = temp_scnews[i]
        for j in t:
            tscnews[i].append(j.get_text())
    else:
        tscnews.append("")
 
contents_scnews=[]
for i in tscnews:
    contents_scnews.append('\n'.join(i))
 
keyword=[]
for i in contents_scnews:
    keyword.append(",".join(jieba.analyse.extract_tags(i,topK=5)))
     
gettime = []
for i in range(len(hlink_scnews)):
    gettime.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
 
news_scnews=[]   
for i in range(len(hlink_scnews)):
    news_scnews.append(('娱乐','新浪网',hlink_scnews[i],title_scnews[i].encode('utf-8'),keyword[i].encode('utf-8'),contents_scnews[i].encode('utf-8'),gettime[i]))

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="******",charset="UTF8") 
    conn.select_db('viewsys') 
    cur=conn.cursor()
    cur.executemany("""insert into newsapp_getnews(cat,src,url,title,keyword,contents,time) values(%s,%s,%s,%s,%s,%s,%s) """,news_scnews)
    conn.commit()
    conn.close
    print '国内娱乐'+'\t'+'成功'+'\t'+str(len(news_scnews))+'\t'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
except:
    print '国内娱乐'+'\t'+'失败'+'\t'+'0'+'\t'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

del url_scnews,html_scnews,templist_scnews,hlink_scnews,contents_scnews,news_scnews
