"""
Functions for generating force directed layout links from
the generically formatted JSON provided by the scraper
"""

import json


def get_dept_node_dict(path_to_json, dept_name):
    """Returns a dictionary of node names to the contents of the node"""
    try:
        w = open(path_to_json)
        return json.load(w)[dept_name]
    except IOError as e:
        print e


def generate_node_list(dept_node_dict):
    """Generate a list of JSON objects for a force directed graph

    returns a list of JSON objects, formatted to be used as the node list of
    a force directed graph
    """
    node_list = []
    for key in dept_node_dict:
        node_list.append(dept_node_dict[key])
    return node_list


def generate_node_index_dict(node_list):
    """Returns a dict of node -> position in node_list

    Can be used for creation of links between nodes in d3 force layout
    """
    node_index_dict = {}
    for node in node_list:
        node_index_dict[node["course_id"]] = node_list.index(node)

    return node_index_dict


def generate_links(node_list):
    """Returns a list of maps with connecting source nodes to destination nodes

    The maps in the list always have 2 keys: 'source' and 'target'
    The source is the index of start of the link
    The target is the index of end of the link
    """
    node_index_dict = generate_node_index_dict(node_list)
    link_list = []
    for node in node_list:
        # iterating over the regular prereqs
        for prereq in node["reg_prereqs"]:
            try:
                link_list.append({
                        "source": node_index_dict[prereq],
                        "target": node_index_dict[node["course_id"]]
                                 })
            except KeyError as e:
                print(e, "didn't exist in the deptartment")
    return link_list
