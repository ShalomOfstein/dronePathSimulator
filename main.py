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





def mykml(points,points1,edges):
 # Create a KML object
 kml = simplekml.Kml()

 # Add the nodes to the KML file as placemarks
 for point in points1:
     kml.newpoint(name=point, coords=[(point[1], point[0], point[2])])

 # Add the edges to the KML file 
 linestring = kml.newlinestring(name="Tour Path")
 linestring.coords=[(point[1], point[0], point[2]) for point in edges]
 linestring.style.linestyle = simplekml.LineStyle(width=0, color='ff0000ff')


 tour = kml.newgxtour(name="Play me!")
 playlist = tour.newgxplaylist()

 wait = playlist.newgxwait(gxduration=2.4)

 animatedupdate = playlist.newgxanimatedupdate(gxduration=5)
 animatedupdate.update.change = simplekml.LineStyle(width=5, color='ff0000ff')

 wait = playlist.newgxwait(gxduration=2.4)

 return kml



def mykml1(points,points1,edges):
    # Create a KML object
    kml = simplekml.Kml()

    # Add the nodes to the KML file as placemarks
    for point in points1:
        kml.newpoint(name=point, coords=[(point[1], point[0], point[2])])

    # Create a tour and playlist
    tour = kml.newgxtour(name="Play me!")
    playlist = tour.newgxplaylist()

    # Add wait time before starting animation
    playlist.newgxwait(gxduration=2)
   
    placemark = kml.newpoint(coords=[(edges[0][1],edges[0][0],edges[0][2])])
    placemark.altitudemode = simplekml.AltitudeMode.clamptoground
    placemark.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

    # Add the edges to the KML file 
    for i, edge in enumerate(edges[:-1]):
         
        linestring = kml.newlinestring(name=f"Edge {i}")
        linestring.coords=[(edges[i][1],edges[i][0],edges[i][2]),(edges[i+1][1],edges[i+1][0],edges[i+1][2])]
        linestring.style.linestyle = simplekml.LineStyle(width=5, color='ff0000ff')
        
        # Create a flyto for each edge
        flyto = playlist.newgxflyto(gxduration=5)
        flyto.camera.longitude = (edges[i][1] + edges[i+1][1]) / 2
        flyto.camera.latitude = (float(edges[i][0]) + float(edges[i+1][0])) / 2
        flyto.camera.altitude = 500
        flyto.camera.tilt = 0
        
       # Set new coordinates for placemark
        new_coords = [(edges[i+1][1]),( edges[i+1][0]), (edges[i+1][2])]
    

        # Create animated update to move placemark
    
        animatedupdate = playlist.newgxanimatedupdate(gxduration=2)
        animatedupdate.update.change = f'<Point targetId="{placemark.id}"><coordinates>{new_coords[0]},{new_coords[1]},{new_coords[2]}</coordinates></Point>'

        # Add wait time before showing next edge
        playlist.newgxwait(gxduration=2)

    return kml






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

# plt.show()
kml = mykml1(points,points1,edges)

# Save the KML file
kml.save("output.kml")





