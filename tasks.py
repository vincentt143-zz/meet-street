import json, urllib2, math
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

def getPointsOfInterest(lat, lng, type = "food", radius = "500"):
  response = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=" + type + "&key=AIzaSyDdrdJXlBA9SvDFpV2ySAS0RkUvaGb7lAU").read()
  response = json.loads(response)
  for poi in response["results"]:
    poi["dist"] = (poi["geometry"]["location"]["lat"] - lat)**2 + (poi["geometry"]["location"]["lng"] - lng)**2
  response = sorted(response["results"], key=lambda location: location["dist"])
  return response

def findMidpoint(coordinates):
  numCoords = 0
  totalX = 0.0
  totalY = 0.0
  Xaverage = 0.0
  Yaverage = 0.0
  for coord in coordinates:
    totalX = totalX + coord[0]
    totalY = totalY + coord[1]
    numCoords = numCoords + 1
  Xaverage = totalX/numCoords
  Yaverage = totalY/numCoords
  midpoint = [Xaverage, Yaverage]
  return midpoint

def getDetails(place_id):
  response = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyDdrdJXlBA9SvDFpV2ySAS0RkUvaGb7lAU").read()
  response = json.loads(response)
  return response["result"]
 
def shortestDistance(coords):
  midpoint = findMidpoint(coords)
  lat2 = midpoint[0]
  long2 = midpoint[1]
  # Convert latitude and longitude to
  # spherical coordinates in radians.
  degrees_to_radians = math.pi/180.0
  shortest = 0
  for coordinate in coords:
    lat1 = coordinate[0]
    long1 = coordinate[1]    
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
          
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
           
    # Compute spherical distance from spherical coordinates.
           
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
       
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    #multiply by radius of earth in km
    arc = arc*6378
    if(arc < shortest):
      shortest = arc   
  return shortest

def getZoomLevel(shortest):
  toDisplay = shortest*2
  zoomLevel = 0
  lengthDisplayed = 40075
  while(lengthDisplayed > toDisplay):
    zoomLevel += 1
    lengthDisplayed = lengthDisplayed**(1/2)
  zoomLevel -= 1
  return zoomLevel


#return a 1d array that has the first x, y, then the next x,y and then the next x,y counterclockwise

def getConvexHullPoints(coordinates):
  hull = ConvexHull(coordinates)
  returnableCoordinates = []
  hullVertices = hull.vertices
  for index in hullVertices:
    returnableCoordinates.append(hull.points[index])
  return returnableCoordinates
