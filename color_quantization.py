import argparse
import numpy as np
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Where your image")
ap.add_argument("-c", "--cluster", required = True,
	help = "Number of Cluster")
args = vars(ap.parse_args())

def centroid_histogram(label_, center_):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(label_)) + 1)
	(hist, _) = np.histogram(center_, bins = len(numLabels))

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()

	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0

	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar

print 'process...'

img = cv2.imread(args["image"])
data = img.reshape((-1,3))

# show our image
cv2.imshow('Original Image', img)
cv2.waitKey(0)

print 'Data = ', data, 'len = ', len(data)

# convert to np.float32
data = np.float32(data)
 
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = int(args["cluster"])
# kmeans(data, K, bestLabels, criteria, attempts, flags[, centers]) -> retval, bestLabels, centers
ret,label,center = cv2.kmeans(data, K, K, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
 
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color
hist = centroid_histogram(label, center)
bar = plot_colors(hist, center)
print 'Bar = ', bar
cv2.imshow('Bar Cluster %s'% (K), bar)
cv2.waitKey(0)

print '\nreturn value:', ret, '\n\nlabel:\n', np.unique(label), '\n\ncenter:\n', center
print 'len(center) = ', len(center)
print 'len(res) = ', len(res)
print 'label flatten = ', label.flatten(), ' len = ', len(label.flatten()), label[:10]

tambah = np.append(center, center, axis=0)
print '\n\n tambah = ', tambah

cv2.imshow('Image Result after Color Quantization', res2)
cv2.waitKey(0)
cv2.destroyAllWindows()