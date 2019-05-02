#
# pycurl/url operation library
#
# This is part of the pg-generic-py library
#
# Patrick Geary (2017) Supermicro Inc
#
from __future__ import print_function

import json
import urllib
from urllib.parse import urlencode
import pycurl
import socket
import os
import sys


from io import StringIO

import pprint

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def getHTMLFileName(url):
	return url.split("/")[-1]

#This returns a dict of the return data, efields should be a urllib.parse.urlencode()'d string
def _getRequest(username, password, url, efields=""):
	cbuf = BytesIO()
	curlI = pycurl.Curl()
	if efields != "":
		url+="?%s" % str(efields)
	curlI.setopt(pycurl.URL, url)
	curlI.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
	# curlI.setopt(pycurl.VERBOSE, 1)
	curlI.setopt(curlI.WRITEFUNCTION, cbuf.write)
	curlI.perform()

	outData = None

	try:
		outData = json.loads(cbuf.getvalue().decode('utf-8'))
	except:
		try:
			outData = cbuf.getvalue().decode('utf-8')
		except:
			print("Warning: no data in getRequest buffer.")
	curlI.close()
	return outData

#This returns a dict of the return data, efields should be a urllib.parse.urlencode()'d string
def _postRequest(username, password, url, efields=""):
	cbuf = BytesIO()
	curlI = pycurl.Curl()
	curlI.setopt(pycurl.URL, url)
	curlI.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
	curlI.setopt(pycurl.POST, 1)
	curlI.setopt(pycurl.POSTFIELDS, efields)
	# curlI.setopt(pycurl.VERBOSE, 1)
	curlI.setopt(curlI.WRITEFUNCTION, cbuf.write)
	curlI.perform()

	outData = None

	try:
		outData = json.loads(cbuf.getvalue().decode('utf-8'))
	except:
		try:
			outData = cbuf.getvalue().decode('utf-8')
		except:
			print("Warning: no data in getRequest buffer.")

	curlI.close()
	return outData

def _getRequestSave(username, password, url, out, efields=""):
	try:

		if not os.path.exists(os.path.dirname(out)):
			os.mkdir(os.path.dirname(out))
		with open(out, "wb") as oFD:
			# cbuf = BytesIO()
			curlI = pycurl.Curl()
			if efields != "":
				url+="?%s" % str(efields)
			curlI.setopt(pycurl.URL, url)
			curlI.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
			# curlI.setopt(pycurl.VERBOSE, 1)
			curlI.setopt(curlI.WRITEFUNCTION, oFD.write)
			curlI.perform()
			curlI.close()
			# return outData
		return True
	except:
		print("ERROR: getRequestSave() failed.")
		return False


def _postRequestUpload(username, password, url, postData, efields=""):
	for i in range(0, 10):
		# try:
		if True:
			cbuf = BytesIO()
			curlI = pycurl.Curl()
			if efields != "":
				url+="?%s" % str(efields)
			curlI.setopt(pycurl.URL, url)
			curlI.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
			# curlI.setopt(pycurl.VERBOSE, 1)
			curlI.setopt(pycurl.POST, 1)
			#curlI.setopt(curlI.HTTPPOST, [ (name, (curlI.FORM_FILE, file)) ])
			curlI.setopt(curlI.HTTPPOST, postData)
			curlI.setopt(curlI.WRITEFUNCTION, cbuf.write)
			curlI.perform()
			curlI.close()
			data = json.loads(cbuf.getvalue().decode('utf-8'))
			if data['status'] != 'failed':
				return data

		# except:
		else:
			pass
	return False

def _postRequestSave(username, password, url, postData, out, efields=""):
	if not os.path.exists(os.path.dirname(out)):
		os.mkdir(os.path.dirname(out))

	for i in range(0, 10):
		# try:
		if True:
			with open(out, "wb") as oFD:
				# cbuf = BytesIO()
				curlI = pycurl.Curl()
				if efields != "":
					url+="?%s" % str(efields)
				curlI.setopt(pycurl.URL, url)
				curlI.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
				# curlI.setopt(pycurl.VERBOSE, 1)
				curlI.setopt(pycurl.POST, 1)
				#curlI.setopt(curlI.HTTPPOST, [ (name, (curlI.FORM_FILE, file)) ])
				curlI.setopt(curlI.HTTPPOST, postData)
				curlI.setopt(curlI.WRITEFUNCTION, oFD.write)
				curlI.perform()
				curlI.close()
				# data = json.loads(cbuf.getvalue().decode('utf-8'))
				# if data['status'] != 'failed':
					# return data

		# except:
		else:
			pass
	return False