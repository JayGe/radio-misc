#!/usr/bin/env python
# JayGe - script to do some counting without manipulating
# fix odd length string 

import argparse
import os.path
import sys
from scipy.io import wavfile

parser = argparse.ArgumentParser(description="Takes a wav file and does some counting")

parser.add_argument('-i', '--infile', help='WAV file to read from', required=True)
parser.add_argument('-m', '--manc', help='print manchester decoding', action='store_true')
parser.add_argument('-t', '--timespace', help='sample spacing for estimating counts, default 34', nargs='?', const=34, type=int)
parser.add_argument('-o', '--offset', help='manchester encoding offset, default 40', nargs='?', const=40, type=int)
parser.add_argument('-b', '--boundary', help='manchester encoding bit boundary, default 40', nargs='?', const=40, type=int)
parser.add_argument('-c', '--channel', help='channel 0 or 1, default 0', nargs='?', const=0, choices=[0,1], type=int)
parser.set_defaults(channel=0, offset=40, timespace=34, boundary=40)

args = vars(parser.parse_args())

inFile = args['infile']
# timeSpace is the number of samples between changes
timeSpace = args['timespace']
channel = args['channel']
offset = args['offset']
boundary = args['boundary']

if os.path.isfile(inFile) == False:
	print "Please give a file to process."
	exit(0)

(sampFreq, snd) = wavfile.read(inFile)
snd = snd / (2.**15) # convert to -1 to 1 

state = 0
statecount = 0
binfull = ""

if args['manc']:
	print "Manchester decoding, channel:", channel, "offset:", offset, "boundary:", boundary
	for x in range(offset,len(snd)-40,boundary):
		if snd[x][channel] > snd[x+boundary-1][channel]:
			binfull += "1"
		else:
			binfull += "0"
	print binfull
	print "ASCII:", ''.join(chr(int(binfull[i:i+8], 2)) for i in xrange(0, len(binfull), 8))

else:
	for x in range(1, len(snd)): # starting at 1, might want to start at 0
		statecount = statecount + 1
		if snd[x][channel] > 0:
			cstate = 1
		else: 
			cstate = 0
		if cstate != state: # If there is a state change
			if args['timespace']: # if timespace provided try to guess count
				statediv = (statecount / timeSpace) # work out the number of samples that fit in to the statecount
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount, "possible count", statediv+1, "=", str(state) * (statediv+1)
				binfull += str(state) * (statediv+1) # guessed number of 1/0 + 1 so no * 0
	
			else: # just prints the switches where they happen without sample guess, will always be 101010...
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount
				binfull += str(state) # number of 1/0 
	
			state = cstate # change the state tracker to the current state 
			statecount = 0 # reset the statecounter

	print "The whole lot:", binfull

