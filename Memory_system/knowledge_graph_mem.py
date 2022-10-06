import numpy as np
import pandas as pd
import json
from os.path import exists


# TODO: Make sure I'm not missing any additional important details
# Previous task is hazy AF. It means that I'm not missing important method calls

# TODO: Bugtest the existing methods

class KnowledgeGraph:
    def __init__(self, target_user: str = None):
        """KnowledgeGraph class, meant to be used as the working memory for the conversational agent later in the
        project.

        Stores a predefined set of labels as well as their connections inside of it, the weights associated with
         each vertex, as well as giving methods to access and modify values within the graph itself.

        :param target_user: Used to identify the current user. In case no user is given, a default graph with 0 weights
            is used at the start.
        """
        # First thing, if there's target user we use their information, if there is none, then we use the default graph
        if target_user is not None and exists('UserGraphs/' + target_user + '.json'):
            # For now, I assume that if a user graph exists, then the vertex weights also exist
            f = open('UserGraphs/' + target_user + '.json')
            graph = json.load(f)
            # For now I'll just assume the weights are stored in a csv, because that's easier, I guess
            # TODO: Decide on a way of properly storing the vertex weights
            vert_weights = pd.read_csv('UserVertexWeights/' + target_user + '.csv')
        else:
            # TODO Modify this json family to be the actual file, instead of the temp file I'm using
            f = open('test_default.json')
            graph = json.load(f)
            vertexes = graph.keys()
            vert_weights = pd.Series(0.0, index=vertexes, dtype=float)

        # A way of storing the user info, in case it is ever used later on
        self.username = target_user

        self.graph = graph
        self.vert_weights = vert_weights

        # I'll just do a count of explore for now, as that is easier to handle
        self.explored = pd.Series(0, index=graph.keys())

        # The way I'm keeping track of keys for now is just having a separate list that stores the name of all the
        #   paintings. That way it is easier to just find the relevant paintings, without having to search much
        # TODO: Decide on a way of reading the paintings list from a text file. A split should be easy enough...
        paintings = open('paintings.txt', 'r')
        paintings_str = paintings.read()
        self.painting_list = paintings_str.split('\n')

    def find_n_highest_ranked_unexplored_vertexes(self, number: int = 3) -> list:
        """Method to find the n highest ranked unexplored vertexes. These can be art pieces, or they can be topics of discussion

        :param number: Number of highest ranked unexplroed vertices
        :returns
            Ordered list of strings, with the highest ranking vertexes
        """
        temp = self.vert_weights[self.explored < 1].sort_values()[:number]
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
        # I'm just looking for the neighbors that are paintings
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

        result = self.vert_weights.isin(self.painting_list)[self.explored < 1].sort_values()[:count]
        return result

    def mark_vertex_as_explored(self, vertex_name: str):
        """Increases the explored count of the given vertex

        :param vertex_name: Increases the explored count of the vertex"""
        self.explored.loc[vertex_name] += 1

    def create_new_vertex(self, vertex_name: str, vertexes_it_connects_to: list, vertex_weight: float = 0.0):
        """Method to add a new vertex to the existing graph

        :param vertex_name: Name of the new vertex. In case it already exists in the graph, the method will not create
            a separate instance of the vertex, it will merely update the nodes it connects to
        :param vertexes_it_connects_to: Vertexes connected to this graph. In case the original vertex exists, these
            will be added to the existing edge list
        :param vertex_weight: Vertex weight. Assumed to be 0, can be modified in case it is deemed relevant"""

        if vertex_name in self.graph:
            # So this is the case where the vertex already exists in the graph
            self.graph[vertex_name] = list(set(self.graph[vertex_name] + vertexes_it_connects_to))
        else:
            self.graph[vertex_name] = vertexes_it_connects_to

        self.vert_weights[vertex_name] = vertex_weight
        # Now is the annoying part, of making sure that each of the vertexes it connects to connects back to the
        #   original vertex
        # Can't think of anything better than just looping through everything, so here we go!
        for vert in vertexes_it_connects_to:
            if vertex_name not in self.graph[vert]:
                self.graph[vert].append(vertex_name)

    def store_graph_and_weights(self, new_username: str = None, memory_reduction: float = 0.5):
        """Method to store the currently created knowledge graph, as well as the associated weights. Will store them
        in the existing folder. Stores the graph as a json file, and the weights as a text file.

        :param memory_reduction: Value that will multiply the current memory's weights by. Done to reduce the value
            of the current memory when storing it in long term. For now, it's just a constant value multiplying the
            values of the current edges.
        :param new_username: In case the username needs to be changed or updated. The files will be stored under this
            name. If this and the self.username are both None, this method does nothing."""

        # TODO: Consider making a new vertex in this existing graph, somehow
        if new_username is not None:
            username = new_username
        else:
            # It's kind of ugly doing two if else statements like this, but it works and I don't care!
            if self.username is None:
                return
            else:
                username = self.username

        # Right now this is kind of wortheless, as I'm not adding any new graph points elsewhere...
        with open('UserGraphs/' + username + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=4)

        reduced_weights = self.vert_weights*memory_reduction
        self.reduced_weights.to_csv('UserVertexWeights/' + username + '.csv')


if __name__ == '__main__':
    # So, first I'll just run this...
    test_graph = KnowledgeGraph()
    test_graph_names = KnowledgeGraph('nick')
