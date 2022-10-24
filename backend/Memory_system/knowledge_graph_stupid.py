import numpy as np
import pandas as pd
from os.path import exists
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS, OWL, FOAF
import random

import json

artgraph_prefix = 'https://www.gennarovessio.com/artgraph-schema#'
artgraph_res_prefix = 'https://www.gennarovessio.com/artgraph-resources#'


class KnowledgeGraphDumb:
    def __init__(self, target_user: str = None, g: rdflib.Graph = None):
        """KnowledgeGraph class, meant to be used as the working memory for the conversational agent later in the
        project.

        Only remembers what paintings have been seen. Has no way of scoring items, so it is very very dumb and stupid.

        Like us.

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
        with open("Memory_system/listing_of_elements/machine_object_both.txt", encoding='utf8') as f:
            for line in f:
                (key, val) = line.split(',', 1)
                val = val[:-1]
                d[key] = val
                d[val] = key

        self.objects_list = d

        # TODO: Painting list might not be relevant. It might be worthwhile to remove this from memory, as it's not used
        paintings = open('Memory_system/listing_of_elements/paintings_in_graph.txt', 'r')
        paintings_str = paintings.read()
        self.painting_list = paintings_str.split('\n')

        machine_name_list = open('Memory_system/listing_of_elements/machine_names_objects.txt', 'r')
        machine_name_list = machine_name_list.read().split('\n')

        # A way of storing the user info, in case it is ever used later on
        self.username = target_user

        self.g = g

        # I'll just do a count of explore for now, as that is easier to handle
        self.explored = pd.Series(0, index=machine_name_list)

        self.neighbor_paintings = []

    def find_n_highest_ranked_unexplored_vertexes(self, number: int = 3, machine_name=True) -> list:
        """Method to find the n highest ranked unexplored vertexes. These can be art pieces, or they can be topics of
        discussion.

        This method just returns a random unexplored vertex in the stupid version

        :param machine_name: If True, returns the RLF machine name. Meaning with the weird naming scheme
        :param number: Number of highest ranked unexplroed vertices
        :returns
            Ordered list of strings, with the highest ranking vertexes
        """
        temp = self.vert_weights[self.explored < 1]

        result = [None] * number

        for i in range(number):
            result[i] = random.choice(temp)

        if machine_name:
            return result
        else:
            for i in range(len(result)):
                result[i] = self.find_string_name_with_machine_name(result[i])

            return result

    def modify_weight_of_vertex(self, vertex_to_modify: str, change_value: float = 0.2) -> None:
        """This method will store the neighboring paintings in memory. Done so that we can remember the genre used
        somehow, but it still ignores the other information.

        :param vertex_to_modify: the vertex that will be modified. Assumes that the string given is the machine name
        :param change_value: Placeholder value used

        :return void"""

        neighbors = self.find_neighboring_nodes(URIRef(vertex_to_modify))

        painting_neighbors = [x for x in neighbors if x in self.painting_list]
        self.painting_list = painting_neighbors

    def find_n_highest_ranked_unexplored_paintings(self, count: int = 1) -> list:
        """Returns the amount of paintings from the painting list. It makes no guarantees that it will display a
        new painting, it can repeat the painting multiple times

        :param count: Number of paintings to explore
        :return list containing the string names of the nth ranked paintings"""

        result = [None] * count
        for i in range(count):
            result[i] = random.choice(self.painting_list)

        return result

    def find_n_highest_ranked_unexplored_topics(self, count: int = 3) -> list:
        """Finds what are the topics with the highest rank. Ignores paintings, so this method is mainly
        helpful for suggesting new conversational topics. The method also focuses only on those topics
        that have not been explored yet, for the sake of returning only new topics

        :param count: Number of topics to explore
        :return list containing the string names of the nth ranked topics"""

        temp = self.vert_weights[~self.vert_weights.index.isin(self.painting_list)]
        temp = temp[self.explored < 1]

        result = [None] * count
        for i in range(number):
            result[i] = random.choice(temp)

        return result

    def mark_vertex_as_explored(self, vertex_name: str):
        """Increases the explored count of the given vertex

        :param vertex_name: Increases the explored count of the vertex"""
        self.explored.loc[vertex_name] += 1

    def store_weights(self, new_username: str = None, memory_reduction: float = 0.5):
        """Method does nothing, it exists for compatability and to make everything consistent

        :param memory_reduction: Placeholder parameter
        :param new_username: Placeholder parameter"""
        pass

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

    def find_neighboring_nodes(self, target_node: URIRef) -> list:
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

    def update_neighboring_to_painting(self, machine_name_painting: str, sentiment: float) -> None:
        """Method will only mark the painting as visited. Ignores anything else related to the memory, as memory does
        not matter

        :param machine_name_painting: Machine name of the painting that was visited. Painting will be marked as
        read
        :param sentiment: Placeholder, it exists for compatability with other things"""
        self.mark_vertex_as_explored(machine_name_painting)

    def find_artist_medium_period_for_painting(self, machine_painting_name: URIRef) -> tuple:
        """Get all the extra info for a painting, based on the machine name. Means we will look for the relevant
        neighbors. This extra info is what was deemed important to speak about, because reasons"""

        # First is finding the artist
        artist = ''
        for s, p, o in self.g.triples((machine_painting_name, URIRef(artgraph_prefix + 'createdBy'), None)):
            artist = self.find_string_name_with_machine_name(o, False)

        medium = ''
        for s, p, o in self.g.triples((machine_painting_name, URIRef(artgraph_prefix + 'madeOf'), None)):
            medium = self.find_string_name_with_machine_name(o, False)

        period = ''
        for s, p, o in self.g.triples((machine_painting_name, URIRef(artgraph_prefix + 'hasPeriod'), None)):
            period = self.find_string_name_with_machine_name(o, False)

        piece_name = self.find_string_name_with_machine_name(machine_painting_name, True)

        artist = artist.replace('-', ' ').replace('_', ' ')
        medium = medium.replace('-', ' ').replace('_', ' ')
        period = period.replace('-', ' ').replace('_', ' ')

        return piece_name, artist, medium, period

    def add_topic_to_graph(self, topic_to_add: str, cut_off: float = 1.):
        """To keep into account context, the system will have a method to read in a topic and save it withing the
        existing graph. This method will also create a separate graph with the extra information.

        Method assumes that internal values that have a score greater than or equal to the given cut_off value are
        the nodes that should be connected, as the user found them to be interesting enough during the conversation.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        THIS METHOD SHOULD NOT BE USED, AS UPDATING THE GRAPHS IS GOING TO BE RATHER ANNOYING
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param topic_to_add: New topic to include in the graph. Could just be the purpose, or the username of the person
        using the program. It's just a noun as an identifier
        :param cut_off: Cut off score, for determining that something is important enough. It has to be greater than
        or equal to whatever the cut off value is"""

        related_to_uri = URIRef(artgraph_prefix + 'relatedTo')

        # For now, I will focus on getting the relevant cut off value
        topics_to_store = self.vert_weights[self.vert_weights >= cut_off].index.to_list()

        # I'd have to think of the proper RFL format, but this is consistent with the rest so it's good enough
        topic_uri = URIRef(artgraph_prefix + topic_to_add)

        for elem in topics_to_store:
            self.g.add((topic_uri, related_to_uri, elem))
            self.g.add((elem, related_to_uri, topic_uri))

        self.g.serialize(destination='saved_graph.ttl')

    def reset_memory(self):
        """Method to reset the internal memory. Done so that future runnings of the app can manage"""
        self.explored = pd.Series(0., index=self.explored.index)
