#!/usr/bin/env python
# JayGe - script to do some counting
# add channel option 

import argparse
import os.path
from scipy.io import wavfile

parser = argparse.ArgumentParser(description="Takes a wav file and does some counting")

parser.add_argument('-i', '--infile', help='WAV file to read from', required=True)
parser.add_argument('-s', '--stats', help='print basic stats', action='store_true')
parser.add_argument('-t', '--timespace', help='sample spacing for estimating counts length (34)', nargs='?', const=34, type=int)
parser.add_argument('-c', '--channel', help='channel 0 or 1, 0 default', nargs='?', const=0, type=int)

args = vars(parser.parse_args())

inFile = args['infile']
# timeSpace is the number of samples between changes
timeSpace = args['timespace']
channel = args['channel']

if os.path.isfile(inFile) == False:
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
	if snd[x][channel] > 0:
		cstate = 1
	else: 
		cstate = 0
	if cstate != state: # If there is a state change
		if args['stats']:
			if args['timespace']: # if timespace provided try to guess count
				statediv = (statecount / timeSpace) # work out the number of samples that fit in to the statecount
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount, "possible count", statediv
				binsection = str(state) * statediv # guessed number of 1/0
			else:
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount
				binsection = str(state) # number of 1/0 

			binfull += binsection # add to basic ook tracker

		state = cstate # change the state tracker to the current state 
		statecount = 0 # reset the statecounter

if args['stats']:
	print "The whole lot:", binfull

