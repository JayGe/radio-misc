#!/usr/bin/env python
# script for controlling the power switches with rfcat

from rflib import *
import argparse

button = {'01': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x22\x8a\x8a\x20',
	'00': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x28\xa2\x28\xa0',
	'11': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x22\xaa\x22\x20',
	'10': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x28\x88\x8a\xa0',
	'21': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x28\xa8\xa2\x20',
	'20': '\xaf\xe0\x22\x2a\x8a\x28\xaa\x2a\xa2\x22\x8a\x28\x88\xa2\x22\x88\xa2\xa0'}

parser = argparse.ArgumentParser(description="Turns power switches on or off with rfcat")

parser.add_argument('-b', '--button', help='Button number|state eg: 00 01 10 11 20 21', required=True)
parser.add_argument('-r', '--retransmit', help='Retransmit times', nargs='?', const=10, type=int)
parser.add_argument('-f', '--frequency', help='Frequency', nargs='?', const=433805000, type=int)
parser.set_defaults(frequency=433805000, retransmit=10)
args = vars(parser.parse_args())

freq = args['frequency']
butt = args['button']
retr = args['retransmit']

signal = button[butt]
d = RfCat()

d.setMdmModulation(MOD_ASK_OOK)
d.setFreq(freq)
d.setMaxPower()
d.setMdmSyncMode(0)
d.setMdmDRate((int)(1.0/0.000450))

for i in range(1, retr):
	d.RFxmit(signal)
	d.setModeIDLE()

