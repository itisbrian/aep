# We have some non-specific-to-green-fireball functions.  I'm dropping them in here.

import os
import sys
import json
import time

from config import *

from pggenericpy.generic import *

#global LOGFILE
#LOGFILE="log.testg"

def writeLogPrint(file, stringi):
	print(stringi)
	try:
		with open(file, 'a+') as oFD:
			oFD.write("%s\n" % stringi)
	except:
		print("ERROR: writeLogPrint could not open `%s`" % file)
		return -1

	return 0


def wlprint(stringi):
#	global LOGFILE
	LOGFILE = os.environ['LOGFILE']

	if writeLogPrint(LOGFILE, stringi):
		sys.exit(1)


def shaFile(filename, blksz=65536):
	import hashlib as hash
	sha = hash.sha256()

	try:
		with open(filename, 'rb') as iFD:
			fbuf = iFD.read(blksz)
			while len(fbuf) > 0:
				sha.update(fbuf)
				fbuf = iFD.read(blksz)
	except:
		wlprint("ERROR: shaFile() Issue handling file operations for %s" % str(filename) )
		sys.exit(-1)

	return sha.hexdigest()

#Create a directory if it doesn't exit
def lmkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)
		return 0

	if os.path.isdir(path):
		return 0

	return -1

def rebootSystem(delay=0):
	wlprint("....Rebooting system....")
	time.sleep(delay)
	getProcRC(["/usr/sbin/reboot"])
	sys.exit(0)

def createGPTLabel(blockdev):
	wlprint("createGPTLabel on %s" % blockdev)
	if getProcRC(["/usr/sbin/parted", "-s", blockdev, "mklabel", "gpt"]):
		wlprint("ERROR: Bad return code when creating label.")
		return -1
	return 0

def createGPTPartition(blockdev, offsetPerc, sizePerc):
	wlprint("createGPTPartition on %s from %d -> %s" % (blockdev, offsetPerc, sizePerc) )
	if getProcRC(["/usr/sbin/parted", "-s", blockdev, "mkpart", "data", "xfs", "%d%%" % offsetPerc, "%d%%" % sizePerc]):
		wlprint("ERROR: Bad return code when creating partition.")
		return -1
	return 0

fs_cmd = {
	'xfs':{
		'cmd':"/usr/sbin/mkfs.xfs",
		'flags':[ '-f', ],
	},
	'btrfs':{
		'cmd': "/usr/sbin/mkfs.btrfs",
		'flags':[ '-f', ],
	},
	'ext4':{
		'cmd': "/usr/sbin/mkfs.ext4",
		'flags':[ '-F', ],
	},
}

def mkfsd(filesystem, device):
	cmd = [ fs_cmd[filesystem]['cmd'] ] + fs_cmd[filesystem]['flags'] + [ device ]

	timelimit = 30

	while not os.path.exists(device) and timelimit > 0:
		time.sleep(1)
		timelimit = timelimit - 1

	if timelimit <= 0:
		wlprint("ERROR: mkfsd failed because the device '%s' never went online." % str(device))
		return -3

	#Super half-assed 3 attempt work hackjob
	retd = getProcRC(cmd)
	if retd:
		time.sleep(10)
		retd = getProcRC(cmd)
		if retd:
			time.sleep(10)
			retd = getProcRC(cmd)
			if retd:
				wlprint("ERROR: mkfsd failed with code %d with command %s" % (retd, str(cmd) ) )
				return -2
	return 0

def mkfs(filesystem, device, partid):
	#We'll be dealing with specific devices, not complete paths to partition id's
	if not os.path.exists("%sp%d" % (device, partid) ):
		wlprint("ERROR: mkfs cannot find partition %d on %s" % (partid, device) )
		return -1

	bdev_p = "%sp%d" % (device, partid)

	return mkfsd(filesystem, bdev_p)

#Determine if a blockdevice is mounted
def isMounted(blockdev):
	mounted  = False
	with open("/proc/mounts") as iFD:
		for line in iFD.readlines:
			if blockdev in line:
				mounted = True
				break

	return mounted

def mountpointInUse(mountpoint):
	mounted  = False
	with open("/proc/mounts") as iFD:
		for line in iFD.readlines:
			if mountpoint in line:
				mounted = True
				break

	return mounted

def unmount(blockdev):
	if getProcRC([ '/usr/bin/umount', '-f', blockdev ]):
		wlprint("ERROR: umount failed in unmount on %s" % blockdev)
		return -1

	return 0

def waitForUnmount(blockdev):
	limit = 180 #3 minute wait time
	curtime = 0

	if unmount(blockdev):
		wlprint("ERROR: waitForUnmount failed because unmounting failed on %s" % blockdev)
		return -1

	while limit > curtime:
		if not isMounted(blockdev):
			return 0

		time.sleep(1)

	wlprint("ERROR: waitForUnmount timed out on %s" % blockdev)
	return 1

def mountDiskD(blockdev, mountpoint):
	if getProcRC(["/usr/bin/mount", blockdev, mountpoint]):
		wlprint("ERROR: Could not mount blockdevice.")
		return -1
	return 0

def mountDisk(blockdev, part, mountpoint):
	#Ensure mountpoint is not already mounted
	wlprint("mountDisk on %s, %d, to %s" % (blockdev, part, mountpoint) )

	if isMounted(blockdev):
		wlprint("ERROR: Disk is currently mounted and we did not mount it.")
		sys.exit(-1)

	if mountpointInUse(mountpoint):
		wlprint("ERROR: Mountpoint is currently in-use.")
		sys.exit(-2)


	#Perform getProcRC against mount
	if getProcRC(["/usr/bin/mount", "%sp%d" % (blockdev, part), mountpoint]):
		wlprint("ERROR: Could not mount blockdevice.")
		sys.exit(-3)

	return None

def flushCache():
	if getProcRC(["/usr/bin/sync"]):
		wlprint("ERROR: flushCache failed sync")
		return -1

	try:
		with open("/proc/sys/vm/drop_caches", "w") as oFD:
			oFD.write("3\n")
	except:
		wlprint("ERROR: flushCache failed to drop caches")
		return -2

	return 0

testOrder = [
	'initialization',
	'diagnostics',

	'gval_50p',
	'perfTest_50p',
	'partTest_50p',
	'goal_clear_50p',

# #0% memory tests [all storage]
	'goal_0p',
	'gval_0p',
	'perfTest_0p',
	'partTest_0p',
	'goal_clear_0p',

# 25% memory tests
	'goal_25p',
	'gval_25p',
	'perfTest_25p',
	'partTest_25p',
	'goal_clear_25p',

# 75% memory tests
	'goal_75p',
	'gval_75p',
	'perfTest_75p',
	'partTest_75p',
	'goal_clear_75p',

# #100% memory tests
	# 'goal_100p',
# 	'gval_100p',

# #25% memory tests
# 	'goal_25p',
# 	'gval_25p',

]

testOrderPower = [
	'initialization',
	'gval_0p',
]

#Return the configuration intialization dict
def initConfig():
	config = {
		'current':None,
		'completed':[],
		'remaining':[],
		'tests':['initialization', 'diagnostics', ], # 'ratio', 'partitioning', 'secerase'],
		'tests':testOrder,
		'state':None,
		'dimms':None,
		'sockets':None,
		'goal':None,
		'regions':None,
	}
	return config

def initConfigPowertest():
	config = {
		'current':None,
		'completed':[],
		'remaining':[],
		'tests':['initialization', 'diagnostics', ], # 'ratio', 'partitioning', 'secerase'],
		'tests':testOrderPower,
		'state':None,
		'dimms':None,
		'sockets':None,
		'goal':None,
		'regions':None,
		'psus':None,
	}
	return config

def nextTest(config):
	config['completed'].append(config['current'])
	try:
		config['current'] = config['remaining'].pop(0)
	except:
		config['current'] = None
		return config
	return config

#Get the configuration
def getConfig(configFile):
	out = None
	if not os.path.exists(configFile):
		return out

	with open(configFile) as iFD:
		try:
			out = json.load(iFD)
		except:
			wlprint("ERROR: Could not load config.")
			return None
	return out

#Write the config
def writeConfig(config, configFile):
	with open(configFile, "w") as oFD:
		try:
			json.dump(config, oFD)
		except:
			wlprint("ERROR: Could not save config.")
			return -1
	return None


def getPmemNumaNode(pmemdev):
	pmemn = pmemdev.split("/")[-1]
	#/sys/block/${pmemn}/device/numa_node

	if pmemn.endswith("p1") or pmemn.endswith("p2") or pmemn.endswith("p3") or pmemn.endswith("p4"):
		pmemn = pmemn[:-2]

	pmemnnp = "/sys/block/%s/device/numa_node" % pmemn
	if not os.path.exists(pmemnnp):
		wlprint("ERROR: getPmemNumaNode could not open numa_node file.")
		return -2

	with open(pmemnnp, 'r') as iFD:
		nodeString = iFD.readline().strip()

	try:
		nodeI = int(nodeString)
	except:
		wlprint("ERROR: Could not convert nodestring `%s` to int." % nodeString)
		return -3

	if nodeI == -1:
		return 0

	return nodeI