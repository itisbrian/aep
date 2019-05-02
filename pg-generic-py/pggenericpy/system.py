from __future__ import print_function

import re
import glob
import os

from pggenericpy.generic import *

#
# These are system detection methods that are super-commonly used by me to
# determine what platform I'm running on, as well as different hardware
# population info.
#

#
# Some of the core smFioTools stuff needs to be imported as part of this lib
#

#
# Standing lib requirements (Since I didn't wanna re-write everything):
# 	- python-hwinfo [See gitlab.bnet
#
from hwinfo.host.dmidecode import *

# Global defs
dmidecode = "/usr/sbin/dmidecode"

validPlatformOut = [
	'X8S',
	'X8D',
	'X9S',
	'X9D',
	'X9Q',
	'X10S',
	'X10D',
	'X10Q',
	'X10O',
	'X11S',
	'X11D',
	'X11Q',
	'X11O',
	'P8D',
	'P9D',

	#I'm sure I'm missing all the AMD and whatever else.  Figger it out later.
]

# This returns a simple string based on motherboard naming conventions
def smciGetPlatform():
	#Performs a simple split to dictionary so that we have 3 string pieces without a need for manipulation
	def splitPlatform(instr):
		parseD = {
			'class':re.compile("^([a-zA-Z]+)\d"),
			'ver':re.compile("^[a-zA-Z]+(\d+)[a-zA-Z]+$"),
			'socketi':re.compile("^[a-zA-Z]+\d+([a-zA-Z]+)$"),
		}
		out = {
			'full':instr,
		}

		for entry in parseD:
			parseS = None #This clear is probaby not necessary.
			parseS = parseD[entry].search(instr)
			if not parseS:
				continue

			out[entry] = str(parseS.group(1))

		return out

	dmiDecodeRaw = getProcAll(dmidecode)
	if dmiDecodeRaw['ret'] != 0:
		print("ERROR: dmidecode execution failed with return code %d" % dmiDecodeRaw['ret'])
		return -1

	#Prepare textblock:
	dmiDecodeTB = "".join(dmiDecodeRaw['data'])

	parser = DmidecodeParser(dmiDecodeTB)

	dmiOut = parser.parse()

	#Debugging noise.
	print(parser.parse())

	#In order we want to try product_manuf (Base Board), system_manuf (System) and then if those fail, we attempt to get fru.

	#We /might/ want to check out vendor/manuf names just to slim things down; but I think it's easier this way.
	for entry in validPlatformOut:
		if 'product_name' in dmiOut and dmiOut['product_name'].startswith(entry):
			return splitPlatform(entry)

		if 'system_product_name' in dmiOut and dmiOut['system_product_name'].startswith(entry):
			return splitPlatform(entry)

	#Try fru data

	#Return empty block
	return None

#This gives us a dictionary with all packages (via numa nodes; so if interleaving is enabled this will break) and their cores and each of the threadid's the cores get assigned to.
def getPackageCoreThreadDict():
	sysfs_cpu = "/sys/bus/cpu/devices/"
	out = {}
	for cpudir in glob.glob("%scpu*" % sysfs_cpu):
		if os.path.exists("%s/topology" % (cpudir) ):
			package = None
			coreid = None
			threadid = None
			logicalid = int(re.sub("cpu", '', cpudir.split("/")[-1]))
			#Get the package id
			try:
				with open("%s/topology/physical_package_id" % (cpudir)) as iFD:
					package = int(iFD.readline().strip())
			except:
				print("ERROR: Unable to read physical package id for %s" % cpudir)
				return -1

			try:
				with open("%s/topology/core_id" % (cpudir)) as iFD:
					coreid = int(iFD.readline().strip())
			except:
				print("ERROR: Unable to read coreid for %s" % cpudir)
				return -2

			# try:
			if True:
				with open("%s/topology/thread_siblings_list" % (cpudir)) as iFD:
					siblings_arr = map(str.strip, iFD.readline().strip().split(","))
					threadid = int(siblings_arr.index(str(logicalid)))
			# except:
			else:
				print("ERROR: Unable to read thread siblings for %s" % cpudir)
				return -3

			if package not in out:
				out[package] = {}

			if coreid not in out[package]:
				out[package][coreid] = {}

			if threadid not in out[package][coreid]:
				out[package][coreid][threadid] = logicalid

	return out



