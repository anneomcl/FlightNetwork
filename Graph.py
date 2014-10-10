import json
from pprint import pprint
import string
import sys
from Node import Node
from Edge import Edge
import webbrowser

class Graph:
    data = dict()

    edges = []
    nodes = []

    #initializes Graph
    #param path - file path for JSON file to import
    def __init__(self, path, path2):
        self.import_data(path, path2)
        self.create_edges()
        self.create_nodes()

    #imports JSON data into Python
    #param path - file path for JSON file to import
    def import_data(self, path, path2):
        map_data=open(path)
        data = json.load(map_data)
        map_data.close()

        map_data = open(path2)
        data2 = json.load(map_data)
        map_data.close()

        merged_data = data["metros"].copy()
        merged_data+=(data2["metros"])
        self.data["metros"] = merged_data

        merged_data = data["routes"].copy()
        merged_data += (data2["routes"])
        self.data["routes"] = merged_data

    #initializes the list of nodes associated with Graph
    def create_nodes(self):
        i = 0
        for key in self.data['metros']:
            self.nodes.append(Node(self.data['metros'][i], self.edges))
            i+=1

    #remove from nodes list, removes all edges w/ this city, redo adjacent_cities
    #param city - must enter the CODE of a city
    def delete_node(self, city):
        i = 0
        for Node in self.nodes:
            if city == self.nodes[i].code:
                self.nodes.remove(self.nodes[i])
                break
            i+=1
        i = 0
        for Edge in self.edges:
            if city == self.edges[i].home or city == self.edges[i].dest:
                self.edges.remove(self.edges[i])
                break
        i = 0
        for Node in self.nodes:
            self.nodes[i].get_adjacent_cities(self.edges)

    #removes edge in both directions
    #param home - CODE of the home city
    #param dest - CODE of the dest city
    def delete_route(self, home, dest, dir):
        i = 0
        for Edge in self.edges:
            if self.edges[i].home == home and self.edges[i].dest == dest:
                self.edges.remove(self.edges[i])
                break
            i+=1

        if(dir == '1'):
            i=0
            for Edge in self.edges:
                if self.edges[i].dest == home and self.edges[i].home == dest:
                    self.edges.remove(self.edges[i])
                    break
                i+=1

        i = 0
        for Node in self.nodes:
            del self.nodes[i].adjacent_cities[:]
            self.nodes[i].get_adjacent_cities(self.edges)
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
            query = input("(1) Get all cities (2) Get information on specific city (3) Statistics"
                          "(4) Edit network (5) Get information on specific route (exit) Quit\n")
            if query == 'exit':
                break
            if query == '1':
                self.get_all_cities()
            if query == '2':
                self.get_city_info()
            if query == '3':
                self.get_stats()
            if query == '4':
                self.edit_network()
            if query == '5':
                city_list = []
                while(1):
                    city = input("Enter city code in route, type 'done' when finished: ")
                    if city == 'done':
                        break
                    city_list.append(city)
                self.get_route_info(city_list)

    #handles option 4
    def edit_network(self):
        while(1):
            query = input("(1) Remove a city (2) Remove a route (3) Add a city (4) Add a route"
                          "(5) Edit a city (6) Save data to JSON file (exit) Quit\n")
            if query == 'exit':
                break
            if query == '1':
                city = input("Type the CODE of the city you would like to remove.")
                self.delete_node(city)
            if query == '2':
                home = input("Type the CODE of the home city you would like to remove.")
                dest = input("Type the CODE of the dest city you would like to remove.")
                both = input("Remove route in both directions? (0) No (1) Yes")
                self.delete_route(home, dest, both)
            if query == '3':
                new_city = input("Type code of new city ")
                new_name = input("Type name of new city ")
                new_country = input("Type country of new city ")
                new_continent = input("Type continent of new city ")
                new_timezone = input("Type timezone of new city ")
                new_lat = input("N or S?")
                new_lat_degree = input("Degrees: ")
                new_long = input("W or E?")
                new_long_degree = input("Degrees: ")
                new_population = input("Type population of new city ")
                new_region = input("Type region of new city ")
                entry = dict()
                entry["metros"] = {'code' : new_city, 'name' : new_name, 'country' : new_country,
                                     'continent' : new_continent, 'timezone' : new_timezone,
                                     'coordinates' : {new_lat : new_lat_degree, new_long : new_long_degree},
                                     'population' : new_population, 'region' : new_region}
                new_node = Node(entry["metros"], self.edges)
                self.nodes.append(new_node)
            if query == '4':
                home = input("Please enter starting city code: ")
                dest = input("Please enter destination city code: ")
                dist = input("Please enter distance between points: ")
                entry = dict()
                entry["ports"] = [home, dest]
                entry["distance"] = dist
                new_edge = Edge(entry)
                self.edges.append(new_edge)
                i=0
                for Node in self.nodes:
                    if(self.nodes[i].code == home):
                        self.nodes[i].adjacent_cities.append({dest : dist})
                    i+=1
            if query == '5':
                self.edit_city()
            if query == '6':
                edit_data = dict()
                edit_data["metros"] = dict()
                edit_data["routes"] = dict()
                i = 0
                for Node in self.nodes:
                    edit_data["metros"][i] = {"code" : self.nodes[i].code, "name" : self.nodes[i].name,
                                              "country" : self.nodes[i].country, "continent" : self.nodes[i].continent,
                                              "timezone" : self.nodes[i].timezone, "coordinates" : self.nodes[i].coords,
                                              "population" : self.nodes[i].population, "region" : self.nodes[i].region}
                    i+=1
                i=0
                for Edge in self.edges:
                    edit_data["routes"][i] = {"ports" : [self.edges[i].home, self.edges[i].dest], "distance" : self.edges[i].distance}
                    i+=1
                with open('map_data_edit.json', 'w') as f:
                    json.dump(edit_data, f)

    def edit_city(self):
        edit_city = input("Choose city to edit (by code): ")
        i=0
        for Node in self.nodes:
            if edit_city == self.nodes[i].code:
                edit_city = self.nodes[i]
            i+=1
        while(1):
            query = input("Which aspect of the city would you like to edit: "
                          "(1) code (2) name (3) country (4) continent (5) timezone (6) coords"
                          "(7) population (8) region")
            if query == 'exit':
                break
            if query == '1':
                query1 = input("Enter new value ")
                edit_city.code = query1
            if query == '2':
                query1 = input("Enter new value ")
                edit_city.name = query1
            if query == '3':
                query1 = input("Enter new value ")
                edit_city.country = query1
            if query == '4':
                query1 = input("Enter new value ")
                edit_city.continent = query1
            if query == '5':
                query1 = input("Enter new value ")
                edit_city.timezone = query1
            if query == '6':
                coords = input("Choose coords to edit: (1) Latitude (2) Longitude")
                if coords == '1':
                    SN = input("North or South?")
                    deg = input("Degrees: ")
                    edit_city[0] = SN
                    edit_city.latitude = deg
                if coords == '2':
                    WE = input("East or West?")
                    deg = input("Degrees: ")
                    edit_city[1] = WE
                    edit_city.latitude = deg
            if query == '7':
                query1 = input("Enter new value ")
                edit_city.population = query1
            if query == '8':
                query1 = input("Enter new value ")
                edit_city.region = query1

    def clear_graph(self):
        del self.nodes[:]
        del self.edges[:]

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

    #calculates cost of trip and time trip will take, then prints values
    #param city_list - list of cities in route
    def get_route_info(self, city_list):
        if not self.check_valid_route(city_list):
            return
        else:
            d = self.get_route_distance(city_list)
            cost = self.get_flight_cost(d)
            print("Cost of trip: ", cost)

    #calculates cost of trip
    #param d_list - list of distances in a given route
    def get_flight_cost(self, d_list):
        cost = 0
        i= 0
        for distance in d_list:
            if i > 6:
                break
            cost += (d_list[i] * (.35 - i*.05))
            i+=1
        return cost

    #creates a list of distances based on a list of cities
    #param city_list - list of cities
    def get_route_distance(self, city_list):
        d = []
        i = 0
        for Node in city_list:
            rt = self.get_route_by_city(city_list[i], city_list[i+1])
            d.append(rt)
            if len(city_list) > i+2:
                i+=1
            else:
                return d

    #finds the distance of a route by passing two nodes
    #param home_node - starting node
    #param dest_node - ending node
    def get_route_by_city(self, home_node, dest_node):
        i = 0
        for Edge in self.edges:
            if self.edges[i].home == home_node.code and self.edges[i].dest == dest_node.code:
                return self.edges[i].distance
            else:
                i+=1
        return 0

    def check_valid_route(self, city_list):
        valid = True

        if len(city_list) < 2:
            return False

        i = 0
        j = 0
        for city in city_list:
            for i in range (0, len(self.nodes)):
                if city_list[j] == self.nodes[i].code:
                    city_list[j] = self.nodes[i]
                    break
            j+=1

        i = 0
        for Node in city_list:
            if city_list[i].code in city_list[i + 1].adjacent_cities\
                    and city_list[i + 1].code not in city_list[i].adjacent_cities:
                valid = False
                return valid
            if len(city_list) > (i + 2):
                i+=1
        return valid

    #finds the shortest path between two cities
    #param home - starting node
    #param dest - destination node
    """def find_shortest_path(self, home, dest):
        unvisited_nodes = self.nodes
        visited_nodes = []

        i=0
        for Node in unvisited_nodes:
            unvisited_nodes[i].distance = sys.maxsize

        curr = home
        curr.distance = 0

        while len(unvisited_nodes) != 0:
            curr = self.min_node(unvisited_nodes)
            unvisited_nodes.remove(curr)
            i = 0
            for city in curr.adjacent_cities:
                path = curr.distance + self.get_route_by_city(curr, curr.adjacent_cities[i])
                if path < curr.adjacent_cities[i].distance:
                    curr.adjacent_cities[i].distance = path
                    curr.adjacent_cities[i].previous = curr
                i+=1
        return

    def min_node(self,list):
        smallest = sys.maxsize
        i = 0
        for Node in list:
            if list[i].distance < smallest:
                smallest = list[i].distance
                ret = list[i]
            i+=1
        return ret"""

x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json', 'C:/Users/Anne/PycharmProjects/Assignment2/cmi_hub.json')
x.user_input()
#x.create_map_URL()