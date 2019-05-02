from __future__ import print_function

from pggenericpy.generic import *

def getBMCLan():
	lanOut = getProcAll(['ipmitool', 'lan', 'print'])

	if lanOut['ret'] != 0:
		print("ERROR: Bad return code from `ipmitool lan print`: %d" % lanOut['ret'])
		return None

	out = {}

	for entry in lanOut['data']:
		if entry.startswith("IP Address"):
			rdata = entry.split(":")
			out[rdata[0].strip()] = rdata[1].strip()
	return out
