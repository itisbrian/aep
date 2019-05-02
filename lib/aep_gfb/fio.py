#FIO-specific functions for AEP dimms
from generic import *
import pprint
import os
import sys

#Get NUMA Node of pmem device
def getPmemNode(pmemdev):
	pmem_mdev = pmemdev.replace('/dev/', '')
	nnode = None
	try:
		with open("/sys/block/%s/device/numa_node" % pmem_mdev, 'r') as iFD:
			nnode = int(iFD.readline().strip())
	except:
		generic.wlprint("ERROR: Could not open numa_node for `%s`" % pmemdev)

	return nnode

#Execute FIO with json output; iops and throughput only.
# Latency later maybe down the road.
#
# Return a json of the output
def fioExecute(jobfile):
	pass

# Create a simple jobfile based on simple input data
def genFio(pmemdev, oFile, append=False):
	pass


#These should be untouched globals so we always know how to find them
FIORunFile="/tmp/test.fiojob"
FIOOutFile="/tmp/test.fioout"



def formulateResults(fioJsonOut):
	results = None
	try:
		with open(fioJsonOut, 'r') as iFD:
			results = json.loads(iFD.read())

	except:
		wlprint("ERROR: Could not load json file %s" % fioJsonOut)

	output = {
		'totals':{
			'read':0,
			'readio':0,
			'write':0,
			'writeio':0,
		},
		'disk':{},
	}

	for entry in results['jobs']:
		# print("Entry for formulateResults")
		# pprint.pprint(entry)
		if entry['jobname'] not in  output['disk']:
			output['disk'][entry['jobname']] = {
				'read':0,
				'readio':0,
				'write':0,
				'writeio':0,
			}

		#BW entries are in bytes; we'll keep them as-is initially.
		output['disk'][entry['jobname']]['read'] += entry['read']['bw_bytes']
		output['disk'][entry['jobname']]['write'] += entry['write']['bw_bytes']

		output['disk'][entry['jobname']]['readio'] += entry['read']['iops']
		output['disk'][entry['jobname']]['writeio'] += entry['write']['iops']

		output['totals']['read'] += entry['read']['bw_bytes']
		output['totals']['write'] += entry['write']['bw_bytes']
		output['totals']['readio'] += entry['read']['iops']
		output['totals']['writeio'] += entry['write']['iops']

	return output

#This expects results from formulateResults.
# bwInData should be a 4 value dict
def validateResults(inData, jsonIn):
	perDisk = {}

	for entry in inData:
		if inData[entry] != -1:
			perDisk[entry] = inData[entry]/len(jsonIn['disk'])

	errors = []
	warnings = []
	for entry in jsonIn['disk']:
		for value in perDisk:
			if jsonIn['disk'][entry][value] < (perDisk[value] - (perDisk[value]*0.1) ):
				errors.append("ERROR: %s is outside of perDisk value for %s (%s) with data: %s" % (entry, value, str(perDisk[value]), str(jsonIn['disk'][entry][value]))) 
			elif jsonIn['disk'][entry][value] > (perDisk[value] + (perDisk[value]*0.1)):
				warnings.append("WARNING: %s is outside of perDisk value for %s (%s) with data: %s" % (entry, value, str(perDisk[value]), str(jsonIn['disk'][entry][value]))) 

	if len(errors):
		wlprint("ERRORS Occurred during validateResults:")
		for entry in errors:
			wlprint(entry)

	for entry in warnings:
		wlprint(entry)

	return len(errors)

#Indata formatter for validateresults
def validateResultsInData(readbw=-1, readio=-1, writebw=-1, writeio=-1):
	return {
		"read":readbw,
		"write":writebw,
		"readio":readio,
		"writeio":writeio,
	}

# Create a simple jobfile based on pmem name, then execute it.
# pmemdev should be a list
# outputAppend changes the output file to be concat'd with outputAppend
def quickFio(pmemdev, rwmode="write", directory=None, single=False, outputAppend=""):
	data = [
		"[global]",
		"direct=1",
		"ioengine=libaio",
		# "runtime=180",
		"runtime=5",
		"iodepth=1",
		"bs=4M",
		"disable_lat=1",
		"disable_clat=1",
		"disable_slat=1",
		"lat_percentiles=0",
		"clat_percentiles=0",
	]

	if rwmode == "write":
		data.append("numjobs=4")
	elif rwmode == "read":
		data.append("numjobs=12")
	elif rwmode == "rw":
		data.append("numjobs=4")
	elif rwmode == "randwrite":
		data.append("numjobs=4")
	elif rwmode == "randread":
		data.append("numjobs=12")
	elif rwmode == "randrw":
		data.append("numjobs=4")
	else:
		data.append("numjobs=4")

	data.append("rw=%s" % rwmode)

	if not isinstance(pmemdev, list):
		wlprint("ERROR: quickFio() called with non-list pmemdev")
		return -1



	if directory:
		#data.append("fill_fs=1")
		data.append("size=1G")
		if not os.path.exists(directory):
			os.mkdir(directory)

		if not os.path.isdir(directory):
			wlprint("ERROR: quickFio() directory is not a directory `%s`" % directory)
			sys.exit(-1)
	else:
		data.append("fill_device=1")

	data.append(" ")

	with open(FIORunFile, "w+") as oFD:
		for line in data:
			oFD.write("%s\n" % line)

	for entry in pmemdev:
		pmemn = entry.split("/")[-1]

		numanode = getPmemNumaNode(entry)
		with open(FIORunFile, "a+") as oFD:

			oFD.write("[%s]\n" % pmemn)
			if single == True:
				oFD.write("stonewall\n")

			oFD.write("numa_cpu_nodes=%s\n" % numanode)

			if directory:
				#Purge and recreate the directory
				if os.path.exists("%s/%s" % (directory, pmemn)):
					shutil.rmtree("%s/%s" % (directory, pmemn))

				os.mkdir("%s/%s" % (directory, pmemn))

				# oFD.write("size=1G\n")
				oFD.write("directory=%s\n" % directory)
				# oFD.write("filename=%s_io\n\n" % pmemn)

			else:
				oFD.write("filename=%s\n\n" % entry)

			

	fioData = getProcRC(["/usr/local/bin/fio", FIORunFile, "--output-format=json", "--output=%s" % str(FIOOutFile + str(outputAppend)) ])
	if fioData:
		wlprint("ERROR: quickFio() fio got bad return code %d" % fioData)
		return 3

	return 0

#Not in use yet
# Create a detailed jobfile based on complex input data.
# All negative numbers mean the argument gets purged
def genFioD(pmemdev, oFile, bs, iodepth, ioengine, append=False):
	pass

#Not in use yet
fioCPArgs = {
	'bs':['4k','8k','64k','128k','256k','1m','2m','4m','8m'],
	'iodepth':[1,2,4,8,16,32,64,128,256,512],
	'numjobs':[1,2,4,8,16,20,24],
	'rw':['read','write','rw','randread','randwrite','randrw'],
	'rwmixread':[5,10,30,50,70,90,95],
	'ioengine':['sync','libaio'],
}

#Not in use yet
# Create cartesian product jobfile with a predetermined set of arguments
def genFioCP(pmemdev, oFile):
	pass


# Write with FIO until the disk is full
# Return fioExecute output
def writeSingleFile(disk, mountp):
	pass
