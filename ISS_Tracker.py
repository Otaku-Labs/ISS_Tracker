import requests
import json

# Main function simply a generic API GET request used 
# by all functions
# Converts binary response into Python object (List, Dict,...)
def makeRequest(url):
    '''makeRequest(url) --> Returns a json response from ISS api

    Parameters:
    url: The api url to make the request on
    '''
    try:
        with requests.get(url) as res:
            if res.status_code in range(200, 300):
                s = res.text
                json_acceptable_string = s.replace("'", "\"")
                return json.loads(json_acceptable_string)
            else:
                res.close()
                raise("Something went wrong...")
    except:
        pass


# Parameters are lead with a '?' followed by the parameter name 
# and '=' followed by the option
# e.g. ?format=json
#
# if multiple parameters exist, they can be concatenated with '&'
# e.g. ?timestamps=1436029892,1436029902&units=miles

# satellites/
def satellites():
    """ 
    RETURNS:
    A list of satellites that this API has information about, 
    inluding a common name and NORAD catalog id. 
    Currently, there is only one, the International Space Station. 
    But in the future, we plan to provide more.

    PARAMETERS:
    None
    """
    site = f"https://api.wheretheiss.at/v1/satellites"
    return makeRequest(site)


# satellites/[id]
def satellite_by_id(id, ts=None, units="kilometers"):
    """ 
    RETURNS:
    Position, velocity, and other related information about 
    a satellite for a given point in time. 
    
    [id] is required and should be the NORAD catalog id.

    PARAMETERS:
    timestamp       Unix Timestamp      No      current timestamp
    units           kilometers/miles    No      kilometers
    """

    site = f"https://api.wheretheiss.at/v1/satellites/{id}"

    if ts and units:
        site.join(f"?timestamp={ts}&units={units}")
    elif ts:
        site.join(f"?timestamp={ts}")
    
    return makeRequest(site)
    

# satellites/[id]/positions
def sat_positions(id, ts, units="kilometers"):
    """ 
    RETURNS:
    A  list in which each entry contains position, velocity, and 
    other related information about a satellite 
    for a comma delimited list of timestamps (up to 10). 
    
    [id] is required and should be the NORAD catalog id.

    PARAMETERS:
    timestamp       Unix timestamp      Yes     None
    units           kilometers/miles    No      kilometers

    Example Resource URL:
    https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps=1436029892,1436029902&units=miles
    """
    site = f"https://api.wheretheiss.at/v1/satellites/{id}/positions?timestamps={ts}&units={units}"
    return makeRequest(site)


# satellites/[id]/tles
def sat_tles(id, format=None):
    """ 
    RETURNS:
    The TLE data for a given satellite in either json or text format 
    
    [id] is required and should be the NORAD catalog id.

    PARAMETERS:
    format      text/json      No      json

    Example Resource URL (json)
    https://api.wheretheiss.at/v1/satellites/25544/tles
    """
    site = f"https://api.wheretheiss.at/v1/satellites/{id}/tles"
    if format:
        site.join(f"?format={format}")
    return makeRequest(site)


# coordinates/[lat,lon]
def coordinates(lat, lon):
    """ 
    RETURNS:
    The TLE data for a given satellite in either json or text format 
    
    [id] is required and should be the NORAD catalog id.

    PARAMETERS:
    lat     float       Yes      None
    lon     float       Yes      None

    Example Resource URL
    https://api.wheretheiss.at/v1/coordinates/37.795517,-122.393693
    """
    site = f"https://api.wheretheiss.at/v1/coordinates/{lat},{lon}"
    return makeRequest(site)
