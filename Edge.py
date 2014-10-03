class Edge:

    ports = ""
    home = ""
    dest = ""
    distance = -1

    #initializes edges for Graph
    #param route - JSON data for all routes
    def __init__(self, route):
        self.home = route['ports'][0]
        self.dest = route['ports'][1]
        self.distance = route['distance']

