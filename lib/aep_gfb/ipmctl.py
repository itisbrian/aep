# all ipmctl-specific commands get dropped in here

from pggenericpy.generic import *
from generic import *
from ndctl import *
import copy
import re
import sys
import os
import time

import pprint

#This splits the output into separate segments based on
#The current output formatting of ipmctl
def parseAllEntry(dataIn):
	def ltoDict(line):
		lineP = line.replace('-','').strip().split("=")
		if len(lineP) != 2:
			return None
		return { lineP[0]: lineP[1] }

	def mergeTwoDicts(a, b):
		out = a.copy()
		out.update(b)
		return out

	output = []
	outputEntry = []
	for line in dataIn:
		if not len(line.strip()) or ( line.startswith("---") and len(outputEntry) > 0): #If the line is empty
			if not len(outputEntry): #And we have nothing in output
				continue

			else:
				outD = {}
				for entry in outputEntry:
					outD = mergeTwoDicts(outD, entry)

				output.append(copy.copy(outD))

				#Deref everything
				outD = None
				outputEntry = None

				#Re-instance the list
				outputEntry = []

		else:
			lout = copy.copy(ltoDict(line) )
			if lout:
				outputEntry.append(copy.copy(lout))

	if len(outputEntry) > 0:
		outD = {}
		for entry in outputEntry:
			outD = mergeTwoDicts(outD, entry)
		output.append(copy.copy(outD))

	return output

# Enable ses feature on nvdimm
def lockPmem(dimmid, passcode):
	pass

# Unlock nvdimm that's locked
def unlockPmem(dimmid, passcode):
	pass

diagnostic_list = [ "Quick", "Config", "Security", "FW" ]

def diagnostic(dimmid, diag):
	wlprint("Executing ipmctl diagnostic %s against dimm %s" % (diag ,dimmid) )

	if diag not in diagnostic_list:
		wlprint("ERROR: Unknown diagnostic called: %s" % diag)
		return -1

	retd = getProcAll([ "/usr/bin/ipmctl", "start", "-diagnostic", diag, "-dimm", dimmid])
	if retd['ret'] != 0:
		wlprint("ERROR: Failed to execute ipmctl start -diagnostic")
		return -2

	wlprint("ipmctl output:")
	stateinfo = None
	for line in retd['data']:
		if len(line.strip()) == 0:
			continue

		wlprint("\t%s" % line.strip())

		if line.strip().startswith("State"):
			stateinfo = line.strip().split(":")[1].strip()

	#Here's where we look at the state and return such things.
	if stateinfo == "Ok":
		return None

	return stateinfo

#Get all info out of a dimmid
def getDIMMDetail(dimmid):
	pass

#Get all dimms
def getDIMMs():
	retd = getProcAll(["/usr/bin/ipmctl", "show", "-dimm"])
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return code when attempting to show dimms [%s]" % str(retd['ret']) )
		return -1

	#Newest IPMCTL uses `|` delimiters
	dimml_re = re.compile("^(0x[0-9A-Fa-f]{4})\s+(\S+)\s+([MGT])iB\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$")

	output = {}
	for line in retd['data']:
#		print("Line: %s" % line)
		dimml_s = dimml_re.search(line)
		if not dimml_s:
			lineSpl = line.split("|")
			if len(lineSpl) != 6:
				continue

			if lineSpl[0].strip().startswith("DimmID"):
				continue

			data = {
				'id':lineSpl[0].strip(),
				'capacity':lineSpl[1].strip().split(" ")[0],
				'capacityU':str(lineSpl[1].strip().split(" ")[1])[0],
				'health':lineSpl[2].strip(),
				'action':lineSpl[3].strip(),
				'lock':lineSpl[4].strip(),
				'fw':lineSpl[5].strip(),
			}

			output[lineSpl[0].strip()] = copy.copy(data)
			data = None
			continue

		data = {
			'id':dimml_s.group(1),
			'capacity':dimml_s.group(2),
			'capacityU':dimml_s.group(3),
			'health':dimml_s.group(4),
			'action':dimml_s.group(5),
			'lock':dimml_s.group(6),
			'fw':dimml_s.group(7),
		}

		output[dimml_s.group(1)] = copy.copy(data)
		data = None

	return output

#Get all info from a cpuid
def getCPUDetail(cpu):
	pass

#Get CPU socket info
def getCPUs():
	retd = getProcAll(["/usr/bin/ipmctl", "show", "-socket"])
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return code when attempting to show sockets [%s]" % str(retd['ret']) )
		return -1

	socketl_re = re.compile("^(0x[0-9A-Fa-f]{4})\s+(\S+)\s+([MGT])iB\s+(\S+)\s+([MGT])iB")

	output = {}
	for line in retd['data']:
		socketl_s = socketl_re.search(line)
		if not socketl_s:
			continue

		data = {
			'id':socketl_s.group(1),
			'mmlimit':socketl_s.group(2),
			'mmlimitU':socketl_s.group(3),
			'mm':socketl_s.group(4),
			'mmU':socketl_s.group(5),
		}

		output[socketl_s.group(1)] = copy.copy(data)
		data = None

	return output

#Return specific region information
def getRegionDetails(isetid=None):
	cmd = ["/usr/bin/ipmctl", "show", "-all", "-region"]
	if isetid:
		cmd.append(isetid)


	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Bad return when executing '%s' for getRegionDetails" % str(cmd) )
		sys.exit(-1)

	data = parseAllEntry(retd['data'])

	if not data:
		wlprint("WARNING: GetRegionDetails called, but no regions found")

	return data

#Return region information
def getRegion(cpu=None):
	return getRegionDetails(None)


def compareRegionToGoal(goalp, interleaved=False):
	regionData = getRegionDetails()
	dimmData = getDIMMs()
	mismatchedDimms = []
	dimmRegionRatios = {}
	if interleaved:
		#We're not implementing the interleaved stuff now; just the noninterleaved
		pass

	else:
		#This is a really bad N^2 design
		for dimm in dimmData:
			for region in regionData:
				if dimm == region['DimmID']:
					if dimm in dimmRegionRatios:
						wlprint("WARNING: Duplicate entry for dimm %s found in regions; will caused skewed calculation." % dimm)

					regionCapB = str(region['Capacity']).split(" ")
					regionCapS = float(regionCapB[0])
					dimmCapS = float(dimmData[dimm]['capacity'])
					regionCapSU = regionCapB[1][0]
					if regionCapSU != dimmData[dimm]['capacityU']:
						wlprint("ERROR: Incorrect capacity units; mismatch.")
						return -1

					dimmRegionPercent = (1.0 - (regionCapS/dimmCapS) ) * 100.0
					wlprint("Got region ratio for dimm %s of %f" % (dimm, dimmRegionPercent))
					dimmRegionRatios[dimm] = dimmRegionPercent

					if (dimmRegionPercent < (goalp - 9)) and ((goalp + 9) < dimmRegionPercent):
						mismatchedDimms.append(dimm)

	#This is for error posting in a unified way.
	for dimm in mismatchedDimms:
		wlprint("ERROR: DIMM Ratio mismatch for %s - %f" % (dimm, dimmRegionRatios[dimm]))

	return len(mismatchedDimms)


#Get detailed goal info for a dimm
def getGoalDetails(cpu=None):
	cmd = ["/usr/bin/ipmctl", "show", "-all", "-goal"]
	if cpu:
		cmd.append("-socket")
		cmd.append(cpu)

	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Bad return when executing `%s` for getGoalDetails" % str(cmd) )
		sys.exit(-1)

	data = parseAllEntry(retd['data'])
	if not data:
		wlprint("WARNING: GetGoalDetails called, but no goals found")

	return data

#Get simple goal data for a dimm
def getGoal(cpu=None):
	cmd = ["/usr/bin/ipmctl", "show", "-goal"]
	if cpu:
		cmd.append("-socket")
		cmd.append(cpu)

	retd = getProcAll(cmd)

	if retd['ret'] != 0:
		wlprint("ERROR: Bad return when executing `%s` for getGoal" % str(cmd) )
		#This should not die under any circumstance, and we can't return codes.  Die.
		sys.exit(-1)

	goall_re = re.compile("^(0x[0-9A-Fa-f]{4})\s+(0x[0-9A-Fa-f]{4})\s+(\S+)\s+([MGT])iB\s+(\S+)\s+([MGT])iB\s+(\S+)\s+([MGT])iB")

	output = {}
	for line in retd['data']:
		goall_s = goall_re.search(line)
		if not goall_s:
			continue

		data = {
			'socket':goall_s.group(1),
			'dimm':goall_s.group(2),
			'msz':goall_s.group(3),
			'mszU':goall_s.group(4),

			'appd1sz':goall_s.group(5),
			'appd1szU':goall_s.group(6),

			'appd2sz':goall_s.group(7),
			'appd2szU':goall_s.group(8),

			#OK, this entry is a bit of math... hopefully it's correct when I actually assign it.
			'perc':None
		}
		#I only do the math for percentage if I know all of the units are consistent.
		if data['appd1szU'] == data['appd2szU'] and data['appd1szU'] == data['mszU']:
			data['perc'] = str( int ( ( float(data['msz']) / ( float(data['appd1sz']) + float(data['appd2sz']) + float(data['msz']) ) ) * 100 ) )

		#Goals are per-socket, but we want per-dimm savings.  We can do multiple refs inside later.
		if goall_s.group(1) not in output:
			output[goall_s.group(1)] = {}

		output[goall_s.group(1)][goall_s.group(2)] = copy.copy(data)
		data = None

	return output


#Clear goal for a CPU socket or all
def clearGoal(cpu=None, reboot=False, ignore=False):
	cmd = ["/usr/bin/ipmctl", "delete", "-goal"]
	if cpu:
		cmd.append("-socket")
		cmd.append(cpu)

	#This command will not return nonzero if there is no goal config; so it'll only give
	# bad returns if it's malformed.

	retd = getProcRC(cmd)
	if retd != 0:
		if not ignore:
			wlprint("ERROR: Bad return when executing `%s` for clearGoal" % str(cmd) )

	if reboot:
		rebootSystem(10)

	return retd

#Set goal for a CPU socket or all
def setGoal(perc, mode=None, cpu=None, reboot=False):
	cmd = ["/usr/bin/ipmctl", "create", "-force", "-goal"]
	cmdEnd = "memorymode=%s" % str(perc)

	if cpu:
		cmd.append("-socket")
		cmd.append(cpu)

	cmd.append(cmdEnd)

	if mode:
		cmd.append("PersistentMemoryType=%s" % mode)

	retd = getProcRC(cmd)

	if retd != 0:
		wlprint("ERROR: Bad return when executing `%s` for setGoal" % str(cmd) )

	if reboot:
		rebootSystem(10)

	return retd

#Clearing the configuration is a 2 step process.
def clearConfig():
	if delete_all():
		wlprint("ERROR: Bad return from delete_all() in clearConfig()")
		return -1

	if setGoal(100):
		wlprint("ERROR: Bad return from setGoal() in clearConfig()")
		return -2

	rebootSystem(10)
	return 0

#def clearConfig_step2():
#	pass