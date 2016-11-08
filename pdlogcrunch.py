#!/usr/bin/python

#
# Compile raw PagerDuty log file(s) into something more organized for Excel
#
# Dean Blevins
# Nov 2016
#

#import pdb		# Debugger

import argparse		# argv processor
import sys		# System functions
import os		# os.path.basename()
import csv		# CSV format functions
import collections      #

#####
##### FUNCTION: sub_total_log()
#####

def sub_total_log( fp, verbose, Verbose ):
	"Summarize stats of a PagerDuty CSV log file"

        MonList = []
	total = 0

	logfile = csv.reader(fp)

	# Read each line, build the array, and sum total lines
	for logline in logfile:
	    # Name of the monitor is in logline[1]
	    MonList.append(logline[1])
	    total += 1

	SumsMonList = collections.Counter(MonList)

        # Dump the list, sorted by count
	for Mon, count in SumsMonList.most_common():
		Perc = float(count)/float(total) * 100
		print '{:_<25} {:5d} {:5.1f}%'.format(Mon, count, Perc)

	print 'Total log lines({:s}) = {:d}'.format(fp.name, total)

	return()

#####
##### END FUNCTION: sub_total_log()
#####

#####
##### FUNCTION: proc_terse()
#####

def proc_terse( fp, ofp, verbose, Verbose ):
	"Output a terse output file: ID,Monitor,Date,Time"

	logfile = csv.reader(fp)
        outfile = csv.writer(ofp)

        TerseLine = []

	# Read each line, manipulate it and write it out
	for logline in logfile:
                # Build the new line
                # [0] = serial number
                # [1] = name of the source/monitor
                TerseLine.append(logline[0])
                TerseLine.append(logline[1])
                # Add the date, first change 2016-08-01 -> 08/01/2016
                timestamp = logline[2].split('T', 1)
                datestring = timestamp[0].split('-')
                date = datestring[1] + "/" + datestring[2] + "/" + datestring[0]
                TerseLine.append(date)
                # Get the time
                time = timestamp[1].rstrip("Z")
                TerseLine.append(time)
                
                outfile.writerow(TerseLine)
                TerseLine = []

#####
##### END FUNCTION: proc_terse()
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
parser.add_argument("-V", "--Verbose", help="very verbose output", action="store_true")
parser.add_argument("-s", "--summary", help="subtotal the drivers", action="store_true")
parser.add_argument("-o", "--output", type=str, help="output file (CSV)")
parser.add_argument("-t", "--terse", help="terse output components", action="store_true")
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

                # Default is to write to stdout
                ofp = sys.stdout

		if args.verbose or args.Verbose:
			print "Logfile name:", args.files[index]

		if args.summary:
			sub_total_log( fp, args.verbose, args.Verbose )

                if args.output:
                        ofp = open(args.output, 'w')
		        if args.verbose or args.Verbose:
		        	print "Output file name:", args.output

		if args.terse:
			proc_terse( fp, ofp, args.verbose, args.Verbose )

                # Close the input file
		fp.close()

# Close the output file
ofp.close()

