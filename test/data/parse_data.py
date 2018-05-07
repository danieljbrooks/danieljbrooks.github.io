# -*- coding: utf-8 -*-
"""
Parses csv files containing distances and scales and outputs JSON object file
"""

import pandas as pd
import numpy as np

def read_dist(filename):
	"""
	Reads distance from distance table produced by Arseny's script.
	return: list containing lists (i.e. dist[0][3])
	"""
	f = open(filename, "r")
	dist_list = []
	for line in f:
		split_line = line.split()
		dist_list.append(split_line)
	f.close()
	return dist_list

def print_properties(dist, scale):
	"""
	Prints out descriptive informations about dist and scale data variables.
	return: Nothing
	"""
	print("Analytics on dist and scale data variables below.")
	print("scale.head()=\n", scale.head())
	print("len(scale)=", len(scale))
	print("scale.color.unique()=", scale.color.unique())
	print("np.shape(dist)=", np.shape(dist))
	return

def get_group(char):
	"""
	Maps colors to arbitrary groups.
	"""
	if char == "W":
		return 1
	elif char == "U":
		return 2
	elif char == "B":
		return 3
	elif char == "R":
		return 4
	elif char == "G":
		return 5
	elif char == "M":
		return 6
	elif char == "0":
		return 7
	else:
		return 8

def create_json(dist, scale, json_path, cutoff=0.8):
	"""
	Creates a .json file for graph visualization named json_path.
	"""

	num_cards = len(scale)

	#Write the first few lines.
	f = open(json_path, 'w')
	f.write('{\n')
	f.write('  "nodes": [\n')

	#Write the node data to file 
	for card in range(num_cards):

		#Create nodes in json.
		str2write = '    {"id": "' + scale["name"][card] + '", "group": ' \
			+ str(get_group(scale["color"][card])) + '}'
		
		#Handle trailing commas.
		if card < num_cards-1:
			str2write+=","

		#Write to file.
		f.write(str2write + "\n")

	#Intermediate section.
	f.write('  ],\n')
	f.write('  "links": [\n')

	#Check each unique pair of points.
	list_link = []
	for card1 in range(num_cards):
		for card2 in range(card1+1, num_cards):
			
			#Display only closely related cards.
			cur_dist = float(dist[card1][card2])
			if cur_dist<=cutoff:
				list_link.append('    {"source": "' + scale["name"][card1] \
					+ '", "target": "' + scale["name"][card2] + '", "value": 1}')

	#Write link data to file with no trailing comma.
	num_link = len(list_link)
	for n in range(num_link-1):
		f.write(list_link[n] + ",\n")
	f.write(list_link[num_link-1] + "\n")

	#Write the last few lines.
	f.write("  ]\n")
	f.write("}\n")
	f.close()
	print("Created json file.")

#Read in the relevant files.
dist = read_dist("dist.csv")
scale = pd.read_csv("scale.csv")

#print_properties(dist, scale)
create_json(dist, scale, "test.json")
