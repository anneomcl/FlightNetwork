import json
import sys
import urllib.request

from PIL import Image

from Node import Node
from Edge import Edge


class Graph:

    data = dict()
    edges = []
    nodes = []

    #initializes Graph
    #param path - file path for JSON file to import
    def __init__(self, paths):
        self.import_data(paths)
        self.create_edges()
        self.create_nodes()

    #imports JSON data into Python
    #param path - file path for JSON file to import
    def import_data(self, paths):
        self.data["metros"] = []
        self.data["routes"] = []

        for path in paths:
            map_data=open(path)
            curr_data = json.load(map_data)
            self.data["metros"]+= (curr_data["metros"])
            self.data["routes"]+= (curr_data["routes"])
            map_data.close()

    #initializes the list of nodes associated with Graph
    def create_nodes(self):
        i = 0
        for key in self.data['metros']:
            self.nodes.append(Node(self.data['metros'][i], self.edges))
            i+=1

    #remove from nodes list, removes all edges w/ this city, redo adjacent_cities
    #param city - must enter the CODE of a city
    def delete_node(self, city):
        #delete nodes
        i = 0
        for Node in self.nodes:
            if city == self.nodes[i].code:
                city_node = self.nodes[i]
                self.nodes.remove(self.nodes[i])
                break
            i+=1

        #delete routes
        i = 0
        for Node in city_node.adjacent_cities:
            self.delete_route(city_node.code, city_node.adjacent_cities[i][0])
            self.delete_route(city_node.adjacent_cities[i][0], city_node.code)
            i+=1

        #update adjacent cities lists
        i = 0
        for Node in self.nodes:
            self.nodes[i].adjacent_cities = []
            self.nodes[i].get_adjacent_cities(self.edges)
            i+=1

    #removes edge in one or both directions
    #param home - CODE of the home city
    #param dest - CODE of the dest city
    def delete_route(self, home, dest):
        i = 0
        for Edge in self.edges:
            if self.edges[i].home == home and self.edges[i].dest == dest:
                self.edges.remove(self.edges[i])
            i+=1

        i = 0
        for Node in self.nodes:
            self.nodes[i].adjacent_cities = []
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
                          "(4) Edit network (5) Get information on specific route (6) Get shortest path"
                          "from a home to a destination (exit) Quit\n")
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
            if query == '6':
                 city_list = []
                 while(1):
                    city = input("Enter city code of home, then dest. Type 'done' when finished: ")
                    if city == 'done':
                        break
                    city_list.append(city)

                 city_list = self.turn_codes_into_nodes(city_list)
                 print("Shortest path between ", city_list[0].code , " and ", city_list[len(city_list) - 1].code , " is ",
              self.find_shortest_path(city_list[0], city_list[len(city_list) - 1], city_list))


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

    #prompts user with options to edit the network
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
                self.delete_route(home, dest)
            if query == '3':
                self.make_new_city()
            if query == '4':
                self.make_new_route()
            if query == '5':
                self.edit_city()
            if query == '6':
                self.save_to_disk()

    #prompts user to create a new city
    def make_new_city(self):
        new_city = input("Type code of new city ")
        new_name = input("Type name of new city ")
        new_country = input("Type country of new city ")
        new_continent = input("Type continent of new city ")
        new_timezone = input("Type timezone of new city ")
        while(1):
            new_lat = input("N or S?")
            if(new_lat == "N" or new_lat == "S"):
                break
        new_lat_degree = input("Degrees: ")
        while(1):
            new_long = input("W or E?")
            if(new_long == "W" or new_long == "E"):
                break
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

    def make_new_city_GUI(self, new_name, new_city, new_country, new_continent, new_timezone,
                          new_lat, new_lat_degree, new_long, new_long_degree, new_population,
                          new_region):
        entry = dict()
        entry["metros"] = {'code' : new_city, 'name' : new_name, 'country' : new_country,
                             'continent' : new_continent, 'timezone' : new_timezone,
                             'coordinates' : {new_lat : new_lat_degree, new_long : new_long_degree},
                             'population' : new_population, 'region' : new_region}
        new_node = Node(entry["metros"], self.edges)
        self.nodes.append(new_node)

    #prompts user to create new route
    def make_new_route(self):
        while(1):
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

    def make_new_route_GUI(self, home, dest, dist):
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

    #saves edited data to new JSON file called map_data_edit.json
    def save_to_disk(self):
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

    #prompts user to edit city
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

    #clears all nodes and edges
    def clear_graph(self):
        del self.nodes[:]
        del self.edges[:]

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
        ret = ""
        for hub in hubs:
            ret += (hub)
        return str(ret)

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
        img = urllib.request.urlopen("http://www.gcmap.com/mapui?P="+url)
        file = open('map.gif', 'wb')
        file.write(img.read())
        file.close()

        #webbrowser.open("http://www.gcmap.com/mapui?P="+url)

    #calculates cost of trip and time trip will take, then prints values
    #param city_list - list of cities in route
    def get_route_info(self, city_list):

        city_list = self.turn_codes_into_nodes(city_list)
        d = self.get_route_distance(city_list)
        cost = self.get_flight_cost(d)
        time = self.get_route_time(d, city_list)
        print("Cost of trip: ", cost)
        print("Time trip will take: ",time, " hours")

    def get_route_info_GUI(self, city_list):
        city_list = self.turn_codes_into_nodes(city_list)
        d = self.get_route_distance(city_list)
        cost = self.get_flight_cost(d)
        time = self.get_route_time(d, city_list)
        ret = [cost, time]
        return ret


    #turns a list of city codes into a list of their respective nodes
    #param city_list - list of cities by codes
    def turn_codes_into_nodes(self, code_list):
        i = 0
        for city in code_list:
            for node in self.nodes:
                if code_list[i] == node.code:
                    code_list[i] = node
            i+=1
        return code_list

    #returns a boolean indicating whether an array of cities forms a valid route
    #param city_list - list of cities to form a route
    def check_valid_route(self, city_list):

        valid = True

        if len(city_list) < 2:
            return False

        found1 = False
        found2 = False

        i = 0
        for node in city_list: #for each city in route
            j = 0
            for city in city_list[i + 1].adjacent_cities[j][0]: #and for each of the next city's adjacent cities
                if city_list[i].code == city_list[i + 1].adjacent_cities[j][0]: #if curr city matches an adj city, is found
                    found1 = True
                    break
                j+=1

            j = 0
            for city in city_list[i].adjacent_cities[j][0]: #and for each of the curr city's adjacent cities
                if city_list[i + 1].code == city_list[i].adjacent_cities[j][0]: #if next city matches an adj city, is found
                    found2 = True
                    break
                j+=1

            if found1 == False or found2 == False:
                return False

            if len(city_list) > (i + 2): #if this iteration is not at the end of the list, do another iteration
                i+=1

            else: #if at the end of the list, do not continue
                break

        return valid

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

    #gets the time a given route will take in total
    #param d_list - list of distances between cities
    #param city_list - list of cities in route
    def get_route_time(self, d_list, city_list):
        j = 0
        #populate city_list with node equivalents
        for city in city_list:
            i = 0
            for item in range (0, len(self.nodes)):
                if city_list[j] == self.nodes[i].code:
                    city_list[j] = self.nodes[i]
                    break
                i+=1
            j+=1

        distance = 0
        for d in d_list:
            distance += d

        time = 0
        if(distance < 400):
            acceleration = 750**2 / (2 * distance/2) #vf^2 = vi^2 + 2ad
            acceleration /= 60 #km per minute
            acceleration /= 60 #km per second
            acceleration *= 1000 #m per second
            time += (2((distance/2) - 0)/(acceleration))**(0.5)#x = vit + 1/2at^2, t = sqrt( 2(x - vit) / a )
            time *= 2 #since the deceleration in the second half of the trip will be the same time

        else:
            acceleration = 750**2 / (2 * 200) #vf^2 = vi^2 + 2ad
            acceleration /= 60 *60 #km per minute^2
            acceleration /= 60 *60 #km per second^2
            acceleration *= 1000 #m per second^2
            time += ((2 * 200 - 0)/acceleration)**(0.5) #x = vit + 1/2at^2, t = sqrt( 2(x - vit) / a )
            time *= 2 #since the deceleration in the second half of the trip will be the same time
            distance_mid = (distance - 400) * 1000 #get m
            velocity_mid = (750 *1000)/(60*60) #to get m per second
            time_mid = distance_mid / velocity_mid
            time += time_mid

        if len(city_list) > 2:
            i = 0
            for city in range(1, len(city_list) - 2):
                #print(i, " ", len(city_list))
                layover = 120 #starts at 120 minutes for 1 connected route
                layover -= 10*(len(city_list[i].adjacent_cities) - 1)
                layover *= 60 #convert to seconds
                time += layover
                i+=1

        time /= (60 * 60) #time is in hours

        return time

    #finds the shortest path between two cities
    #param home - starting node
    #param dest - destination node
    #param city_list - a list of city codes
    def find_shortest_path(self, home, dest, city_list):

        self.turn_codes_into_nodes(city_list)
        home = city_list[0]
        dest = city_list[len(city_list) - 1]


        dist = dict() #keys are nodes
        prev = dict() #keys are nodes
        unvisited_nodes = [] #list of nodes

        dist[home] = 0
        for node in self.nodes:
            if node.code != home.code:
                dist[node] = sys.maxsize
                prev[node] = None
            unvisited_nodes.append(node)

        while unvisited_nodes:
            curr = self.min_node(dist, unvisited_nodes)
            unvisited_nodes.remove(curr)
            if curr != dest:
                adj_copy = curr.adjacent_cities

                for city in adj_copy:
                    path = dist[curr] + city[1]
                    if path < dist[self.find_node(city[0])]:
                        dist[self.find_node(city[0])] = path
                        prev[self.find_node(city[0])] = curr

        seq = []
        u = dest
        while u != home:
            seq.insert(0, u.code)
            u = prev[u]

        ret = ""
        ret += home.code
        ret += " "
        for item in seq:
            ret+=str(item)
            ret+=" "
        return ret

    #finds the minimum node for dijkstra's algorithm
    #param dist_list - list of distances with nodes as keys
    #param nodes_list - list of unvisited nodes
    def min_node(self, dist_list, nodes_list):
        min = sys.maxsize
        min_node = None
        for node in nodes_list:
            if dist_list[node] < min:
                min_node = node
                min = dist_list[node]
        return min_node

    #finds node based on a code
    #param code - node to find
    def find_node(self, code):
        for node in self.nodes:
            if code == node.code:
                return node

#paths = ['C:/Users/Anne/PycharmProjects/Assignment2/map_data.json','C:/Users/Anne/PycharmProjects/Assignment2/cmi_hub.json']
#x = Graph(paths)
#x.create_map_URL()
#x.user_input()