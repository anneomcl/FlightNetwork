import easygui as eg
import sys
from Graph import Graph

paths = ['C:/Users/Anne/PycharmProjects/Assignment2/map_data.json','C:/Users/Anne/PycharmProjects/Assignment2/cmi_hub.json']
x = Graph(paths)

while 1:
    image = "C:/Users/Anne/PycharmProjects/Assignment2/map.gif"
    msg ="Please choose an option."
    title = "CSAir Options"
    choices = ["Cities", "Statistics", "Routes", "Edit" ,"Cancel"]
    choice = eg.buttonbox(msg, title, choices, image)

    if str(choice) == "Cancel":
        sys.exit(0)

    if str(choice) == "Routes":
        title = "Routes"
        msg = "Choose an option"
        choices = ["Route Info", "Find Shortest Path Between Cities"]
        choice = eg.buttonbox(msg, title, choices)

        if str(choice) == "Route Info":
            list = []
            while(1):
                msg = "Enter the CODE of city in VALID route, or type 'done' when finished."
                title = "Enter city in route"
                city = eg.enterbox(msg, title)
                if(city == 'done'):
                    break
                list.append(city)
            cost_and_time = x.get_route_info_GUI(list)
            msg = "Cost of trip: " + str(cost_and_time[0]) + "\n Time trip will take: " +\
                str(cost_and_time[1]) + " hours.\n"
            eg.msgbox(msg)

        if str(choice) == "Find Shortest Path Between Cities":
            msg = "Enter the CODE of the home city."
            title = "Home"
            home = eg.enterbox(msg, title)
            msg = "Enter the CODE of the dest city."
            title = "Destination"
            dest = eg.enterbox(msg, title)

            list = [home, dest]
            msg = "Shortest path between " + str(list[0]) + " and " + str(list[1]) +\
                  " is: " + str(x.find_shortest_path(home,dest,list))
            eg.msgbox(msg)


    if str(choice) == "Statistics":
        msg = "Longest Flight: " + x.get_longest_flight().home +" to " + x.get_longest_flight().dest +\
                      "\nDistance: " + str(x.get_longest_flight().distance)+ "\n\n" +\
            "Shortest Flight: " + x.get_shortest_flight().home+" to " + x.get_shortest_flight().dest +\
                      "\nDistance: " + str(x.get_shortest_flight().distance) + "\n\n" +\
            "Distance of Average Flight: "+ str(x.get_avg_flight())+"\n\n" +\
            "Largest City: " + x.get_big_city().name + "\nPopulation: " + str(x.get_big_city().population)+ " \n\n" +\
            "Smallest City: " + x.get_small_city().name + "\nPopulation: " + str(x.get_small_city().population)+ " \n\n" +\
            "Average City Size: " + str(x.get_avg_city()) + "\n\n"+\
            "Cities w/ Most Connections: " + str(x.get_hub_city()) + " "+"\n\n"
        eg.msgbox(msg)

    if str(choice) == "Edit":
        title = "Edit Network"
        msg = "Choose an option"
        choices = ["Add a city", "Delete a city", "Add a route", "Delete a route", "Save"]
        choice = eg.buttonbox(msg, title, choices)

        if str(choice) == "Delete a route":
            msg = "Enter the CODE of the home city."
            title = "Home"
            home = eg.enterbox(msg, title)
            msg = "Enter the CODE of the dest city."
            title = "Destination"
            dest = eg.enterbox(msg, title)

            x.delete_route(home, dest)

        if str(choice) == "Add a route":
            msg = "Enter the CODE of the home city"
            title = "Home"
            home = eg.enterbox(msg, title)

            msg = "Enter the CODE of the destination city"
            title = "Destination"
            dest = eg.enterbox(msg, title)

            msg = "Enter the distance between the cities"
            title = "Distance"
            distance = eg.enterbox(msg, title)

            x.make_new_route_GUI(home, dest, distance)

        if str(choice) == "Save":
            x.save_to_disk()

        if str(choice) == "Delete a city":
            msg = "Please enter the CODE of the city you want to delete."
            title = "Delete a City"
            delete = eg.enterbox(msg, title)
            x.delete_node(delete)

        if str(choice) == "Add a city":
            msg = "Please enter the information of the city you want to add."
            title = "Add a City"
            fieldValues = []
            fieldNames = ["Name", "Code", "Country", "Continent", "Timezone", "Latitude (N or S)",
                          "Lat. Degrees", "Longitude (E or W)", "Long. Degrees", "Population",
                          "Region"]
            fieldValues = eg.multenterbox(msg, title, fieldNames, fieldValues)
            x.make_new_city_GUI(fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3],
                                fieldValues[4], fieldValues[5], fieldValues[6], fieldValues[7],
                                fieldValues[8], fieldValues[9], fieldValues[10])

    if str(choice) == "Cities":
        msg = "Choose a city to get information: "
        title = "Cities"
        choices = []
        nodes = dict()
        for city in x.nodes:
            choices.append(city.name)
            nodes[city.name] = city
        choice = eg.choicebox(msg, title, choices)
        if choice != ("Add a city" or "Delete a city"):
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