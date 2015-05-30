#!/usr/bin/python

"""
This script takes a folder of results and creates a graph similar to Figure 7 in the SPDY paper.
It works with the "retransmissions" folder inside the overall results graph.
Requires matplotlib and numpy for the graphs.
"""

import os
import math
import matplotlib
# Force matplotlib to not use any Xwindows backend, since we don't have a graphical environment
matplotlib.use('Agg')
import pylab
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np

parser = ArgumentParser(description="Figure 7 Graph Generator")

parser.add_argument('--dir', '-d',
                    help="Directory where the input is located",
                    default=".")

parser.add_argument('--out', '-o',
                    help="Directory to store the resulting graphs",
                    default=".")

#parse arguments
args = parser.parse_args()

# file names to look for
base = "retransmissions"
types = ['http_netstat', 'spdy_netstat']

# data to graph
extracted_data = {'http': [], 'spdy': []}
# name of graph
name = "tcp_retransmissions"

# extracts the variable parameter from the name
def getDirName(name):
	name = os.path.basename(name)
	for g in graphs:
		if g in name:
			return name.strip(g+"_")
	return name

# adds the data to the correct key-value pair of the results
def addData(data, name):
	if 'loss' in name:
		index = loss_map[data[0]]
		extracted_data['Loss'][0][index] = data[0]
		extracted_data['Loss'][1][index] = data[1]
		extracted_data['Loss'][2][index] = data[2]
	# in these cases, the lexographic ordering the data comes in is not the ordering we want
	elif 'objnum' in name: 
		index = objnum_map[data[0]]
		extracted_data['Object Number'][0][index] = data[0]
		extracted_data['Object Number'][1][index] = data[1]
		extracted_data['Object Number'][2][index] = data[2]
	elif 'objsize' in name:
		index = objsize_map[data[0]]
		extracted_data['Object Size'][0][index] = data[0]
		extracted_data['Object Size'][1][index] = data[1]
		extracted_data['Object Size'][2][index] = data[2]

# parse the number of retransmissions out of the files
def parseData():
	print "Parsing data"
	# walk the directory tree of the results folder
	for dirName, subdirList, fileList in os.walk(args.dir):
		if "retransmissions" in dirName:
			for fname in fileList:
				if fname in types: #if this is a results file
					with open(os.path.join(dirName, fname)) as f: # parse out the page load time
						for line in f:
							if "segments retransmited" in line:
								plt = int(line[:-22].strip("\r\n"))
								if fname == "spdy_netstat":
									extracted_data['spdy'].append(plt)
								else:
									extracted_data['http'].append(plt)

# generates a CDF plot after normalizing the data
def generateGraph():
	print "Generating graph..."
	figure, axis = plt.subplots()

	for key, value in extracted_data.iteritems():
		# sort the data
		sorted_data = np.sort(value)
		# set the x-axis range
		pylab.xlim([-1,max(sorted_data)+5])
		# plot the CDF
		y_axis = np.arange(len(sorted_data))/float(len(sorted_data))
		if key == "http":
			http_line = plt.plot(sorted_data, y_axis, 'r', linewidth=3)
		else:
			spdy_line = plt.plot(sorted_data, y_axis, 'b--', linewidth=3)

	# make labels
	axis.set_ylabel('CDF')
	axis.set_xlabel('# of Retransmissions')
	axis.set_title('Comparison of Retransmissions')
	axis.legend((http_line[0], spdy_line[0]), ('HTTP', 'SPDY'))

	#write to file
	pylab.savefig(os.path.join(args.out, name))


if __name__ == "__main__":
  print "Plotting Figure 7..."
  parseData()
  generateGraph()



