#!/usr/bin/env python
# JayGe - script to do some counting without manipulating

import argparse
import os.path
from scipy.io import wavfile

parser = argparse.ArgumentParser(description="Takes a wav file and does some counting")

parser.add_argument('-i', '--infile', help='WAV file to read from', required=True)
parser.add_argument('-s', '--stats', help='print basic stats', action='store_true')
parser.add_argument('-m', '--manc', help='print manchester guess', action='store_true')
parser.add_argument('-t', '--timespace', help='sample spacing for estimating counts or manc spacing, default 34', nargs='?', const=34, type=int)
parser.add_argument('-o', '--offset', help='manchester encoding offset, default 10', nargs='?', const=10, type=int)
parser.add_argument('-c', '--channel', help='channel 0 or 1, default 0', nargs='?', const=0, choices=[0,1], type=int)
parser.set_defaults(channel=0, offset=10, timespace=34)

args = vars(parser.parse_args())

inFile = args['infile']
# timeSpace is the number of samples between changes
timeSpace = args['timespace']
channel = args['channel']
offset = args['offset']

if os.path.isfile(inFile) == False:
	print "Please give a file to process."
	exit(0)

(sampFreq, snd) = wavfile.read(inFile)
snd = snd / (2.**15) # convert to -1 to 1 

state = 0
statecount = 0
binfull = ""

if args['manc']:
	print "MAND"

for x in range(0, len(snd)):
	statecount = statecount + 1
	if snd[x][channel] > 0:
		cstate = 1
	else: 
		cstate = 0
	if cstate != state: # If there is a state change
		if args['stats']:
			if args['manc']: # give best guess for manchester encoding, requires a fairly clean file so timings are okay
				print "MANC", offset, timeSpace

			elif args['timespace']: # if timespace provided try to guess count
				statediv = (statecount / timeSpace) # work out the number of samples that fit in to the statecount
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount, "possible count", statediv
				binfull += str(state) * statediv # guessed number of 1/0

			else: # just prints the switches where they happen without sample guess, will always be 101010...
				print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount
				binfull += str(state) # number of 1/0 

		state = cstate # change the state tracker to the current state 
		statecount = 0 # reset the statecounter

if args['stats']:
	print "The whole lot:", binfull

