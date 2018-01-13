# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
import glob
import cv2

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
output = open("index.csv" ,"w")

# use glob to grab the image paths and loop over them
for imagePath in glob.glob("html" + "/*/*.jpg"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	imageID = imagePath[imagePath.find("/") + 1:]
	image = cv2.imread(imagePath)
	infile = open("indeximg.txt","r")
    	infilelines = infile.readlines()
    	infile.close()
	for line in infilelines:
    		line = line.split()
    		if (line[1] == imageID[:imageID.find('/')]):
			url = line[0]
			imgname = line[2]
			imgfile = open("html/"+line[1]+"/index.txt",'r')
			imgfilelines = imgfile.readlines()
    			imgfile.close()
			for imgline in imgfilelines:
				imgline = imgline.split()
				if (imgline[1] == imageID[imageID.find('/')+1:]):
					imgurl = imgline[0]

	# describe the image
	try:
		features = cd.describe(image)
		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s,%s,%s\n" % (url,imgname,imgurl,",".join(features)))
	
	except:
		print imageID
	
	
for imagePath in glob.glob("html" + "/*/*.png"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	imageID = imagePath[imagePath.find("/") + 1:]
	image = cv2.imread(imagePath)
	infile = open("indeximg.txt","r")
    	infilelines = infile.readlines()
    	infile.close()
	for line in infilelines:
    		line = line.split()
    		if (line[1] == imageID[:imageID.find('/')]):
			url = line[0]
			imgname = line[2]
			imgfile = open("html/"+line[1]+"/index.txt",'r')
			imgfilelines = imgfile.readlines()
    			imgfile.close()
			for imgline in imgfilelines:
				imgline = imgline.split()
				if (imgline[1] == imageID[imageID.find('/')+1:]):
					imgurl = imgline[0]

	# describe the image
	try:
		features = cd.describe(image)
		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s,%s,%s\n" % (url,imgname,imgurl,",".join(features)))
	
	except:
		print imageID
output.close()
