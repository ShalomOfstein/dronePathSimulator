import matplotlib.pyplot as plt
import networkx as nx
import pykml as kml
from pykml.factory import KML_ElementMaker as KML
import zipfile
from pykml import parser
import simplekml
from os import path
import itertools
from math import radians, sin, cos, sqrt, atan2

def get_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Open the KMZ file and extract the KML file:
with zipfile.ZipFile('C:\\Users\\shalo\\OneDrive\\Desktop\\all documents\\vs_code\\DroneProject\\droneProject.kmz', 'r') as kmz:
    kml_file = kmz.extract('doc.kml')

# Parse the KML file: 
with open(kml_file) as f:
    doc = parser.parse(f).getroot()


# Extract the points from the KML file, and save them to "points"
points = []
points1 = []
for placemark in doc.Document.Folder.Placemark:
    coords = placemark.Point.coordinates.text
    lon, lat, alt = coords.split(',')
    points.append((float(lat), float(lon), float(alt)))
    points1.append((float(lat), float(lon), float(alt)))

# create a graph from the points
G = nx.Graph()
G.add_nodes_from(points)
print(points)
print(G.nodes)

# Add edges between all pairs of nodes to create a complete graph
for u, v in itertools.combinations(points, 2):
    weight = get_distance(u[0], u[1], v[0], v[1])
    G.add_edge(u, v, weight=weight)



# Get an approximate solution to the TSP problem
edges  = list(nx.algorithms.approximation.traveling_salesman.traveling_salesman_problem(G))

# Add the edges corresponding to the chosen algorithm to the graph
for i in range(len(edges) - 1):
    G.add_edge(edges[i], edges[i+1])

# Draw the graph with the edges:
pos = {point: point[:2] for point in points}
nx.draw_networkx_edges(G, pos, edgelist=[(edges[i], edges[i+1]) for i in range(len(edges) - 1)], edge_color='r', width=2)
nx.draw_networkx_nodes(G, pos, nodelist=points, node_color='b', node_size=80)
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
plt.axis('off')

plt.show()

print("tour:" , edges)
print("points:" , points)




# Create a KML object
kml = simplekml.Kml()


# Add the nodes to the KML file as placemarks
for point in points1:
    
    kml.newpoint(name=point, coords=[(point[1], point[0], point[2])])


tour = kml.newgxtour(name="Play me!")


# Add the edges to the KML file 
linestring = kml.newlinestring(name="Tour Path")
linestring.coords=[(point[1], point[0], point[2]) for point in edges]
linestring.style.linestyle = simplekml.LineStyle(width=5, color='ff0000ff')

# Save the KML file
kml.save("output.kml")
