# This is a dumb class made so that I can test stuff and write without worrying about dirtying the main class
#   There should be nothing of value here, at least long term
import numpy as np
import pandas as pd
import json
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS, OWL, FOAF
import rdflib

artgraph_prefix = 'https://www.gennarovessio.com/artgraph-schema#'
artgraph_res_prefix = 'https://www.gennarovessio.com/artgraph-resources#'

g = rdflib.Graph()
g.parse('artgraph-rdf/artgraph-facts.ttl')

paintings = open('listing_of_elements/paintings_in_graph.txt', 'r')
paintings_str = paintings.read()
painting_list = paintings_str.split('\n')

artwork_uri = URIRef('https://www.gennarovessio.com/artgraph-schema#Artwork')
name_uri = URIRef(artgraph_prefix + 'name')

# THE FOLLOWING IS CODE TO CREATE A LINK BETWEEN TOPICS AND MACHINE NAMES!!!!
result_list = set()
for s, p, o in g:
    if p == name_uri:
        # So, now I do an extra check to remove the paintings by checking if s is in painting list
        if not (str(s) in painting_list):
            temp = str(o).replace('-', ' ')
            temp = temp.replace('_', ' ')
            temp = temp.replace(',', ' ')
            result_list.add((str(s), temp))

result_list = list(result_list)

with open('listing_of_elements/human_to_machine.txt', 'w', encoding='utf-8') as f:
    for line in result_list:
        key, value = line[0], line[1]
        #print(key + ',' + value)
        temp = key + ',' + value
        f.write(f"{temp}\n")


d = {}
with open("listing_of_elements/human_to_machine.txt") as f:
    for line in f:
        (key, val) = line.split(',')
        d[key] = val
        d[val] = key
