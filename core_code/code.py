import web
from web import form
import urllib2
import os
import sys, lucene,jieba,threading,re

INDEX_DIR = "IndexFiles.index"

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import cv2

reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
    '/', 'index',
    '/s', 's' ,
    '/im', 'index_img',
    '/i', 'image'
)

render = web.template.render('templates') # your templates

login1 = form.Form(
    form.Textbox('Sentence'),
    form.Button('Search'),
)

login2 = form.Form(
    form.Textbox('Path'),
    form.Button('Search'),
)

def func1(command):
    global vm_env
    STORE_DIR = "index"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    #lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    if command == '':
        return []
    command_list = jieba.cut(command)
    command = " ".join(command_list)
    query = QueryParser(Version.LUCENE_CURRENT, "contents",                            analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    result = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        doct = { 'title':doc.get("title"),'url' : doc.get("url"),"sentence":doc.get("sentence")}
        result.append(doct)
    del searcher
    return result

def func2(command):
    folder='target'
    command=os.path.join(folder, command)
    # initialize the image descriptor
    cd = ColorDescriptor((8, 12, 3))

    # load the query image and describe it
    query = cv2.imread(command)
    features = cd.describe(query)

    # perform the search
    searcher = Searcher("index.csv")
    results = searcher.search(features)

    # loop over the results
    result = []
    for (score, resultp) in results:
	url , imgname ,imgurl = resultp
	doct = {"url":url,'name':imgname,'imgurl': imgurl}
	result.append(doct)
    return result
    
class index:
    def GET(self):
        f = login1()
        return render.formsen(f)

class index_img:
    def GET(self):
        f = login2()
        return render.formimg(f)

class s:
    def GET(self):
        user_data = web.input()
        f = login1()
        command = user_data.Sentence
        a = func1(command)
        return render.resultsen(a,command,f)

class image:
    def GET(self):
        user_data = web.input()
	f = login2()
        command = user_data.Path
        a = func2(command)
	for result in a:
		print result['imgurl']
        return render.resultimg(a,command,f)

if __name__ == "__main__":
    vm_env=lucene.initVM()
    app = web.application(urls, globals())
    app.run()
