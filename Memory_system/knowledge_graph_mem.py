from re import S
import numpy as np
import pandas as pd
import json

# TODO: Make sure I'm not missing any additional important details
# TODO: Create test dataset files, and make sure I can read them in properly
# TODO: Bugtest the existing methods

class KnowledgeGraph:
    def __init__(self, target_user: str = None):
        # First thing, if there's target user we use their information, if there is none, then we use the default graph
        if target_user is None:
            # TODO Fix up the path to the graphs. Right now I'm having them in the same folder as the graphs
            f = open('default.json')
            graph = json.load(f)
            vertexes = graph.keys()
            vert_weights = pd.Series(0, index=vertexes)
        else:
            f = open(target_user + '.json')
            graph = json.load(f)
            # For now I'll just assume the weights are stored in a csv, because that's easier, I guess
            # TODO: Decide on a way of properly storing the vertex weights
            vert_weights = pd.read_csv(target_user + '.csv')

        self.graph = graph
        self.vert_weights = vert_weights

        # I'll just do a count of explore for now, as that is easier to handle
        self.explored = pd.Series(0, index=graph.keys())

        # The way I'm keeping track of keys for now is just having a separate list that stores the name of all the
        #   paintings. That way it is easier to just find the relevant paintings, without having to search much
        # TODO: Decide on a way of reading the paintings list from a text file. A split should be easy enough...
        paintings = open('paintings.txt')
        self.painting_list = paintings

    def find_n_highest_ranked_unexplored_vertexes(self, number : int = 3) -> list:
        """Method to find the n highest ranked unexplored vertexes. These can be art pieces, or they can be topics of discussion

        :param number: Number of highest ranked unexplroed vertices
        :returns
            Ordered list of strings, with the highest ranking vertexes
        """
        temp = self.vert_weights[~self.explored].sort_values()[:number]
        return temp.index

    def modify_weight_of_vertex(self, vertex_to_modify: str, change_value: float) -> None:
        """Modifies the weight of one of the internal vertexes. It will add the change_value to the current value
        being stored, so it does not replace the current value completely.

        Additionally, if the vertex is directly linked to any painting, then the value of that painting is also
        increased with the same value. This is done to make other methods easier to code

        :param vertex_to_modify: the vertex that will be modified
        :param change_value: How much to modify the current vertex by

        :return void"""
        self.vert_weights.loc[vertex_to_modify] += change_value
        # It would make it easier to update the vertex weights of paintings directly here...
        # yeah, that makes things easier
        neighbors = self.graph[vertex_to_modify]
        # This is not the most efficient way, but screw it it works.
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

        result = self.vert_weights.isin(self.painting_list).sort_values()[:count]
        return result
