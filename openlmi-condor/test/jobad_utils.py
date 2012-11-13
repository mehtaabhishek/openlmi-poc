#!/usr/bin/env python

from suds.client import Client
import logging
import sys


#
# Pass dict with name, type, value and convert
# to classAd SOAP format
#
def dictToClassAd(dic):
    pass

#
# Append new property in jobAd passed
#
def createAdProperty(service, job, name, typ, val):
    p = service.factory.create("ClassAdStructAttr")
    p.name = name
    p.type = typ
    p.value = val
    job[1].item.append(p)
    return job
#
# Update type and/or value of property name
#
def setAdProperty(name, typ, val):
    pass
#
# Pass jobAd (createJobTemplate) and convert to dictionary
#
def classAdToDict(job):
    d = {}
    attrs = job[1][0]
    for attr in attrs:
        d[attr['name']] = attr['value']
    return d 

#
# Pass jobAd (createJobTemplate), and print all name=value 
#
def listAdProperties(job):
	jobAd = job[1]
	for i in range(len(jobAd[0])):
		print "%s = %s" % (jobAd[0][i].name, jobAd[0][i].value)
#
# Pass property name and return {"name":"value"} dict.
#
def getAdProperty(name):
	d = {}
	for i in range(len(jobAd[0])):
		if (jobAd[0][i].name == name):
			d[jobAd[0][i].name] = jobAd[0][i].value
			return d
	return None


# ---------------- check utils -------------
CONDOR_HOST      = "mncars002"
SCHEDD_PORT      = "8080"
SCHEDD_LOCATION  = "http://" + CONDOR_HOST + ":" + SCHEDD_PORT
WSDL_SCHEDD_FILE = "file:condorSchedd.wsdl"

#
# We can query to any queue scheduler
#
condor_schedd = Client(WSDL_SCHEDD_FILE, location=SCHEDD_LOCATION)
ads = condor_schedd.service.getJobAds(None, None)
#print ads

#for i in range(len(schedds[0])):
#	schedd_ad = classad_dict(schedds[0][i])
#	print schedd_ad["Machine"] + " -> " + schedd_ad["ScheddIpAddr"]

transaction = condor_schedd.service.beginTransaction(10);
transactionId = transaction[1]

cluster = condor_schedd.service.newCluster(transactionId)
clusterId=cluster[1]

job = condor_schedd.service.newJob(transactionId, clusterId)
jobId = job[1]

job = condor_schedd.service.createJobTemplate(clusterId, 
                jobId, "condor", 5, "/bin/sleep", "30", "Queue=150")
jobAd = job[1]

ret = getAdProperty("Owner")
print ret

#listAdProperties(job)

ret = classAdToDict(job)
print ret["Owner"]

job = createAdProperty(condor_schedd, job, "Queue", "INTEGER-ATTR", 150) 
print getAdProperty("Queue")

#print jobAd[0][58].name
#jobAd[0][58].value = "FALSE"

#cls = condor_schedd.factory.create("ClassAdStructAttr")
#cls.name = "queue"
#cls.type = "INTEGER-ATTR"
#cls.value = 150
#print cls
#print job[1].item.append(cls)

# vim: ts=4:et:sw=4:tw=80:sts=4:cc=80
