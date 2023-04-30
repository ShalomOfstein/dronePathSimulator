import matplotlib.pyplot as plt
import networkx as nx
import pykml as kml
from pykml.factory import KML_ElementMaker as KML
import zipfile
from pykml import parser
import simplekml
from os import path
import itertools

# Open the KMZ file and extract the KML file:
with zipfile.ZipFile('C:\\Users\\shalo\\OneDrive\\Desktop\\all documents\\vs_code\\DroneProject\\droneProject.kmz', 'r') as kmz:
    kml_file = kmz.extract('doc.kml')

# Parse the KML file: 
with open(kml_file) as f:
    doc = parser.parse(f).getroot()


# Extract the points from the KML file, and save them to "points"
points = []
for placemark in doc.Document.Folder.Placemark:
    coords = placemark.Point.coordinates.text
    lon, lat, alt = coords.split(',')
    points.append((float(lon), float(lat), float(alt)))

# create a graph from the points
G = nx.Graph()
G.add_nodes_from(points)


# Add edges between all pairs of nodes to create a complete graph
for u, v in itertools.combinations(points, 2):
    G.add_edge(u, v)

# Get an approximate solution to the TSP problem
tour =  tour = list(nx.algorithms.approximation.traveling_salesman.traveling_salesman_problem(G))

# Add the edges corresponding to the chosen algorithm to the graph
for i in range(len(tour) - 1):
    G.add_edge(tour[i], tour[i+1])

# Draw the graph with the edges:
pos = {point: point[:2] for point in points}
nx.draw_networkx_edges(G, pos, edgelist=[(tour[i], tour[i+1]) for i in range(len(tour) - 1)], edge_color='r', width=2)
nx.draw_networkx_nodes(G, pos, nodelist=points, node_color='b', node_size=80)
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
plt.axis('off')

plt.show()

print("tour:" , tour)
print("points:" , points)




# Create a KML object
kml = simplekml.Kml()

# Add the nodes to the KML file as placemarks
for point in points:
    kml.newpoint( coords=[(point[0], point[1], point[2])])

# Add the edges to the KML file 
linestring = kml.newlinestring(name="Tour Path")
linestring.coords = [(point[0], point[1], point[2]) for point in tour]

linestring.style.linestyle = simplekml.LineStyle(width=5, color='ff0000ff')
# Save the KML file
kml.save("output.kml")
