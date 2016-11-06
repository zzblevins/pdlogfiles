#!/usr/bin/python

#
# Compile a raw PagerDuty log file into something more organized for Excel
#
# Dean Blevins
# Oct 2015
#

#import pdb		# Debugger

import argparse		# argv processor
import sys		# System functions
import os		# os.path.basename()
import csv		# CSV format functions
import collections          #

#####
##### FUNCTION: process_pd_log()
#####

def sub_total_log( fp, verbose, Verbose ):
	"Process a PagerDuty CSV log file"

        MonList = []
	total = 0

	logfile = csv.reader(fp)

	# Read each line, build the array, and sum total lines
	for logline in logfile:
	    # Name of the monitor is in logline[1]
	    MonList.append(logline[1])
	    total += 1

	#print(MonList)
	SumsMonList = collections.Counter(MonList)
	#print(SumsMonList)
	#print(list(SumsMonList.elements()))
	#print(list(SumsMonList.values()))
	#print(list(SumsMonList.items()))
	#print(SumsMonList.items())

	for Mon, count in SumsMonList.items():
		Perc = float(count)/float(total) * 100
		#print("{0}: {1}".format(Mon, count))
		print "%s: %d (%.1f%%)" % (Mon, count, Perc)

	print "Total log lines = ", total

	return()

#####
##### END FUNCTION: sub_total_log()
#####

#####
##### MAIN
#####

codeversion =	2.1 
codelines =	0   
index =		0
TotalLines =	0   

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
parser.add_argument("-V", "--Verbose", help="more verbose output", action="store_true")
parser.add_argument("-s", "--summary", help="subtotal the drivers", action="store_true")
parser.add_argument("-t", "--totals", help="totals all files", action="store_true")
parser.add_argument("--version", help="version info", action="store_true")
parser.add_argument("files", help="source file(s)...", nargs=argparse.REMAINDER)
args = parser.parse_args()

#pdb.set_trace()	# Turn on debugger

# If just looking at program version, show it and exit
if args.version:
	print os.path.basename(sys.argv[0]), codeversion
	sys.exit(0)

# Process each file

for index in range(0, len(args.files)):

	# If this is a directory, skip
	if os.path.isdir(args.files[index]):
		if args.verbose or args.Verbose:
			print "Skipping directory:", args.files[index]
		continue

	with open(args.files[index], 'r') as fp:


		if args.verbose or args.Verbose:
			print "Logfile name:", args.files[index]

		if args.summary:
			sub_total_log( fp, args.verbose, args.Verbose )

		fp.close()

if args.totals:
	print "Total: ", TotalLines
