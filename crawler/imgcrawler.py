# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bsp
import urllib2
import re
import urlparse
import os
import urllib
import sys
import threading
import Queue
import time
import requests
import random

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    content = ''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
    try:
        req=urllib2.Request(page,None,headers)
        content=urllib2.urlopen(req,timeout=3.0).read()
        time.sleep(random.uniform(2,4))
    except:
        print 'error'
    return content

def get_all_links(content, page):
    links = []
    soup=bsp(content,"lxml")
    p=re.compile('^http')
    p1=re.compile('^http://www.6vhao.tv')
    for i in soup.findAll('a',{'href':re.compile('^http|^/')}):
        url=i.get('href','')
        m=p.match(url)
        if m==None:
            url=urlparse.urljoin(page,url)
        m1=p1.match(url)
        if m1!=None:
            links.append(url)
    return links
       
def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    src_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
    if content == '':
        return
    soup=bsp(content,"lxml")
    title=str(soup.head.title)
    p=re.compile('<title>《(.+)》下载_迅雷下载_(.+)_6v电影网</title>')
    m=p.match(title)
    if m==None:
        return
    title=m.group(1)

    index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'html'                 #存放网页的文件夹
    filename = valid_filename(page) #将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename +'\t'+title+ '\n')
    index.close()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)

    imgfolder=os.path.join(folder, filename)
    if not os.path.exists(imgfolder):  #如果文件夹不存在则新建
        os.mkdir(imgfolder)
    imgurls=[]
    for i in soup.findAll('img',{'src':re.compile('^http.*\.jpg$|^http.*\.png$')}):
        imgurls.append(i.get('src',''))
    for imgurl in imgurls:
        imghtml=requests.get(imgurl,headers=src_headers)
        img=imghtml.content
        imgname=valid_filename(imgurl)
        imgindex = open(os.path.join(imgfolder,index_filename), 'a')
        imgindex.write(imgurl + '\t' + imgname + '\n')
        imgindex.close()
        with open(os.path.join(imgfolder, imgname),'ab') as f:
            f.write(img)
        time.sleep(random.uniform(2,4))
    
def crawl():
    global count
    while tocrawl:
        if (count>=max_page):
            break
        page = tocrawl.get()
        if page not in crawled:
            print page
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            for e in outlinks:
                tocrawl.put(e)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
                count+=1
                print count
            
            tocrawl.task_done()

count=0
tocrawl = Queue.Queue()
seed=raw_input("Address: ")
tocrawl.put(seed)
max_page=int(input("max page: "))
crawled = []
graph = {}
varLock = threading.Lock()
threads=[]
Num=8
for i in range(Num):
    t = threading.Thread(target=crawl)
    t.setDaemon(True)
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
