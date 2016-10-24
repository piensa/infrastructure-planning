from collections import OrderedDict
from invisibleroads_macros.iterable import OrderedDefaultDict
from invisibleroads_macros.math import divide_safely


def pick_proposed_technology(
        infrastructure_graph, selected_technologies, node_id,
        consumption_threshold_in_kwh_per_year, **keywords):
    d = {}
    proposed_technology = 'unelectrified'
    # If the consumption is below the threshold, choose unelectrified
    x = keywords['final_consumption_in_kwh_per_year']
    if x < consumption_threshold_in_kwh_per_year:
        d['proposed_technology'] = proposed_technology
        return d
    # If the node is connected to the network, choose grid
    if infrastructure_graph.edge[node_id]:
        d['proposed_technology'] = 'grid'
        return d
    d['grid_local_discounted_cost'] = ''
    d['grid_local_levelized_cost_per_kwh_consumed'] = ''
    # Choose best standalone technology
    proposed_cost = float('inf')
    for technology in selected_technologies:
        if technology == 'grid':
            continue
        discounted_cost = keywords[technology + '_local_discounted_cost']
        if discounted_cost < proposed_cost:
            proposed_technology = technology
            proposed_cost = discounted_cost
    d['proposed_technology'] = proposed_technology
    return d


def estimate_proposed_cost_per_connection(
        proposed_technology, final_connection_count, **keywords):
    proposed_cost_per_connection = divide_safely(
        keywords.get(proposed_technology + '_local_discounted_cost', 0),
        final_connection_count, 0)
    return {'proposed_cost_per_connection': proposed_cost_per_connection}


def estimate_total_count_by_technology(
        infrastructure_graph, selected_technologies):
    count_by_technology = OrderedDefaultDict(int)
    for node_id, node_d in infrastructure_graph.cycle_nodes():
        technology = node_d['proposed_technology']
        count_by_technology[technology] += 1
    return {'count_by_technology': count_by_technology}


def estimate_total_discounted_cost_by_technology(
        infrastructure_graph, selected_technologies):
    discounted_cost_by_technology = OrderedDefaultDict(int)
    for node_id, node_d in infrastructure_graph.cycle_nodes():
        technology = node_d['proposed_technology']
        if technology not in selected_technologies:
            continue
        discounted_cost_by_technology[technology] += node_d[
            technology + '_local_discounted_cost']
    return {'discounted_cost_by_technology': discounted_cost_by_technology}


def estimate_total_levelized_cost_by_technology(
        infrastructure_graph, selected_technologies,
        discounted_cost_by_technology):
    discounted_consumption_by_technology = OrderedDefaultDict(int)
    for node_id, node_d in infrastructure_graph.cycle_nodes():
        technology = node_d['proposed_technology']
        if technology not in selected_technologies:
            continue
        discounted_consumption_by_technology[technology] += node_d[
            'discounted_consumption_in_kwh']
    levelized_cost_by_technology = OrderedDict()
    for technology in selected_technologies:
        discounted_cost = discounted_cost_by_technology[technology]
        discounted_consumption = discounted_consumption_by_technology[
            technology]
        levelized_cost_by_technology[technology] = divide_safely(
            discounted_cost, discounted_consumption, 0)
    return {'levelized_cost_by_technology': levelized_cost_by_technology}