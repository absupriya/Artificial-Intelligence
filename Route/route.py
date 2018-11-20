#!/usr/bin/env python2

""" 
**************************************************************************************** Comments start *******************************************************************************************
1. Formulation of search problem:
The user inputs the start city, destination city, routing algorithm and the cost function (in the same order) to the script route.py.
The two datasets road-segments.txt and city-gps.txt are read using pandas and stored the data in dataframes. Using the dataframes, nodes and edges weights were stored in dictionaries by using Graph class to generate graph. 
As per the input parameters, respective algorithm function is invoked and the best possible route is printed.


2. Abstraction:
Initial state: The initial state is the start city which is passed as the first argument to the script.
State Space: The state space is the set of all nodes (cities) generated using the Graph class.
Successor function: The successors for the node which is being searched are all of its neighbouring nodes except for the visited nodes. 
Goal state: The goal state is the destination city which is passed as the second argument to the script.
Edge weights/Cost function: Cost function is defined in 3 ways - Segments, Distance and Time. 
			   Segments is the route with least number of turns. 
			   Distance: The route with the shortest distance.
			   Time: The route with the least time to travel to the destination.


3. Heuristic functions:
The heuristic function choosen is the haversine function or the great-circle distance. This gives the shortest distance between the 2 points given their gps coordinates. As the haversine distance is calculated along the surface of the sphere, this gives the shortest distance between the two points. Whereas, the euclidean distance is calculated as the distance of the straight line between 2 points cutting through the earth's interior.
Below are the detailed description of the heuristics for each of the cost function.
a. Segments:
The heuristic function for the segments is the number of nodes travelled between the cities and I assumed it to be 1.

b. Distance: 
As BFS, DFS and IDS are blind search algorithms, distance cost function does not matter.
For A* algorithm, the heuristic function is the haversine distance from the current city to the goal city (using the gps coordinates from city-gps.txt dataset) and the cost function is the distance from the start city to the current city (distance from road-segments.txt dataset), i.e 
f(s) = g(s) + h(s), where g(s) is the cost function and h(s) is the haversine function.
For Uniform Cost Search, the heuristic function is only the cost function, i.e, the distance from the start city to the current city (distance from road-segments.txt dataset), i.e f(s) = g(s), where g(s) is the cost function.

c. Time: 	
As BFS, DFS and IDS are blind search algorithms, time cost function does not matter.
For A* algorithm, the heuristic function is the haversine distance/80(=considering the speed which is slightly more than the max speed from the road-segments.txt dataset) from the current city to the goal city (using the gps coordinates from city-gps.txt dataset) and the cost function is the distance/speed from the start city to the current city (distance from road-segments.txt dataset), i.e,
f(s) = g(s) + h(s), where g(s) is the cost function and h(s) is the haversine function.
For Uniform Cost Search, the heuristic function is only the cost function, i.e, the distance/speed from the start city to the current city (distance from road-segments.txt dataset), i.e, f(s) = g(s), where g(s) is the cost function.


4. Problems faced/Assumptions:
i. Few cities in the road-segments.txt dataset has speed=0 or speed=NULL. I have replaced the speeds for those cities with the max(speed) from the datatset (which I found is 65).
ii. There are around ~1000 cities with no gps coordinates and I assumed the haversine distance to be 0. Only if the cities that I am looking for the gps coordinates has an entry in the city-gps.txt dataset haversine distance is calculated, else it is considered as 0.
iii. The graph dictionary is storing the neighbouring cities as its key values as a tuple. The order in which the neighbouring cities are stored is different when seen in the dataset. I found this difference when I was running my script for DFS algorithm in python 2 and python 3 versions. Hence the DFS algorithm is giving different output. 
For eg: the graph dictionary in python 2 is storing as : {'Y_City,_Arkansas': set(['Acorn,_Arkansas', 'Hot_Springs,_Arkansas', 'Greenwood,_Arkansas'])}, 
whereas in python 3, {'Y_City,_Arkansas': set(['Acorn,_Arkansas', 'Greenwood,_Arkansas', 'Hot_Springs,_Arkansas'])}. 
Hence, for DFS and IDS algorithm, a different successor gets popped out and outputs a different route.

**************************************************************************************** Comments end ******************************************************************************************
"""


import pandas as pd
import itertools
import sys
from math import radians, cos, sin, asin, sqrt
from Queue import PriorityQueue

# Reading the datasets and storing in a dataframe.
# https://stackoverflow.com/questions/21546739/load-data-from-txt-with-pandas
citygps = pd.read_csv('city-gps.txt',delimiter=' ',names=['City','Latitude','Longitude'])
roadseg= pd.read_csv('road-segments.txt',delimiter=' ',names=['FromCity','ToCity','Distance','Speed','Highway'])

# Replacing the NAN's and 0's in the Speed column with max speed in the dataset.
# https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
# https://stackoverflow.com/questions/27060098/replacing-few-values-in-a-pandas-dataframe-column-with-another-value
roadseg['Speed'] = roadseg['Speed'].fillna(0)
roadseg[roadseg['Speed']==0] = roadseg[roadseg['Speed']==0].replace(0,max(roadseg['Speed']))

# Calculating the time in the road segments dataset and rounding it to 4 decimal places.
roadseg['Time'] = roadseg['Distance']/roadseg['Speed']
roadseg['Time'] = roadseg['Time'].round(4)


# Initiating graph
# https://www.python-course.eu/graphs_python.php
class Graph:
    print 'Generating the graph'
    def __init__(self):
        self.__graph_dict = {}
        self.__edge_dict = {}

    def generate_node(self, FromCity, ToCity, Distance, Time, Highway):
        if FromCity not in self.__graph_dict:
            self.__graph_dict[FromCity] = set()
            self.__graph_dict[FromCity].add(ToCity)
        else:
            self.__graph_dict[FromCity].add(ToCity)
        
        if ToCity not in self.__graph_dict:
            self.__graph_dict[ToCity] = set()
            self.__graph_dict[ToCity].add(FromCity)
        else:
            self.__graph_dict[ToCity].add(FromCity)
        
        
        for FromCity in self.__graph_dict:
            for ToCity in self.__graph_dict[FromCity]:
                if (FromCity, ToCity) not in self.__edge_dict:
                    self.__edge_dict[(FromCity, ToCity)]= (Distance, Time, Highway)

    def generate_edges(self):
        return self.__edge_dict

    def generate_graph(self):
        return self.__graph_dict

graph=Graph()

for i in range(len(roadseg)):
    graph.generate_node(roadseg['FromCity'][i],roadseg['ToCity'][i],roadseg['Distance'][i],roadseg['Time'][i],roadseg['Highway'][i])

mygraph = graph.generate_graph()
edges_graph = graph.generate_edges()

print 'Graph generated\n'


# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
# Calculate the great circle distance (Haversine distance) between two points on the earth (specified in decimal degrees)
def haversine(start_city,goal_city,costfunc):
    if (start_city in citygps) and (goal_city in citygps):
        lat1=citygps[citygps['City']==start_city]['Latitude']
        lon1=citygps[citygps['City']==start_city]['Longitude']
               
        lat2=citygps[citygps['City']==goal_city]['Latitude']
        lon2=citygps[citygps['City']==goal_city]['Longitude']
    
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3959 # Radius of earth in miles. Use 6371 for kilometers
        hdist= c * r
    else:
        hdist=0
	
	
    if costfun=='segments':
        return 1
    elif costfun=='distance':
        return hdist
    elif costfun=='time':
        return hdist/80  # Assuming a speed which is slightly greater than the max speed from the road-segments dataset.


# Breadth First Search algorithm
def bfs(graph, start, goal):
    visited=[]
    bfs_fringe = [(start, [start])]
    while len(bfs_fringe) > 0:
        (state, path) = bfs_fringe.pop(0)
        visited.append((state, path))
        for succ in graph[state]-set(path):
            if succ not in visited:
                visited.append((state, (path + [succ])))
            if succ==goal:
                return (path + [succ])
            else:
                bfs_fringe.append((succ,(path + [succ])))
    return False


# Depth First Search algorithm 
def dfs(graph, start, goal, depth):
    visited = []
    dfs_fringe = [(start, [start])]
    while len(dfs_fringe)>0:
        if depth==0:
            if start==destination:
                 return True
            return False
        (state, path) = dfs_fringe.pop()
        visited.append((state,path))
        for succ in graph[state] - set(path):
            if succ not in visited:
                visited.append((succ,(path + [succ])))
            if succ == goal:
                return path + [succ]
            if depth!=None and len(visited)>=depth:
                continue
            dfs_fringe.append((succ,(path + [succ])))
    return False


# Iterative Deepening Search algorithm. Calling DFS algorithm by incrementing the depth untill goal state is reached. 
def ids(graph, start, goal):
    for depth in itertools.count():
        route = dfs(graph, start, goal, depth)
        if route:
            return route
    return False


# A* and uniform cost search algorithm.
# Priority queue: https://dbader.org/blog/priority-queues-in-python
def astar(graph, start, goal, costfun):
    astar_fringe = PriorityQueue()
    visited = []
    initial_cost=haversine(start, goal, costfun)
    astar_fringe.put((initial_cost, (start, [start])))
	
    while not astar_fringe.empty():
        (priority,(state, path))=astar_fringe.get()
        visited.append(state)
        if state == goal:
            return path
        else:
            for succ in graph[state] - set(visited):
                if routealgo=='astar':
                    heuristic_cost=haversine(succ,goal,costfun)
                    route_so_far_cost=costfunction(path,costfun)
                elif routealgo=='uniform':
                    heuristic_cost=0
                    route_so_far_cost=costfunction(path,costfun)
                cost_so_far = route_so_far_cost + heuristic_cost               
                if succ not in visited:
                    astar_fringe.put((cost_so_far,(succ, (path + [succ]))))
    return False	


# Cost function calculations
def costfunction(route, costfun):
    cost=0
    for i in range(len(route) - 1):
        edge=(route[i],route[i+1])
        
        if edge in edges_graph and costfun=='distance':
            cost+=edges_graph[edge][0]
        
        if edge in edges_graph and costfun=='time':
            cost+=edges_graph[edge][1]
        
        if costfun=='segments':
            cost=len(route)
    
    return cost
	
# Final output format
def finaloutput(route):
    if route is None:
        print 'No route found !!'
    else:               
        if ((routealgo == 'bfs' and costfun=='segments') or routealgo=='astar' or routealgo=='uniform'):
        	optimal='yes'
        if (routealgo == 'bfs' and (costfun=='distance' or costfun=='time')) or routealgo == 'dfs' or routealgo == 'ids':
        	optimal='no'
        
        path_dist=costfunction(route,'distance')
        
        path_time=costfunction(route,'time')
        
        printable_route=' '.join(route)
        
    print optimal, path_dist, path_time, printable_route


# Intializing the input parameters.
source = sys.argv[1]
destination = sys.argv[2]
routealgo = sys.argv[3]
costfun = sys.argv[4]

# Invoking the respective functions as per the user input values.
if  routealgo == 'bfs':
    print 'Finding the route by BFS routing algorithm and',costfun,'cost function...\n'
    path = bfs(mygraph,source,destination)
    finaloutput(path)
elif routealgo == 'dfs':
    print 'Finding the route by DFS routing algorithm and',costfun,'cost function...\n'
    path = dfs(mygraph,source,destination,None)
    finaloutput(path)
elif routealgo == 'ids':
    print 'Finding the route by IDS routing algorithm and',costfun,'cost function...\n'
    path = ids(mygraph,source,destination)
    finaloutput(path)
elif routealgo == 'astar' or routealgo=='uniform':
    print 'Finding the route by',routealgo,'routing algorithm and',costfun,'cost function...\n'
    path = astar(mygraph, source, destination, costfun)
    finaloutput(path)
