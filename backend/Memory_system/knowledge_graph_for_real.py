import numpy as np
import pandas as pd
from os.path import exists
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS, OWL, FOAF

import json

artgraph_prefix = 'https://www.gennarovessio.com/artgraph-schema#'
artgraph_res_prefix = 'https://www.gennarovessio.com/artgraph-resources#'


class KnowledgeGraphArt:
    def __init__(self, target_user: str = None, g: rdflib.Graph = None):
        """KnowledgeGraph class, meant to be used as the working memory for the conversational agent later in the
        project.

        Stores a predefined set of labels as well as their connections inside of it, the weights associated with
         each vertex, as well as giving methods to access and modify values within the graph itself.

        :param target_user: Used to identify the current user. In case no user is given, a default graph with 0 weights
            is used at the start.
        """
        # First thing, if there's target user we use their information, if there is none, then we use the default graph
        if g is None:
            try:
                # There's an error with the format of the original file. Doing a generic AF exception is the only fix I
                # can think of quickly. It's horrible, ugly and not good at all. But it works!
                g = rdflib.Graph()
                g.parse('artgraph-rdf/artgraph-facts.ttl')
            except Exception:
                print('Key error was reached')

        d = {}
        with open("listing_of_elements/machine_object_both.txt") as f:
            for line in f:
                (key, val) = line.split()
                d[key] = val
                d[val] = key

        self.objects_list = d

        # TODO: Painting list might not be relevant. It might be worthwhile to remove this from memory, as it's not used
        paintings = open('listing_of_elements/paintings_in_graph.txt', 'r')
        paintings_str = paintings.read()
        self.painting_list = paintings_str.split('\n')

        machine_name_list = open('listing_of_elements/machine_names_objects.txt', 'r')
        machine_name_list = machine_name_list.read().split('\n')

        if target_user is not None and exists('UserVertexWeights/' + target_user + '.csv'):
            vert_weights = pd.read_csv('UserVertexWeights/' + target_user + '.csv')
        else:
            # I'll store a separate file with all unique objects. I'll just read it in, in case the user is a new
            #   user
            # TODO: Add the weights, somehow

            vert_weights = pd.Series(0.0, index=machine_name_list, dtype=float)

        # A way of storing the user info, in case it is ever used later on
        self.username = target_user

        self.g = g
        self.vert_weights = vert_weights

        # I'll just do a count of explore for now, as that is easier to handle
        self.explored = pd.Series(0, index=machine_name_list)

    def find_n_highest_ranked_unexplored_vertexes(self, number: int = 3, machine_name=True) -> list:
        """Method to find the n highest ranked unexplored vertexes. These can be art pieces, or they can be topics of
        discussion

        :param machine_name: If True, returns the RLF machine name. Meaning with the weird naming scheme
        :param number: Number of highest ranked unexplroed vertices
        :returns
            Ordered list of strings, with the highest ranking vertexes
        """
        temp = self.vert_weights[self.explored < 1].sort_values(ascending=False)[:number]
        result = temp.index.to_list()

        if machine_name:
            return result
        else:
            for i in range(len(result)):
                result[i] = self.find_string_name_with_machine_name(result[i])

            return result

    def modify_weight_of_vertex(self, vertex_to_modify: str, change_value: float) -> None:
        """Modifies the weight of one of the internal vertexes. It will add the change_value to the current value
        being stored, so it does not replace the current value completely.

        Additionally, if the vertex is directly linked to any painting, then the value of that painting is also
        increased with the same value. This is done to make other methods easier to code. The idea is that you will
        not talk directly about a painting, but you can get an idea of the weight of the painting based on the
        neighboring values.

        :param vertex_to_modify: the vertex that will be modified. Assumes that the string given is the machine name
        :param change_value: How much to modify the current vertex by

        :return void"""
        self.vert_weights.loc[vertex_to_modify] += change_value

        neighbors = self.find_neighboring_nodes(URIRef(vertex_to_modify))

        painting_neighbors = [x for x in neighbors if x in self.painting_list]
        for elem in painting_neighbors:
            self.vert_weights.loc[elem] += change_value

    def find_n_highest_ranked_unexplored_paintings(self, count: int = 3) -> list:
        """Finds what are the paintings with the highest rank. Because paintings are rarely going to be directly
        scored, this method relies on finding the neighbors of each painting and using their scores to estimate the
        score of the painting. The method also focuses only on those paintings that have not been explored yet,
        for the sake of returning only new paintings

        :param count: Number of paintings to explore
        :return list containing the string names of the nth ranked paintings"""

        temp = self.vert_weights[self.vert_weights.index.isin(self.painting_list)]
        # I was having issues removing the paintings based on painting list. This extra line is here to check that out
        result = temp[self.explored < 1].sort_values(ascending=False)[:count]
        result = result.index.to_list()
        return result

    def find_n_highest_ranked_unexplored_topics(self, count: int = 3) -> list:
        """Finds what are the topics with the highest rank. Ignores paintings, so this method is mainly
        helpful for suggesting new conversational topics. The method also focuses only on those topics
        that have not been explored yet, for the sake of returning only new topics

        :param count: Number of topics to explore
        :return list containing the string names of the nth ranked topics"""

        temp = self.vert_weights[~self.vert_weights.index.isin(self.painting_list)]
        result = temp[self.explored < 1].sort_values(ascending=False)[:count]
        result = result.index.to_list()
        return result

    def mark_vertex_as_explored(self, vertex_name: str):
        """Increases the explored count of the given vertex

        :param vertex_name: Increases the explored count of the vertex"""
        self.explored.loc[vertex_name] += 1

    def store_weights(self, new_username: str = None, memory_reduction: float = 0.5):
        """Method to store the currently associated weights with the knowledge graph. Will store them
        in the existing folder. Stores the weights as a text file.

        :param memory_reduction: Value that will multiply the current memory's weights by. Done to reduce the value
            of the current memory when storing it in long term. For now, it's just a constant value multiplying the
            values of the current edges.
        :param new_username: In case the username needs to be changed or updated. The files will be stored under this
            name. If this and the self.username are both None, this method does nothing."""

        # TODO: Modify this method to work with knowledge graph framework
        if new_username is not None:
            username = new_username
        else:
            # It's kind of ugly doing two if else statements like this, but it works and I don't care!
            if self.username is None:
                # So, if there is no existing username, and no new username has been given, then just do nothing
                return
            else:
                username = self.username

        reduced_weights = self.vert_weights * memory_reduction
        reduced_weights.to_csv('UserVertexWeights/' + username + '.csv')

    def find_string_name_with_machine_name(self, machine_name: URIRef, through_graph: False) -> str:
        """Given the machine name in URIRef format of an object, find what the corresponding string name is. In case the
        piece is an art piece, then this method will return the title of the art piece

        Done so that AI can actually talk to humans about subjects in a way that makes sense.

        In case there are multiple names for a given machine name, then this method returns the last name in the graph.

        :param machine_name: URIRef formatted name to search in the graph
        :param through_graph: Searches for the string name through the graph if true. By default, it will use the
            internal double dictionary.
        :returns string name of the relevant object"""

        # First, define if I'm searching for an artwork or just a name. This is because for artworks title makes more
        #   sense as the thing to parse. The objective is for the result to be as human readable as possible
        if through_graph:
            art_type = URIRef('https://www.gennarovessio.com/artgraph-schema#Artwork')

            if (machine_name, RDF.type, art_type) in self.g:
                target_uri = URIRef(artgraph_prefix + 'title')
            else:
                target_uri = URIRef(artgraph_prefix + 'name')

            # Just to deal with errors of it not existing in the graph
            res = 'Not found'
            for s, p, o in self.g.triples((machine_name, target_uri, None)):
                # I'm going to assume that there is only one name. In
                res = o

            return str(res)
        else:
            return self.objects_list[str(machine_name)]

    def machine_to_name_finder(self, to_find: str) -> str:
        """Given either a machine name or a proper name, this method finds its opposite. Meaning, for a machine name
        it finds the human name, and for a human name it finds the machine name.

        :param to_find: The relevant string that will be searched
        :returns The corresponding opposite of the given string"""
        return self.objects_list[to_find]

    def find_neighboring_nodes(self, target_node: URIRef) -> list[URIRef]:
        """Method to return all the immediate neighbors of a given target node. Does not return the relationship, just
        returns that they are somehow related.

        For now, this method assumes that any direction is valid. So (target, p, o) and (s, p, target) are both
        valid items.

        :param target_node: Node that is being targeted for neighbors. It should already be in URIRef format
        :returns A list with all the URIRef that neighbor the given target node"""
        result_list = []
        for s, p, o in self.g.triples((target_node, None, None)):
            result_list.append(o)

        for s, p, o in self.g.triples((None, None, target_node)):
            result_list.append(s)

        return result_list