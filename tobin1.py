#!/usr/bin/env python

import argparse
import os.path
from scipy.io import wavfile

parser=argparse.ArgumentParser(description="Takes a wav file and sets channel 1 to 1 or 0")

parser.add_argument('-i', '--infile', help='WAV file to read from', required=True)
parser.add_argument('-o', '--outfile', help='WAV file to write to', required=True)
parser.add_argument('-s', '--stats', help='Displays some stats', action='store_true')
parser.add_argument('-t', '--timespace', help='sample spacing, default 34', type=int, default=34)

args = vars(parser.parse_args())

inFile = args['infile']
outFile = args['outfile']
# timeSpace is the number of samples between changes
timeSpace = args['timespace']

if  os.path.isfile(inFile) == False:
	print "Please give a file to process."
	exit(0)

(sampFreq, snd) = wavfile.read(inFile)
snd = snd / (2.**15) # convert to -1 to 1 

state = 0
statecount = 0
binsection = 0
binfull = ""
for x in range(0, len(snd)):
	statecount = statecount + 1
	# working with one channel only as it lets us see the original plus altered at same time
	# pull it down a bit as is hovering a bit too close to 0, should be a better way?
	snd[x][1] = snd[x][1]-.1
	if snd[x][1] > 0:
		snd[x][1] = 1
		cstate = 1
	else: 
		snd[x][1] = -1
		cstate = 0
	if cstate != state:
		if args['stats']:
			statediv = (statecount / timeSpace) # work out the number of samples that fit in to the statecount
			print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount, "possible count", statediv
			binsection = str(state) * statediv 
#			print binsection		
			binfull += binsection
		state = cstate
		statecount = 0

if args['stats']:
	print "The whole lot: " + binfull

print 'Writing to: ' + outFile
wavfile.write(outFile, sampFreq, snd)

