import xml.etree.ElementTree as ET
from OneWayTrip.map.Street import House, Street

__author__ = 'elleryaree'

tree = ET.parse('../data/map.xml')
root = tree.getroot()

streets = []
for child in root.iter('street'):
    houses = []
    for neighbor in child.iter('house'):
        house = House(neighbor.get("id"),
                        neighbor.get("name"))
        houses.append(house)

    street = Street(houses,
                        child.get("id"),
                        child.get("name"),
                        child.get("x"),
                        child.get("y"))
    streets.append(street)

print "Parse result:"
for street in streets:
    print "Street: ", street.name
    for house in street.houses:
        print "\thouse: ", house.name