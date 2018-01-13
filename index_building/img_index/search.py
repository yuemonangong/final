# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import cv2
query = raw_input("Query:")

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(query)
features = cd.describe(query)

# perform the search
searcher = Searcher("index.csv")
results = searcher.search(features)

# display the query
cv2.imshow("Query", query)

# loop over the results
for (score, result) in results:
	url,resultname,resulturl = result
	
	print url,resultname,resulturl
