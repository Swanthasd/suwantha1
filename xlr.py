#!/usr/bin/env python

import sys, string, time, os, re
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.xlrelease.domain import Task
from com.xebialabs.deployit.plugin.api.reflect import Type
from java.text import SimpleDateFormat

def createSimpleTask(phaseId, taskTypeValue, title, propertyMap):
    """
    Function that creats a simple task
    """
    parentTask = taskApi.newTask(taskTypeValue)
    parentTask.title = title
    parentTask.description = title
    sdf = SimpleDateFormat("yyyy-MM-dd hh:mm:ss")

    for item in propertyMap:
        if item.lower().find("date") > -1:
            if propertyMap[item] is not None and len(propertyMap[item]) != 0:
                parentTask.pythonScript.setProperty(item,sdf.parse(propertyMap[item]))
        else:
            parentTask.pythonScript.setProperty(item,propertyMap[item])

    taskApi.addTask(phaseId, parentTask)
def createManualTask(phaseId, taskTypeValue, title, propertyMap):
    parenttaskType = Type.valueOf(taskTypeValue)
    
    parentTask = parenttaskType.descriptor.newInstance("nonamerequired")
    parentTask.setTitle(title)
    sdf = SimpleDateFormat("yyyy-MM-dd hh:mm:ss")
    for item in propertyMap:
        if item.lower().find("date") > -1:
            if propertyMap[item] is not None and len(propertyMap[item]) != 0:
                parentTask.setProperty(item,sdf.parse(propertyMap[item])) 
        else:
            parentTask.setProperty(item,propertyMap[item]) 
    
    #parentTask.setStartDate(sdf.parse(startDate))
    taskApi.addTask(phaseId,parentTask)

def createTask(phaseId, taskTypeValue, title, propertyMap):
    parenttaskType = Type.valueOf(taskTypeValue)
    
    parentTask = parenttaskType.descriptor.newInstance("nonamerequired")
    parentTask.setTitle(title)
    sdf = SimpleDateFormat("yyyy-MM-dd hh:mm:ss")
    for item in propertyMap:
        if item.lower().find("date") > -1:
            if propertyMap[item] is not None and len(propertyMap[item]) != 0:
                parentTask.setProperty(item,sdf.parse(propertyMap[item])) 
        else:
            parentTask.setProperty(item,propertyMap[item]) 
    
    #parentTask.setStartDate(sdf.parse(startDate))
    taskApi.addTask(phaseId,parentTask)
    
app = ${Application_Name}
env = ${Application_Environment}
for enviro in env:
    phase = ''
    phaseList = ''
    if("stage-int" in enviro):
        phaseList = phaseApi.searchPhasesByTitle("stage-int-zbc-np",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "stage-int-zbc-np"
    elif("test" in enviro):
       
        phaseList = phaseApi.searchPhasesByTitle("test-zbc",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "test-zbc"
    elif("perf-int" in enviro):
       
        phaseList = phaseApi.searchPhasesByTitle("perf-int-zbc-np",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "perf-int-zbc-np"
    elif("prod" in enviro):
       
        phaseList = phaseApi.searchPhasesByTitle("prod-zbc",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "prod-zbc"
    elif("uat" in enviro):
       
        phaseList = phaseApi.searchPhasesByTitle("uat-zbc",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "uat-zbc"
    elif("dr" in enviro):
       
        phaseList = phaseApi.searchPhasesByTitle("uat-zbc",release.id)
        if len(phaseList) == 1:
            phase = phaseList[0]
            print "uat-zbc"
            
    print phase        
    for item in app:    
        server = "XL Deploy Server "
        deploymentPackage =item
        environment = enviro
        serverCI = configurationApi.searchByTypeAndTitle("xldeploy.XLDeployServer",str(server))[0]
        currentPhase = phase

        createSimpleTask(currentPhase.id,
                        "xldeploy.Deploy",
                        "Deployment of {0} to {1}".format(deploymentPackage, environment),
                        {'server':serverCI,'deploymentPackage':deploymentPackage,'deploymentEnvironment':environment}
                        )
    createManualTask(phase.id,
                    "xlrelease.Task", 
                    "Testing done by QA", {'description':'QA Check'})
