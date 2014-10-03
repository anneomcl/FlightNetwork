import json
from pprint import pprint
import string
import sys
from Node import Node
from Edge import Edge
import webbrowser

class Graph:

    #JSON data
    data = []

    #list of Graph nodes
    nodes = []

    #list of graph edges
    edges = []

    #distance of longest flight
    longest_flight = -1

    #distance of shortest flight
    shortest_flight = -1

    #average distance of flights
    average_flight_dist = -1

    #population of largest city
    largest_city = -1

    #population of smallest city
    smallest_city = -1

    #average population of cities
    average_city_pop = -1

    #initializes Graph
    #param path - file path for JSON file to import
    def __init__(self, path):
        self.import_data(path)
        self.create_edges()
        self.create_nodes()

    #imports JSON data into Python
    #param path - file path for JSON file to import
    def import_data(self, path):
        map_data=open(path)
        self.data = json.load(map_data)
        map_data.close()

    #initializes the list of nodes associated with Graph
    def create_nodes(self):
        i = 0
        for key in self.data['metros']:
            self.nodes.append(Node(self.data['metros'][i], self.edges))
            i+=1

    #initializes the list of edges associated with Graph
    def create_edges(self):
        i = 0
        for key in self.data['routes']:
            self.edges.append(Edge(self.data['routes'][i]))
            return_edge = Edge(self.data['routes'][i])
            return_edge.home, return_edge.dest = return_edge.dest, return_edge.home
            self.edges.append(return_edge)
            i+=1

    #prompts user with options to get information on CSAir
    def user_input(self):
        while(1):
            query = input("(1) Get all cities (2) Get information on specific city (3) Statistics (exit) Quit\n")
            if query == 'exit':
                break
            if query == '1':
                self.get_all_cities()
            if query == '2':
                self.get_city_info()
            if query == '3':
                self.get_stats()

    #handles option 1 (list all cities)
    def get_all_cities(self):
        i = 0
        for Node in self.nodes:
            print(self.nodes[i].name)
            i+=1

    #handles option 2 (get info from specific city)
    def get_city_info(self):
        while(1):
            query = input("Enter the code or name of the city to query, or 'exit' to quit: \n")
            if query == 'exit':
                break
            i = 0
            for Node in self.nodes:
                if query == self.nodes[i].name or query == self.nodes[i].code:
                    self.get_city_info_helper(self.nodes[i])
                i+=1

    #helps handle option 2. Allows users to query different facts about a given city
    #param node - the node (city) a user wants to know more about
    def get_city_info_helper(self, node):
        while(1):
            print("What would you like to know about", node.name,"?")
            query = input("(1) Code (2) Name (3) Country (4) Continent (5) Timezone \n"
                  "(6) Coordinates (7) Population (8) Region (9) Connected Cities (exit) Quit\n")
            if query == 'exit':
                break
            if query == '1':
                print(node.code, '\n')
            if query == '2':
                print(node.name, '\n')
            if query == '3':
                print(node.country, '\n')
            if query == '4':
                print(node.continent, '\n')
            if query == '5':
                print(node.timezone, '\n')
            if query == '6':
                print(node.coords, '\n')
            if query == '7':
                print(node.population, '\n')
            if query == '8':
                print(node.region, '\n')
            if query == '9':
                print(node.adjacent_cities, '\n')

    #handles option 3 (getting statistics)
    def get_stats(self):
         while(1):
            print("What would you like to know about our flight network?")
            query = input("(1) Longest Flight (2) Shortest Flight (3) Average Distance of Flights\n"
                          "(4) Largest City (5) Smallest City (6) Average Size of Cities\n"
                          "(7) List of Cities by Continent (8) Cities w/ Most Connections (exit) Quit\n")
            if query == 'exit':
                break
            if query == '1':
                print(self.get_longest_flight().home,"to", self.get_longest_flight().dest,
                      "\nDistance: ", self.get_longest_flight().distance, "\n")
            if query == '2':
                print(self.get_shortest_flight().home,"to", self.get_shortest_flight().dest,
                      "\nDistance: ", self.get_shortest_flight().distance, "\n")
            if query == '3':
                print("Distance of Average Flight: ", self.get_avg_flight(), "\n")
            if query == '4':
                print("Largest City: ", self.get_big_city().name, "\nPopulation: ", self.get_big_city().population, "\n")
            if query == '5':
                print("Smallest City: ", self.get_small_city().name, "\nPopulation: ", self.get_small_city().population, "\n")
            if query == '6':
                print("Average City Size: ", self.get_avg_city(), "\n")
            if query == '7':
                i = 0
                for item in self.get_city_by_continent()[0]:
                    print("Continent: ", self.get_city_by_continent()[0][i], "\n"
                    "Cities: ", self.get_city_by_continent()[1][i],"\n")
                    i+=1
            if query == '8':
                print("Cities w/ Most Connections: ", self.get_hub_city(), "\n")

    #handles query 7 of option 3: gets a list of cities organized by continents
    #return - list of continents, double array of cities where cities[i] is all the cities at continents[i]
    def get_city_by_continent(self):
        i = 0
        continents = []
        cities = []
        for Node in self.nodes:
            if self.nodes[i].continent not in continents:
                continents.append(self.nodes[i].continent)
                cities.append([])

            j = 0
            for cont in continents:
                if self.nodes[i].continent == continents[j]:
                    break
                j+=1
            cities[j].append(self.nodes[i].name)
            i+=1

        return continents, cities

    #finds the city or cities with the most edges
    #return - city or cities with the most edges
    def get_hub_city(self):
        i = 0
        curr = 0
        hubs = []
        for Node in self.nodes:
            if len(self.nodes[i].adjacent_cities) == curr:
                hubs.append(self.nodes[i].name)
            elif len(self.nodes[i].adjacent_cities) > curr:
                hubs = [self.nodes[i].name]
            i += 1
        return hubs

    #finds the average population of all cities
    #return - avg population
    def get_avg_city(self):
        sum = 0
        i = 0
        for Node in self.nodes:
            sum += self.nodes[i].population
            i+=1
        return sum / i

    #finds the city with the largest population
    #return - city with largest population
    def get_big_city(self):
        i = 0
        curr = 0
        biggest = 0
        for Node in self.nodes:
            if self.nodes[i].population >= curr:
                curr = self.nodes[i].population
                biggest = i
            i+=1
        return self.nodes[biggest]

    #finds the city with the smallest population
    #return - city with smallest population
    def get_small_city(self):
        i = 0
        curr = sys.maxsize
        smallest = 0
        for Node in self.nodes:
            if self.nodes[i].population <= curr:
                curr = self.nodes[i].population
                smallest = i
            i+=1
        return self.nodes[smallest]

    #finds the average distance of all edges
    #return - avg distance
    def get_avg_flight(self):
        sum = 0
        i = 0
        for Edge in self.edges:
            sum += self.edges[i].distance
            i+=1
        return sum / i

    #gets the flight with the longest distance
    #return - edge with longest distance
    def get_longest_flight(self):
        i = 0
        curr = 0
        longest = 0
        for Edge in self.edges:
            if self.edges[i].distance >= curr:
                curr = self.edges[i].distance
                longest = i
            i+=1
        return self.edges[longest]

    #gets the flight with the shortest distance
    #return - edge with shortest distance
    def get_shortest_flight(self):
        i = 0
        curr = sys.maxsize
        shortest = 0
        for Edge in self.edges:
            if self.edges[i].distance <= curr:
                curr = self.edges[i].distance
                shortest = i
            i+=1
        return self.edges[shortest]

    #creates a URL for Great Circle Mapper to visualize all routes and opens the webpage
    def create_map_URL(self):
        i = 0
        url = []
        for Edge in self.edges:
            if i < len(self.edges):
                item = ""
                item+=self.edges[i].home
                item+="-"
                item+=self.edges[i].dest
                if i < len(self.edges) - 2:
                    item+=",+"
                url.append(item)
                i+=2
        url = "".join(url)
        webbrowser.open("http://www.gcmap.com/mapui?P="+url)



#x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
#x.user_input()
#x.create_map_URL()