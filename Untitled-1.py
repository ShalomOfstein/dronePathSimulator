import matplotlib.pyplot as plt
import networkx as nx
import pykml as kml
import zipfile
from pykml import parser
from os import path
import itertools

# Open the KMZ file and extract the KML file
with zipfile.ZipFile('C:\\Users\\shalo\\OneDrive\\Desktop\\all documents\\vs_code\\DroneProject\\droneProject.kmz', 'r') as kmz:
    kml_file = kmz.extract('doc.kml')

# Parse the KML file using pykml
with open(kml_file) as f:
    doc = parser.parse(f).getroot()


# Extract the points from the KML file
points = []
for placemark in doc.Document.Folder.Placemark:
    coords = placemark.Point.coordinates.text
    lon, lat, alt = coords.split(',')
    points.append((float(lon), float(lat), float(alt)))


G = nx.Graph()
G.add_nodes_from(points)


# Add edges between all pairs of nodes to create a complete graph
for u, v in itertools.combinations(points, 2):
    G.add_edge(u, v)

# Get an approximate solution to the TSP problem
tour =  tour = list(nx.algorithms.approximation.traveling_salesman.christofides(G))

# Add the edges corresponding to the tour to the graph
for i in range(len(tour) - 1):
    G.add_edge(tour[i], tour[i+1])
# Draw the graph with the tour
pos = {point: point[:2] for point in points}
nx.draw_networkx_edges(G, pos, edgelist=[(tour[i], tour[i+1]) for i in range(len(tour) - 1)], edge_color='r', width=2)
nx.draw_networkx_nodes(G, pos, nodelist=points, node_color='b', node_size=80)
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
plt.axis('off')

plt.show()
