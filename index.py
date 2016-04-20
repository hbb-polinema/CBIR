# Usage: >> python index.py --dataset dataset --index index.csv
# or >> py index.py -d <your_folder_data_images> -i <output_file_index.csv>

# import the necessary packages
from module.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

# Labeling image ID to index file
def labeling(imgID):
	label = ''
	id = imgID[0:imgID.find('.jpg')]
	
	if len(id) <= 2:
		label = 'people'
	
	if len(id) == 3:
		if int(id[0]) is 1:
			label = 'beach'
		elif int(id[0]) == 2:
			label = 'building'
		elif int(id[0]) == 3:
			label = 'bus'
		elif int(id[0]) == 4:
			label = 'dinasaur'
		elif int(id[0]) == 5:
			label = 'elephant'
		elif int(id[0]) == 6:
			label = 'flower'
		elif int(id[0]) == 7:
			label = 'horse'
		elif int(id[0]) == 8:
			label = 'mountain'
		elif int(id[0]) == 9:
			label = 'food'
	
	print label
	return label
	
# Estimated timing
start_time = time.time()

# initialize the color descriptor
# using 8 Hue bins, 12 Saturation bins, and 3 Value bins
cd = ColorDescriptor((8, 12, 3))

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

# Result estimated time
print("\n--- Estimated time execution: %s seconds ---" % round(time.time() - start_time, 4))