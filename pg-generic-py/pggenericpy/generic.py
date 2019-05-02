#
# super-generic methods
#
# This is part of the pg-generic-py library
#
# Patrick Geary (2017) Supermicro Inc
#

import subprocess

def getProc(proc):
    process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(process.stdout.readline, b'')

def getProcL(proc):
    out = []
    for line in getProc(proc):
        out.append(line.decode('utf-8'))
    return out

def getProcRC(proc):
    process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cb = process.communicate()[0]
    return process.returncode

#For when we need stdout/stderr and the rc.
def getProcAll(proc):
	process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	dOut = []
	for line in iter(process.stdout.readline, b''):
		dOut.append(line.decode('utf-8'))
	cb = process.communicate()[0]
	return { 'ret':process.returncode, 'data':dOut }

#Shell-based calls
def getProcS(proc):
    process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return iter(process.stdout.readline, b'')

def getProcLS(proc, shell=True):
    out = []
    for line in getProc(proc):
        out.append(line.decode('utf-8'))
    return out

def getProcRCS(proc):
    process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    cb = process.communicate()[0]
    return process.returncode

#For when we need stdout/stderr and the rc.
def getProcAllS(proc):
    process = subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    dOut = []
    for line in iter(process.stdout.readline, b''):
        dOut.append(line.decode('utf-8'))
    cb = process.communicate()[0]
    return { 'ret':process.returncode, 'data':dOut }