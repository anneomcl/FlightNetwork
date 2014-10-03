from unittest import TestCase
from Graph import Graph

__author__ = 'Anne'


class TestGraph(TestCase):

    def test_import_data(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.data['metros'][6]['code'], "LOS")

    def test_create_nodes(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        i = 0
        for Node in x.nodes:
            if x.nodes[5].code == x.data['metros'][i]['code']:
                self.assertTrue(x.nodes[5].code in x.data['metros'][i]['code'])

    def test_create_edges(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        i = 0
        for Route in x.data['routes']:
            if x.edges[10].home == x.data['routes'][i]['ports'][0]:
                self.assertTrue(x.edges[10].home in x.data['routes'][i]['ports'][0])

    def test_get_hub_city(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_hub_city(), ['Toronto'])

    def test_get_avg_city(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_avg_city(), 11796143.75)

    def test_get_big_city(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_big_city().population, 34000000)

    def test_get_small_city(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_small_city().population, 589900)

    def test_get_avg_flight(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_avg_flight(), 2300.276595744681)

    def test_get_longest_flight(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_longest_flight().distance, 12051)

    def test_get_shortest_flight(self):
        x = Graph('C:/Users/Anne/PycharmProjects/Assignment2/map_data.json')
        self.assertEqual(x.get_shortest_flight().distance, 334)