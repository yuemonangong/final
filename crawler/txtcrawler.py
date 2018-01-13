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

def sentences(page,folder,filename):
    flag=True
    f=open(os.path.join(folder, filename), 'w')
    
    while (flag):
        content=get_page(page)
        soup=bsp(content,'lxml')
        
        nextpage=soup.find('a',{'class':'active','rel':'next'})
        if nextpage==None:
            flag=False
            
        for i in soup.findAll('a',{'class':'xlistju','title':'查看本句'}):
            f.write(i.text.encode('utf-8'))
            f.write('\n\n')
        if flag:
            page=urlparse.urljoin(page,nextpage.get('href','')).encode('utf-8')
    f.close()

def get_page(page):
    global ips
    content = ''
    try:
        proxies=ips[random.randint(0,len(ips)-1)]
        headers = {'Referer':page,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        req=requests.get(page,proxies=proxies, headers=headers,timeout=3.0)
        content=req.content
        time.sleep(2)
    except:
        print 'error'
    return content

def get_all_links(content, page):
    items={}
    soup=bsp(content,"lxml")
    p=re.compile('(.*)查看《(.*)》名句(.*)')
    for i in soup.findAll('a',{'class':'xqallarticletilelink'}):
        url=i.get('href','')
        url=urlparse.urljoin(page,url)
        m=p.match(str(i))
        if m!=None:
            title=m.group(2)
            items[title]=url.encode('utf-8')
    nextpage=soup.find('a',{'class':'active','rel':'next'})
    if nextpage!=None:
        nextpage=urlparse.urljoin(page,nextpage.get('href','')).encode('utf-8')
    return items,nextpage

def add_page_to_folder(title, page):
    index_filename = 'index.txt'
    folder = 'html'
    filename = title
    index = open(index_filename, 'a')
    index.write(page + '\t' + filename +'\t'+title+ '\n')
    index.close()
    if not os.path.exists(folder):
        os.mkdir(folder)
    sentences(page,folder,filename)

def one_class_crawl(classname):
    page='http://www.juzimi.com/allarticle/'+classname
    flag=True
    while(flag):
        content=get_page(page)
        items,nextpage=get_all_links(content, page)
        if nextpage==None:
            flag=False

        for key in items.keys():
            print 'adding',key
            add_page_to_folder(key, items[key])
            time.sleep(10)
        page=nextpage

def crawl():
    classes=['jingdiantaici','zhaichao','sanwen','dongmantaici']
    for c in classes:
        one_class_crawl(c)

ips=[{'http': 'http://111.230.247.240:808'},{'http': 'http://123.185.131.199:8118'},
     {'http': 'http://183.52.150.81:61234'},{'http': 'http://180.114.229.69:808'},
     {'http': 'http://121.206.217.165:808'},{'http': 'http://183.52.150.34:61234'}]
     
crawl()
