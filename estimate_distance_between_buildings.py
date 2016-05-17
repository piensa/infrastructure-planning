from argparse import ArgumentParser
from geopy.distance import vincenty as get_distance
from invisibleroads_macros.log import format_summary
from networkx import Graph
from networkx.algorithms import minimum_spanning_tree
from pandas import read_csv


def run(buildings_geotable):
    graph = Graph()
    for index, row in buildings_geotable.iterrows():
        graph.add_node(index, {
            'lat': row['Latitude'], 'lon': row['Longitude']})
    for node1_id in xrange(min(graph), max(graph)):
        for node2_id in xrange(node1_id + 1, max(graph) + 1):
            node1_d = graph.node[node1_id]
            node2_d = graph.node[node2_id]
            node1_ll = node1_d['lat'], node1_d['lon']
            node2_ll = node2_d['lat'], node2_d['lon']
            distance = get_distance(node1_ll, node2_ll).m
            graph.add_edge(node1_id, node2_id, weight=distance)
    tree = minimum_spanning_tree(graph)
    total_distance = sum(edge_d[
        'weight'] for node1_id, node2_id, edge_d in tree.edges(data=True))
    building_count = len(graph)
    average_distance = total_distance / float(building_count)
    return [
        ('total_distance_between_buildings_in_meters', total_distance),
        ('building_count', building_count),
        ('average_distance_between_buildings_in_meters', average_distance),
    ]


if __name__ == '__main__':
    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        '--buildings_geotable_path',
        metavar='PATH', required=True)

    args = argument_parser.parse_args()
    d = run(
        read_csv(args.buildings_geotable_path))
    print(format_summary(d))
