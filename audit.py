"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "cleveland-original.osm"
last_word_reg = re.compile(r'\b\S+\.?$', re.IGNORECASE)



#Definition of expected street-types
expected = ["Avenue",
            "Boulevard",
            "Court",
            "Circle",
            "Drive",
            "Highway",
            "Lane",
            "Marketplace",
            "Place",
            "Parkway",
            "Road",
            "Street",
            "Square",
            "Terrace",
            "Trail"]

#Mapping to target the specific errors in the dataset:
mapping_road = {
            "ave": "Avenue",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "ct": "Court",
            "Ct": "Court",
            "cir":"Circle",
            "Cir": "Circle",
            "Dr": "Drive",
            "Dr.": "Drive",
            "LANE": "Lane",
            "Ln": "Lane",
            "Pkwy": "Parkway",
            "Pl": "Place",
            "PL": "Place",
            "Rd.": "Road",
            "Rd": "Road",
            "St": "Street",
            "St ": "Street ",
            " St": " Street",
            "St.": "Street",
            "St. ": "Street",
            "st.": "Street",
            
            }
#account for the directions
mapping_directions = {
            "N": "North",
            "N.": "North",
            "E": "East",
            "E.": "East",
            "S": "South",
            "S.": "South",
            "W": "West",
            "W.": "West",
            "NE": "North East",
            "NE.": "North East",
            "SE": "South East",
            "SE.": "South East",
            "NW": "North West",
            "NW.": "North West",
            "SW": "South West",
            "SW.": "South West"
            
            }



def audit_street_type(street_types, street_name):
    m = last_word_reg.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
           


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        elem.clear() #prevents from memory error                

    return street_types

#Update the abbreviation of direction or street-type
def update_direction(better_name,mapping_directions):
    m = last_word_reg.search(better_name)
    better_name_direction = better_name
    if m:
        current_direction = m.group()

        if current_direction in mapping_directions:
            better_street_direction = mapping_directions[m.group()]
            better_name_direction = last_word_reg.sub(better_street_direction, better_name)
    return better_name_direction

def update_name(name, mapping_road):
    m = last_word_reg.search(name)
    better_name = name
    if m:
        current_name = m.group()

        if current_name in mapping_road:
            better_street_type = mapping_road[m.group()]
            better_name = last_word_reg.sub(better_street_type, name)

    return better_name


#audit street types and print these out to inspect visually. 
def run():
    global st_types
    st_types = audit(OSMFILE)
 
    pprint.pprint(dict(st_types))
    

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping_road)
            better_name_direction = update_direction(better_name, mapping_directions)
        print (name, "=>", better_name_direction)            
    return better_name

if __name__ == '__main__':
    run()

