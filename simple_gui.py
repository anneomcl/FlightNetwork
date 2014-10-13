import easygui as eg
import sys
from Graph import Graph

paths = ['C:/Users/Anne/PycharmProjects/Assignment2/map_data.json','C:/Users/Anne/PycharmProjects/Assignment2/cmi_hub.json']
x = Graph(paths)

while 1:
    image = "C:/Users/Anne/PycharmProjects/Assignment2/map.gif"
    msg ="Please choose an option."
    title = "CSAir Options"
    choices = ["Cities", "Statistics", "Routes", "Cancel"]
    choice = eg.buttonbox(msg, title, choices, image)

    if str(choice) == "Cancel":
        sys.exit(0)

    if str(choice) == "Routes":
        pass

    hub = x.get_hub_city()
    if str(choice) == "Statistics":
        msg = "Longest Flight: " + x.get_longest_flight().home +" to " + x.get_longest_flight().dest +\
                      "\nDistance: " + str(x.get_longest_flight().distance)+ "\n\n" +\
            "Shortest Flight: " + x.get_shortest_flight().home+" to " + x.get_shortest_flight().dest +\
                      "\nDistance: " + str(x.get_shortest_flight().distance) + "\n\n" +\
            "Distance of Average Flight: "+ str(x.get_avg_flight())+"\n\n" +\
            "Largest City: " + x.get_big_city().name + "\nPopulation: " + str(x.get_big_city().population)+ " \n\n" +\
            "Smallest City: " + x.get_small_city().name + "\nPopulation: " + str(x.get_small_city().population)+ " \n\n" +\
            "Average City Size: " + str(x.get_avg_city()) + "\n\n"+\
            "Cities w/ Most Connections: " + str(hub) + " "+"\n\n"
        eg.msgbox(msg)

    if str(choice) == "Cities":
        msg = "Choose a city to get information: "
        title = "Cities"
        choices = []
        nodes = dict()
        for city in x.nodes:
            choices.append(city.name)
            nodes[city.name] = city
        choice = eg.choicebox(msg, title, choices)
        node = nodes[str(choice)]
        msg = "What would you like to know about this city?"
        title = "City Info"
        msg = "Name: " + node.name + "\n" +\
              "Code: " + node.code + "\n" +\
            "Country: " + node.country + "\n"+\
            "Continent: " + node.continent + "\n"+\
            "Timezone: " + str(node.timezone) + "\n"+\
            "Coordinates: " + str(node.coords) + "\n"+\
            "Population: " + str(node.population) + "\n"+\
            "Region: " + str(node.region) + "\n"+\
            "Connected Cities (CODE, DIST): \n" + str(node.adjacent_cities) + "\n"

        eg.msgbox(msg)

    '''if str(choice) == "Map":
        image = "C:/Users/Anne/PycharmProjects/Assignment2/map.gif"
        msg = "Map of CSAir Network"
        title = "CSAir Map"
        eg.buttonbox(msg, title, choices, image)'''

    ''' msg = "Do you want to continue?"
    title = "Please Confirm"
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)           # user chose Cancel'''