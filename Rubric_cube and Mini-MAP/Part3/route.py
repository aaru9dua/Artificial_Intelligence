#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
import math
from queue import PriorityQueue
import numpy as np

#parse throught road-segments.txt and create key-value pairs (bidirectional)
def road_segment_parser():
    road_segments = {}
    distances = []
    speeds = []
    with open('road-segments.txt') as f:
        lines = f.readlines()
        for line in lines:
            arr = line.rstrip("\n").split(" ")
            start_city = arr[0]
            end_city = arr[1]
            desc = arr[2:5]
            distances.append(float(desc[0]))
            speeds.append(int(desc[1]))

            if start_city in road_segments.keys():
                road_segments[start_city].append([end_city] + desc)
            else:
                road_segments[start_city] = [[end_city] + desc]

            if end_city in road_segments.keys():
                road_segments[end_city].append([start_city] + desc)
            else:
                road_segments[end_city] = [[start_city] + desc]
    
    #calculate average segment distance and max speed across dataset
    avg_segment_distance = 0.25*max(distances)+0.75*(sum(distances)/len(distances))
    max_speed = max(speeds)

    return (avg_segment_distance,max_speed,road_segments)

#parse through city-gps.txt and assign the latitude-longitude coordinates to each city
def gps_parser():
    gps_city = {}
    with open('city-gps.txt') as f:
        lines = f.readlines()
        for line in lines:
            arr = line.rstrip("\n").split(" ")
            city,lat_long = arr[0],arr[1:]
            gps_city[city] = lat_long

    return gps_city

#find haversine distance between two cities
def find_distance(start, end):
    start_lat, start_long = float(start[0]), float(start[1])
    end_lat, end_long = float(end[0]), float(end[1])
    dLat = (end_lat - start_lat) * math.pi / 180.0
    dLon = (end_long - start_long) * math.pi / 180.0

    # convert to radians
    lat1 = (start_lat) * math.pi / 180.0
    lat2 = (end_lat) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2));

    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

#in case of missing coordinates, we follow triangulation and find the average of the coordinates of the neighboring cities
def find_avg_coordinate(city,road_segments,gps_city):
    neighbour_lat = []
    neighbour_long = []
    neighbors = road_segments[city]

    for neighbors in road_segments[city]:
        if(neighbors[0] in gps_city.keys()):
            neighbour_coord = gps_city[neighbors[0]]
            neighbour_lat.append(float(neighbour_coord[0]))
            neighbour_long.append(float(neighbour_coord[1]))

    if(len(neighbour_lat)!=0 and len(neighbour_long)!=0):
        avg_lat = sum(neighbour_lat)/len(neighbour_lat)
        avg_long = sum(neighbour_long)/len(neighbour_long)

    else:
        avg_lat = 0
        avg_long = 0
        
    coord_city = [avg_lat,avg_long]
    return coord_city

#calculate cost functions for segments, distance, time and delivery time
def calc_cost_function(cost_function,segments,curr_distance,curr_speed,havershine_distance,time,delivery_time,max_speed,avg_segment_distance):
    calc_cost = 0
    if(cost_function=='segments'):
        calc_cost = segments + (havershine_distance/avg_segment_distance)

    elif(cost_function=='distance'):
        calc_cost = curr_distance + havershine_distance

    elif(cost_function=='time'):
        calc_cost = time + (havershine_distance/max_speed)

    elif(cost_function=='delivery'):
        calc_cost = delivery_time + (havershine_distance/max_speed)


    return calc_cost

def get_route(start, end, cost):

    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """


    avg_segment_distance,max_speed,road_segments = road_segment_parser()

    gps_city = gps_parser()
    
    fringe = PriorityQueue()
    fringe.put((0,start,0,0,0,0,''))
    visited = [start]
    while fringe:
        (calc_cost, curr_city, segments, dist, time, delivery_time, route_taken) = fringe.get()

        #successor function to fetch the next set of cities 
        next_cities_desc = road_segments[curr_city]

        for city_desc in next_cities_desc:
            city, curr_distance, curr_speed, highway_name = city_desc[0], float(city_desc[1]), float(city_desc[2]), city_desc[3]
            route_temp = route_taken
            if(city not in visited):
                route_temp += city + '#' + highway_name + " for " + str(int(curr_distance)) + " miles$"
                #find havershine distance between start node and existing node
                #print(gps_city[city])
                # print(route_temp)
                if(city not in gps_city.keys()):
                    coord_city = find_avg_coordinate(city, road_segments, gps_city)

                else:
                    coord_city = gps_city[city]

                #find havershine distance between existing node and end city
                havershine_distance = find_distance(coord_city, gps_city[end])

                total_dist = curr_distance + dist

                curr_time = (curr_distance/curr_speed)

                total_time = time+curr_time

                p = 0
                if(curr_speed >= 50):
                    p = np.tanh(curr_distance/1000)

                curr_delivery_time = (curr_distance/curr_speed) +  p*2*((curr_distance/curr_speed) + delivery_time)

                total_delivery_time = delivery_time + curr_delivery_time

                calc_cost = calc_cost_function(cost,segments+1,total_dist,curr_speed,havershine_distance,total_time,total_delivery_time,max_speed,avg_segment_distance)

                if city==end:
                    route_taken = list(map(lambda x: tuple(x.split('#')),route_taken.split('$')))
                    route_taken.pop()
                    route_taken.append((end,highway_name + " for " + str(int(curr_distance)) + " miles"))
                    return {"total-segments" : len(route_taken),
                            "total-miles" : total_dist,
                            "total-hours" : total_time,
                            "total-delivery-hours" : total_delivery_time,
                            "route-taken" : route_taken}
                else:
                    fringe.put((calc_cost, city, segments+1, total_dist, total_time, total_delivery_time, route_temp))


        visited.append(curr_city)





# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
