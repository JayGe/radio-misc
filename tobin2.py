#!/usr/bin/env python

import argparse
import os.path
from scipy.io import wavfile

parser=argparse.ArgumentParser(description="Takes a wav file and sets channel 1 to 1 or 0")

parser.add_argument('-i', '--infile', help='WAV file to read from', required=True)
parser.add_argument('-o', '--outfile', help='WAV file to write to', required=True)
parser.add_argument('-s', '--stats', help='Displays some stats', action='store_true')
parser.add_argument('-r', '--resize', help='Resize x channel', action='store_true')
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
wstate = 0
peak = 0.9
trough = -0.9

for x in range(0, len(snd)):
	statecount = statecount + 1
	# working with one channel only [1] as it lets us see the original plus altered at same time
	# pull it down a bit as is hovering a bit too close to 0
	snd[x][1] = snd[x][1]-.1
	# square it off to 0.9/-0.9 so it's clearly visible in editor etc
	if snd[x][1] > 0:
		snd[x][1] = peak
		cstate = 1
	else: 
		snd[x][1] = trough
		cstate = 0
	if cstate != state: # If there is a state change
		if args['stats']:
			statediv = (statecount / timeSpace) # work out the number of samples that fit in to the statecount
			print "State switch at", x , state , "->" , cstate, "samples since last switch", statecount, "possible count", statediv
			binsection = str(state) * statediv # guessed number of 1/0
#			print binsection		
			binfull += binsection # add to basic ook tracker

		if args['resize']:
			if state == 1: # sed peak/trough to be something more readable than 1 0 
				peaktrough = 0.9
			else:
				peaktrough = -0.9
			if statecount > 30: # if the count is ofer 30, set it to 40
				nposition = wstate+40
				for y in range(wstate,nposition):
					snd[y][0] = peaktrough
				print "wstate", wstate, "nposition", nposition, "state", state
			else: # if the count is <=30 set it to 20
				nposition = wstate+20
				for y in range(wstate,nposition):
					snd[y][0] = peaktrough
				print "wstate", wstate, "nposition", nposition, "state", state
			wstate = nposition # set wstate to the last written position

		state = cstate # change the state tracker to the current state 
		statecount = 0 # reset the statecounter

if args['resize']: # just flatten the end of the channel
	if nposition < len(snd):
		for z in range(nposition, len(snd)):
			snd[z][0] = 0

if args['stats']:
	print "The whole lot:", binfull

print 'Writing to: ' + outFile
wavfile.write(outFile, sampFreq, snd)

