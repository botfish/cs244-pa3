#!/usr/bin/python

"""
This script takes a folder of results and creates a graph similar to Figure 3 in the SPDY paper.
Requires matplotlib and numpy for the graphs
"""

import os
import sys
import math
import matplotlib
# Force matplotlib to not use any Xwindows backend, since we don't have a graphical environment
matplotlib.use('Agg')
import pylab
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np

parser = ArgumentParser(description="Figure 3 Graph Generation")

parser.add_argument('--dir', '-d',
                    help="Directory where the input is located",
                    default=".")

parser.add_argument('--out', '-o',
                    help="Directory to store the resulting graphs",
                    default=".")

#parse arguments
args = parser.parse_args()
# file names to look for
types = ['http', 'spdy']
graphs = ['loss', 'objnum', 'objsize']
# these mappings are just so we can get the columns in the right order
loss_map = {"0":0, "0.5":1, "1":2, "2":3}
ln = len(loss_map)
objnum_map = {"10K2":0, "10K8":1, "10K16":2, "10K32":3, "10K64":4,"10K128":5}
on = len(objnum_map)
objsize_map = {"100B64":0, "1K64":1, "10K64":2, "100K64":3}
om = len(objsize_map)
# data to graph
extracted_data = {'Loss': [[None]*ln,[None]*ln,[None]*ln], 'Object Number': [[None]*on,[None]*on,[None]*on], 'Object Size': [[None]*om,[None]*om,[None]*om]}

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

# parse the page load times out of the command line output in the files
def parseData():
	print "Parsing data"
	# walk the directory tree of the results folder
	for dirName, subdirList, fileList in os.walk(args.dir):
		dir_data = [getDirName(dirName)]
		for fname in fileList:
			if fname in types: #if this is a results file
				with open(os.path.join(dirName, fname)) as f: # parse out the page load time
					for line in f:
						if "=== [page load time]" in line:
							plt = float(line[20:].strip("\r\n"))/1000.0
							if fname == "http":
								dir_data.insert(1,plt)
							else:
								dir_data.append(plt)
							f.close()
							break
		# add the extracted data to the list
		addData(dir_data, os.path.basename(dirName))

# generates a grouped bar graph based on the data given
# data is expected to be an array of arrays, with the first element being the name of the subgraph
# name is the filename of the graph
def generateGraph(data, name):
	print "Generating graph for " + name
	figure, axis = plt.subplots()

	# make bars
	x_places = np.arange(len(data[0]))
	width = 0.35
	http_bars = axis.bar(x_places, data[1], width, color='b')
	spdy_bars = axis.bar(x_places+width, data[2], width, color='r')

	# make labels
	axis.set_ylabel('Page Load Time (seconds)')
	axis.set_title(name)
	axis.set_xticks(x_places+width)
	axis.set_xticklabels(data[0])
	axis.legend((http_bars[0], spdy_bars[0]), ('HTTP', 'SPDY'))

	#write to file
	pylab.savefig(os.path.join(args.out, name))


if __name__ == "__main__":
  parseData()
  for key, value in extracted_data.iteritems():
  	generateGraph(value, key)



