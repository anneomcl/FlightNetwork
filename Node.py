class Node:
    code = ""
    name = ""
    country = ""
    continent = ""
    timezone = -1
    coords = ()
    latitude = -1
    longitude = -1
    population = -1
    region = -1

    #initializes Node based on JSON data
    #param metro - JSON city data
    #param edges - edges associated with Graph
    def __init__(self, metro, edges):
        self.code = metro['code']
        self.name = metro['name']
        self.country = metro['country']
        self.continent = metro['continent']
        self.timezone = metro['timezone']
        self.coords = metro['coordinates']
        if(metro['coordinates'].get('S') != None):

            self.latitude = metro['coordinates']['S']
        else:
            self.latitude = metro['coordinates']['N']

        if(metro['coordinates'].get('E') != None):
            self.longitude = metro['coordinates']['E']
        else:
            self.longitude = metro['coordinates']['W']

        self.population = metro['population']
        self.region = metro['region']
        self.adjacent_cities = [] #list of keys (cities) that correspond to values (distances)
        self.get_adjacent_cities(edges)

    #gets a list of all cities adjacent to this node and updates member variable
    #param edges - edges associated with Graph
    def get_adjacent_cities(self, edges):
        i = 0
        for Edge in edges:
            if edges[i].home == self.code:
                self.adjacent_cities.append({edges[i].dest : edges[i].distance})
            i+=1