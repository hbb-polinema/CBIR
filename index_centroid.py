import argparse
import numpy as np
import cv2
import color_quantization as cq

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "where your dataset")
ap.add_argument("-i", "--index", required = True,
	help = "filename save index centroid")
ap.add_argument("-c", "--cluster", required = True,
	help = "Number of Cluster")
args = vars(ap.parse_args())

def color_q():
	pass

# open the output index file for writing
output = open(args["index"], "w")

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	print 'imagePath: ',imagePath
	imageID = imagePath[imagePath.rfind("\\") + 1:]
	print 'imageID: ',imageID
	image = cv2.imread(imagePath)
	
	# describe the image
	features = cd.describe(image)

	# write the features to file
	features = [str(f) for f in features]
	# output.write("%s,%s\n" % (imageID, ",".join(features)))
	output.write("%s,%s,%s\n" % (imageID,labeling(imageID),",".join(features)))

# close the index file
output.close()