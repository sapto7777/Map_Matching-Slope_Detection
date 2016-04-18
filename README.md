# Map_Matching-Slope_Detection

Input of map matching:
  
  -Probe point data
  
  -Link data
  
  
Output:
  
  -Matched points
  
  
Input of slope detection:
  
  -Link data
  
  -Matched points


Output:
  
  -Slope for each link



ProbePoints Record Format:

	sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading

		0 sampleID	is a unique identifier for the set of probe points that were collected from a particular phone.
		1 dateTime	is the date and time that the probe point was collected.
		2 sourceCode	is a unique identifier for the data supplier.
		3 latitude	is the latitude in decimal degrees.
		4 longitude	is the longitude in decimal degrees.
		5 altitude	is the altitude in meters.
		6 speed		is the speed in KPH.
		7 heading		is the heading in degrees.


LinkData Record Format:

	linkPVID, refNodeID, nrefNodeID, length, functionalClass, directionOfTravel, speedCategory, fromRefSpeedLimit, toRefSpeedLimit, fromRefNumLanes, toRefNumLanes, multiDigitized, urban, timeZone, shapeInfo, curvatureInfo, slopeInfo

		0 linkPVID		is the published versioned identifier for the link.
		1 refNodeID		is the internal identifier for the linkís reference node.
		2 nrefNodeID		is the internal identifier for the linkís non-reference node.
		3 length			is the length of the link (in decimal meters).
		4 functionalClass		is the functional class for the link (1-5).
		5 directionOfTravel	is the allowed direction of travel for the link (F ñ from ref node, T ñ towards ref node, B - both)
		6 speedCategory		is the speed category for the link (1-8).
		7 fromRefSpeedLimit	is the speed limit for the link (in kph) in the direction of travel from the reference node.
		8 toRefSpeedLimit		is the speed limit for the link (in kph) in the direction of travel towards the reference node.
		9 fromRefNumLanes		is the number of lanes for the link in the direction of travel from the reference node.
		10 toRefNumLanes		is the number of lanes for the link in the direction of travel towards the reference node.
		11 multiDigitized		is a flag to indicate whether or not the link is multiply digitized (T ñ is multiply digitized, F ñ is singly digitized).
		12 urban			is a flag to indicate whether or not the link is in an urban area (T ñ is in urban area, F ñ is in rural area).
		13 timeZone		is the time zone offset (in decimal hours) from UTC.
		14 shapeInfo		contains an array of shape entries consisting of the latitude and longitude (in decimal degrees) and elevation (in decimal meters) for the linkís nodes and shape points ordered as reference node, shape points, non-reference node. The array entries are delimited by a vertical bar character and the latitude, longitude, and elevation values for each entry are delimited by a forward slash character (e.g. lat/lon/elev|lat/lon/elev). The elevation values will be null for linkís that donít have 3D data.
		15 curvatureInfo		contains an array of curvature entries consisting of the distance from reference node (in decimal meters) and curvature at that point (expressed as a decimal value of 1/radius in meters). The array entries are delimited by a vertical bar character and the distance from reference node and curvature values for each entry are separated by a forward slash character (dist/curvature|dist/curvature). This entire field will be null if there is no curvature data for the link.
		16 slopeInfo		contains an array of slope entries consisting of the distance from reference node (in decimal meters) and slope at that point (in decimal degrees). The array entries are delimited by a vertical bar character and the distance from reference node and slope values are separated by a forward slash character (dist/slope|dist/slope). This entire field will be null if there is no slope data for the link.


Map matching output is the following file:

Partition6467MatchedPoints.csv	The subset of probe points in partion 6467 that were successfully map-matched to a link.

MatchedPoints Record Format:

	sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink

		0 sampleID	is a unique identifier for the set of probe points that were collected from a particular phone.
		1 dateTime	is the date and time that the probe point was collected.
		2 sourceCode	is a unique identifier for the data supplier.
		3 latitude	is the latitude in decimal degrees.
		4 longitude	is the longitude in decimal degrees.
		5 altitude	is the altitude in meters.
		6 speed		is the speed in KPH.
		7 heading		is the heading in degrees.
		8 linkPVID	is the published versioned identifier for the link.
		9 direction	is the direction the vehicle was travelling on thelink (F = from ref node, T = towards ref node).
		distFromRef	is the distance from the reference node to the map-matched probe point location on the link in decimal meters.
		distFromLink	is the perpendicular distance from the map-matched probe point location on the link to the probe point in decimal meters.
