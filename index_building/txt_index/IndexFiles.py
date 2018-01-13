#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time ,re,jieba
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

reload(sys)
sys.setdefaultencoding("utf-8")
"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, file ,storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer,1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, file, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root,file, writer):
        f = open(file,'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line=line.decode('utf-8')
            line=line.split()
            if len(line)==2 :
                line.append('')
            if len(line)>=3:
                tmp0=[]
                for i in range(2,len(line)):
                    tmp0.append(line[i])
                tmp=[]
                tmp.append(line[0])
                tmp.append(line[1])
                tmp.append(' '.join(tmp0))
                line=tmp
		filename  = line[1]
		url = line[0]
                title = line[2]
                print "adding", title
                try:
                    path = os.path.join(root, title)
                    file = open(path)
                    contents = unicode(file.read(),'utf-8')
		    contents_list = contents.split("\n")
                    file.close()
		    count = 0
		    for sentence in contents_list:
			print sentence,'\n'
			contents_list = jieba.cut(sentence)
			content = " ".join(contents_list)
			doc = Document()
			doc.add(Field("title", title ,Field.Store.YES,Field.Index.NOT_ANALYZED))
			doc.add(Field("name", filename, Field.Store.YES,Field.Index.NOT_ANALYZED))
			doc.add(Field("path", root, Field.Store.YES,Field.Index.NOT_ANALYZED))
			doc.add(Field("url",url, Field.Store.YES,Field.Index.NOT_ANALYZED))
			if len(content) > 0:
				doc.add(Field("sentence",sentence,Field.Store.YES,Field.Index.NOT_ANALYZED))
				doc.add(Field("contents", content,Field.Store.YES,Field.Index.ANALYZED))
			else:
				print "warning: no content in %s" % filename
			writer.addDocument(doc)
			count += 1
		    print count 
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('html','index.txt' ,"index", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
