from django.shortcuts import render
import urllib
import xml.etree.ElementTree as ET
import json

def vesselConfiguration(vi):
    '''
    Function to call the webservice vesselconfiguration/ with a vesselId given 
    and return a Json dict with the data
    '''
    url= "http://nautilus.intertug.com:8080/api/vesselconfiguration/"
    fleetId = vi
    url += fleetId
    try:
        openUrl = urllib.urlopen(url)
    except:
           print "Error calling vesselConfig" 
    data = openUrl.read()
    dataJson = json.loads(data)
    return dataJson

def getVesselsPosition(si, gd):
    '''
    Function to call the webservice GetVesselsPosition/ with a vesselId and a getData param given 
    and return a Json dict with the data
    '''
    url= "http://190.242.119.122:82/sioservices/daqonboardservice.asmx/GetVesselsPosition?"
    sessionId = si
    getData = gd
    params = "SessionID=" + sessionId
    params += "&GetData=" + getData
    url += params
    try:
        openUrl = urllib.urlopen(url)
    except:
        print "Error calling getVesselsPosition"
    data = openUrl.read()
    try:
        tree = ET.fromstring(data) #the Json is inside an XML, first node 
    except:
        print "Error readind the XML"
    dataJson = json.loads(tree.text)
    vessels = dataJson["vessels"]["vessel"]
    return vessels

def visualConfiguration(fi):
    '''
    Function to call the webservice visualconfiguration/ with a fleetId given 
    and return a Json dict with the data
    '''    
    url= "http://nautilus.intertug.com:8080/api/visualconfiguration/"
    fleetId = fi
    url += fleetId
    try:
        openUrl = urllib.urlopen(url)
    except:
        print "Error calling visualConfig"
    data = openUrl.read()
    dataJson = json.loads(data)
    return dataJson

def mapConfiguration(fi):
    '''
    Function to call the webservice mapconfiguration/ with a fleetId given 
    and return a Json dict with the data
    '''  
    url= "http://nautilus.intertug.com:8080/api/mapconfiguration/"
    fleetId = fi
    url += fleetId
    try:
        openUrl = urllib.urlopen(url)
    except:
        print "Error calling mapConfig"
    data = openUrl.read()
    dataJson = json.loads(data)
    return dataJson

def country(request, fleet):
    '''
    Controller that recieve a request from the browser and a parameter in the url with the fleetId
    returns a render page with the variables to use in the HTML
    '''
    sessionId = ""
    if (fleet == "0"):#if the fleetId is 0, then blank the string to search
        getData = ""
    else:
        getData = "fleetId=" + fleet
    vesselsPosition = getVesselsPosition(sessionId, getData)
    visualConfig = visualConfiguration("0")
    fleetName = "Flota Global"
    #extracts all the fleet Names
    for f in visualConfig["linksmenu"][0]["links"]:
        if fleet == str(f["value"]):
            fleetName = f["label"]
    vesselsIds = []
    #extracts all the vesselsId's
    for vessel in vesselsPosition:
        vesselsIds.append(vessel["id"])
    vesselConfig = []
    #with the vesselsId's creates all the configurations for that ids
    for vessel in vesselsIds:
        vesselConfig.append(vesselConfiguration(vessel))
    mapConfig = mapConfiguration(fleet)
    vars = {"vessels": vesselsPosition, "visual": visualConfig, "map": mapConfig, "vessel": vesselConfig, 
            "fleet": fleetName, "fleetId": fleet}
    return render(request, "country.html", vars)

def index(request):
    return render(request, "index.html")