#encoding=utf8
import urllib
import socket
import requests
socket.setdefaulttimeout(3)
f = open("proxy")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "https://"+ip[0]+":"+ip[1]
    proxy_temp = {"https":proxy_host}
    proxys.append(proxy_temp)
url = 'http://www.juzimi.com/'
for proxy in proxys:
    try:
        res = requests.get(url,proxies=proxy,timeout=3).read()
        print proxy
        print res
        print '000000000000000000000'
    except Exception,e:
        print proxy
        print e
        print '000000000000000000000'
        continue
