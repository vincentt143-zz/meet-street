import json
import urllib2
from numpy import *
from scipy.spatial import ConvexHull

def getCoordinates(address):
  response = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=" + address).read()
  response = json.loads(response)
  return [response["results"][0]["geometry"]["location"]["lat"], response["results"][0]["geometry"]["location"]["lng"]]

def getLocationName(lat, lng):
  response = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng)).read()
  response = json.loads(response)
  return response["results"][0]["formatted_address"]



def getPointsOfInterest(lat, lng, type, radius = "500m"):
  response = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=" + type + "&key=AIzaSyDdrdJXlBA9SvDFpV2ySAS0RkUvaGb7lAU").read()
  response = json.loads(response)
  for poi in response["results"]:
    poi["dist"] = (poi["geometry"]["location"]["lat"] - lat)**2 + (poi["geometry"]["location"]["lng"] - lng)**2
  response = sorted(response["results"], key=lambda location: location["dist"])
  return response

def findMidpoint(coordinates):
  numCoords = 0.0
  totalX = 0.0
  totalY = 0.0
  Xaverage = 0.0
  Yaverage = 0.0
  isX = True
  for coord in coordinates:
    if(isX == True):
      totalX = totalX + coord
      isX = False
    else:
      totalY = totalY + coord
      isX = True
      numCoords = numCoords + 1
  if(numCoords > 0):
    Xaverage = totalX/numCoords
    Yaverage = totalY/numCoords
  midpoint = [Xaverage, Yaverage]
  return midpoint

# getLocationName(-33.9174103,151.2313068)
getPointsOfInterest(-33.8670522, 151.1957362, "food", 500)
# location=-33.8670522,151.1957362&radius=500&types=food&name=cruise

#return a 1d array that has the first x, y, then the next x,y and then the next x,y counterclockwise

def getConvexHullPoints(coordinates):
  hull = ConvexHull(coordinates)
  returnableCoordinates = []
  hullVertices = hull.vertices
  for index in hullVertices:
    for coord in hull.points[index]:
      returnableCoordinates.append(coord)
  return returnableCoordinates
