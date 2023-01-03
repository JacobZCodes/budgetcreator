import requests
import json
"""
This function is the heart of the entire program. Requests module
gets an HTTP response from Mapbox API in the form of a Geocoding response
object (a JSON string). Digging into the properties of this Geocoding
response object, one of the properties is a features array, but this is
easily converted into a list made up of dictionary elements via 
the JSON module. Within these dictionary elements there is a key called 
'properties' with a nested key called 'category' containing values of 
string descriptors that describe the requested location. Since each Geocoding 
response object will respond with multiple locations (e.g., a search for Target would
give a Geocoding response object with multiple Targets at different locations)
, I set properties = set() inside of the function in order to filter out
repetetive descriptors.
"""
def find_properties(location):
    properties = set()
    link = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity=-117.85331471845761,33.79156714114322&access_token=pk.eyJ1IjoiamFjb2JtYXBzIiwiYSI6ImNsYmlrMzR6YjB2ejIzbm8zdGJiZGpmYjgifQ.BQa0LwKKHL7MTbjpBRzyfA"    
    r = requests.get(link)
    r = r.text
    data = json.loads(r)
    for place in data['features']:
        try:
            # This inner for loop is countering a problem I ran into when
            # adding each location's properties into my properties set. Since
            # I want to be able to loop through each descriptor within my 
            # properties set, I need each item of the set to be an individual string word.
            # However, some locations have multiple properties encased in a single string,
            # so this would mess up my program when it tried to loop through
            # the properties set since a string containing multiple words would be 
            # iterated over instead of iterating over each word in the string. 
            # Thus, the below for-loop serves to unpack these problematic, larger
            # strings and break them down into individual string words.
            for descriptor in place['properties']['category'].split(','):
                descriptor = descriptor.strip()
                properties.add(descriptor)
        except KeyError:
            continue
    return properties

print(find_properties('Kroger'))









