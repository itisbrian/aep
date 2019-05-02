# All ndctl-specific commands get dropped into here
from pggenericpy.generic import *
from generic import *

import os
import sys
import json
import copy
import re
import time

from distutils.version import LooseVersion


import pprint


#
# Anything calling this method will need to check for list size.  There can be >1 ns
#
def region_to_namespace(region):
	regionD = list_region_namespace(region=region, namespacen=None)
	if regionD:
		out = []
		for entry in regionD['namespaces']:
			out.append(entry['dev'])

		return out

	return None

def iset_to_namespace(isetid):
	return region_to_namespace(iset_to_regionS(isetid))

def namespace_to_region(namespacen):
	regionD = list_region_namespace(region=None, namespacen=namespacen)
	if regionD:
		return regionD['dev']

	return None

def enable_namespace(namespacen):
	cmd = [ "/usr/bin/ndctl", "enable-namespace", "--force", namespacen ]
	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return from `%s` in enable_namespace" % str(cmd) )
		return -1
	return 0

#Disable a region
def disable_region(region):
	error = False
	print("Disabling region %s" % region)

	regionM = region_to_namespace(region)
	if not regionM:
		regionM = []

	for entry in regionM:
		if not entry:
			continue
		if disable_ns(entry):
			wlprint("ERROR: disable_region failed to disable %s in region %s" % (entry, region) )
			error = True
	if error:
		return -1

	return None

#Delete a region
def destroy_region(region):
	error = False

	print("Destroying region %s" % region)

	regionM = region_to_namespace(region)
	if not regionM:
		regionM = []

	for entry in regionM:
		if not entry:
			continue
		if destroy_ns(entry):
			wlprint("ERROR: disable_region failed to disable %s in region %s" % (entry, region) )
			error = True
	if error:
		return -1

	return None


def destroyf_region(region):
	error = False

	print("Forced Destroying region %s" % region)

	regionM = region_to_namespace(region)
	if not regionM:
		regionM = []

	for entry in regionM:
		if not entry:
			continue
		if destroy_nsf(entry):
			wlprint("ERROR: destroyf_region failed to force destroy %s in region %s" % (entry, region) )
			error = True
	if error:
		return -1

	return None

def delete_region(region, ret_on_error=False):
	# if disable_region(region):
		# wlprint("ERROR: delete_region failed to disable %s" % region)
		# sys.exit(-1)

	if destroyf_region(region):
		if ret_on_error:
			wlprint("ERROR: delete_region failed to destroy %s" % region)
			sys.exit(-2)

	return None

#Delete a region via iset
def delete_iset(isetid):
	regionS = iset_to_regionS(isetid)
	if not regionS:
		wlprint("ERROR: delete_iset Could not find region associated with isetid %s" % isetid)
		return -1

	if delete_region(regionS):
		wlprint("ERROR: delete_iset Could not delete region %s" % regionS)
		return -2

	return None

#Delete all regions
def delete_all(ret_on_error=False):
	for entry in list_region_namespace():
		if delete_region(entry['dev'], ret_on_error):
			if ret_on_error:
				wlprint("ERROR: Could not delete region `%s`" % entry['dev'])
				return -1

	return 0

def enable_all(retIfFail=False):
	for entry in list_namespace():
		out = enable_namespace(entry['dev'])
		if retIfFail and (out != 0):
			wlprint("ERROR: Could not enable namespace `%s`" % entry['dev'])
			return -1

#Translate an iset to a region (string)
def iset_to_regionS(isetid):
	regions = list_region(None)
	if not regions:
		wlprint("WARNING: Got no regions for iset_to_region")
		return None

	for entry in regions:
		if isetid == entry['iset_id']:
			return entry['dev']

def iset_to_region(isetid):
	data = iset_to_regionS(isetid)

	if not data:
		wlprint("WARNING: data empty for iset_to_region `%s`" % isetid)
		return None

	return data.replace("region","")

#ipmctl-shifted region ID return
def iset_to_regionI(isetid):
	data = iset_to_regionS(isetid)
	if not data:
		wlprint("WARNING: data empty for iset_to_region `%s`" % isetid)
		return None

	return str( int(data.replace("region","")) + 1 )


#Create a namespace via region
def create_ns_region(region):
	#They say -f, but they only ever reference --force; not sure if it's valid in the code.
	

	#I reverted this because of a kernel patch;  until the patch is integrated this should not run without align.
	cmd = [ "/usr/bin/ndctl", "create-namespace", "--force", "-r", region ]

	#Compare complete string; good kernel should be "4.18.18-148.fc28.x86_64"
	if (os.uname()[2] != "4.18.18-148.fc28.x86_64") and ( LooseVersion(os.uname()[2]) < LooseVersion("4.20") ):
		cmd.append("--align=1G")

	print("Calling create namespace with: '%s'" % str(cmd))
	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return from `%s` in create_ns_region" % str(cmd) )
		return {}

	return retd['data']


#Create a namespace via a region id
def create_ns_iset(isetid):
#	return create_ns_iset(region)
	return create_ns_region(iset_to_regionS(isetid))

def disable_ns(namespacen):
	cmd = [ "/usr/bin/ndctl", "disable-namespace", namespacen ]
	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return from `%s` in disable_ns, messages:" % str(cmd) )
		for line in retd['data']:
			wlprint("\t# %s" % str(line.strip()) )
		return -1

	return 0

def destroy_ns(namespacen):
	cmd = [ "/usr/bin/ndctl", "destroy-namespace", namespacen ]
	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return from `%s` in destroy_ns, messages:" % str(cmd) )
		for line in retd['data']:
			wlprint("\t# %s" % str(line.strip()) )
		return -1

	return 0

def destroy_nsf(namespacen):
	cmd = [ "/usr/bin/ndctl", "destroy-namespace", "--force", namespacen ]
	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad return from `%s` in destroy_ns, messages:" % str(cmd) )
		for line in retd['data']:
			wlprint("\t# %s" % str(line.strip()) )
		return -1

	return 0

#This command combines disable and destroy
def delete_ns(namespacen):
	if disable_ns(namespacen):
		wlprint("ERROR: disable_ns failed against %s" % str(namespacen) )
		return -1

	if destroy_ns(namespacen):
		wlprint("ERROR: destroy_ns failed against %s" % str(namespacen) )
		return -2

	return 0

#ndctl list
def list_namespace(namespacen=None):
	cmd = [ "/usr/bin/ndctl", "list", "-N" ]

	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad retrun from `%s` in list_namespace" % str(cmd) )
		sys.exit(-1)

	#This is probably wrong
	try:
		jData = json.loads(''.join(retd['data']) )
	except:
		wlprint("WARNING: Failed to load json under list_namespace")
		jData = []
	if isinstance(jData, dict):
		jData = [ jData, ]
	if namespacen:
		for entry in jData:
			if entry['dev'] == namespacen:
				return entry

		#Bail here if we somehow escape.  Return dict so we don't need to
		# worry about doing `in` against None
		return {}

	return jData


#ndctl list -RNu
# Dumps region[namespace] dict
#
def list_region_namespace(region=None, namespacen=None):
	cmd = [ "/usr/bin/ndctl", "list", "-RNu" ]

	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad retrun from `%s` in list_region_namespace" % str(cmd) )
		sys.exit(-1)

	#This is probably wrong
	try:
		jData = json.loads(''.join(retd['data']) )
	except:
		wlprint("WARNING: Failed to load json under list_region_namespace")
		jData = []
#	if isinstance(jData, dict):
#		jData = [ jData, ]

	if 'regions' in jData:
		jData = jData['regions']

	if region:
		for entry in jData:
			if entry['dev'] == region:
				if "namespaces" in entry:
					#We have a special case just for if we ALSO have namespace defined
					if namespacen:
						for nsentry in entry['namespaces']:
							if nsentry['dev'] == namespacen:
								#Formulate special region [namespace] dump.
								specialOut = copy.copy(entry)
								specialOut['namespaces'] = [ copy.copy(nsentry) ]
								return specialOut

						#Return empty dict if no namespace entry under this region is found
						return {}

					#Return the complete region entry
					return entry

				#If namespaces not in region, there are none, return empty list
				return []

		#Bail here if we somehow escape.  Return dict so we don't need to
		# worry about doing `in` against None
		return {}

	#Case if there is only namespacen defined
	if namespacen:
		for entry in jData:
			if "namespaces" in entry:
				for nsentry in entry['namespaces']:
					if nsentry['dev'] == namespacen:
						#Formulate special region [namespace] dump.
						specialOut = copy.copy(entry)
						specialOut['namespaces'] = [ copy.copy(nsentry) ]
						return specialOut

		#If we get through all the regions, and we can't find a matching namespace, return empty dict.
		return {}

	return jData

#When we say region, we mean the complete region string here; not the region # alone.
def list_region(region=None):
	cmd = [ "/usr/bin/ndctl", "list", "-Ru" ]

	retd = getProcAll(cmd)
	if retd['ret'] != 0:
		wlprint("ERROR: Got bad retrun from `%s` in list_region" % str(cmd) )
		sys.exit(-1)

	#This is probably wrong
	try:
		jData = json.loads(''.join(retd['data']) )
	except:
		wlprint("WARNING: Failed to load json under list_region")
		jData = []
	if isinstance(jData, dict):
		jData = [ jData, ]

	if region:
		for entry in jData:
			if entry['dev'] == region:
				return entry

		#Bail here if we somehow escape.  Return dict so we don't need to
		# worry about doing `in` against None
		return {}

	return jData

def list_region_iset(iset=None):
	jData = list_region(None)

	if iset:
		for entry in jData:
			if entry['iset_id'] == iset:
				return entry

		return {}

	#Return everything if iset not set.
	return jData
