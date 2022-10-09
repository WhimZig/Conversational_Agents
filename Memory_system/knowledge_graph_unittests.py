import unittest
from knowledge_graph_mem import *


class TestKnowledgeGraph(unittest.TestCase):

    def test_no_errors(self):
        # Just runs through the most important methods, and makes sure there are no errors or exceptions
        # Not really informational, but good as a sanity check
        # Method assumes I'm only working with the default test template
        test_graph = KnowledgeGraph()
        test_graph.find_n_highest_ranked_unexplored_paintings()
        test_graph.find_n_highest_ranked_unexplored_vertexes()
        test_graph.modify_weight_of_vertex('Oil', 1.5)
        test_graph.find_n_highest_ranked_unexplored_paintings()
        test_graph.mark_vertex_as_explored('Oil')
        test_graph.create_new_vertex('Canvas Art', ['Oil'])
        # The storing method isn't tested, so that I don't create too much dummy files

    def test_unexplored_method(self):
        # Gives weight to come vertexes, and makes sure that the returned methods return the highest ranked values
        test_graph = KnowledgeGraph()
        test_graph.modify_weight_of_vertex("Oil", 1.)
        test_graph.modify_weight_of_vertex("Dutch", 2.)
        test_graph.modify_weight_of_vertex("Village", 1.)
        # The reason the values are weird is because the method also increases the value of paintings
        # Default is 3, so we're looking for this
        result = test_graph.find_n_highest_ranked_unexplored_vertexes()
        correct_result = ['The Starry Night', 'The Siesta', 'Dutch']
        self.assertListEqual(result, correct_result)

    def test_correct_painting_weight_modified(self):
        # Modify weights neighboring a painting, now that painting should be worth more
        test_graph = KnowledgeGraph()
        test_graph.modify_weight_of_vertex("Oil", 1.)
        test_graph.modify_weight_of_vertex("Dutch", 2.)
        test_graph.modify_weight_of_vertex("Village", 3.)
        test_graph.modify_weight_of_vertex("Nature", 3.)

        result = test_graph.find_n_highest_ranked_unexplored_paintings(1)
        correct_result = ['The Starry Night']
        self.assertListEqual(result, correct_result)
        # Test passes

    def test_ignoring_explored_vertexes(self):
        # Method will add weight to vertexes and ignore one of them. The ignored vertex should not be returned when
        #   querying results
        test_graph = KnowledgeGraph()
        test_graph.modify_weight_of_vertex("Oil", 1.)
        test_graph.modify_weight_of_vertex("Dutch", 2.)
        test_graph.modify_weight_of_vertex("Village", 3.)
        test_graph.modify_weight_of_vertex("Nature", 4.)

        test_graph.mark_vertex_as_explored("Nature")
        test_graph.mark_vertex_as_explored("Fine Wind, Clear Morning")
        result = test_graph.find_n_highest_ranked_unexplored_vertexes()
        correct_result = ['The Starry Night', 'The Siesta', 'Village']
        self.assertListEqual(result, correct_result)

    def test_create_new_high_value_vertex(self):
        # Create a vertex, then check it exists because it will have the highest weight for talk count
        test_graph = KnowledgeGraph()
        test_graph.create_new_vertex('random_test', ['Village', 'Dutch', 'Oil'], 5.)

        result = test_graph.find_n_highest_ranked_unexplored_vertexes(1)
        correct_result = ['random_test']
        self.assertListEqual(result, correct_result)

        # This is the only way I can think of making sure that the connections are properly working internally
        #   it's ugly, but it works
        connected_vertexes = test_graph.graph['random_test']
        self.assertListEqual(connected_vertexes, ['Village', 'Dutch', 'Oil'])

        # Now, we check that the connection exists both ways
        # The line looks ugly, but this is just making sure that 'random_test' is a connection for every vertex
        self.assertTrue('random_test' in test_graph.graph['Village'])
        self.assertTrue('random_test' in test_graph.graph['Dutch'])
        self.assertTrue('random_test' in test_graph.graph['Oil'])

    def test_unexplored_topics(self):
        # Gives weight to come vertexes, and makes sure that the returned methods return the highest ranked values.
        #   focuses on the ones that are topics
        test_graph = KnowledgeGraph()
        test_graph.modify_weight_of_vertex("Oil", 1.)
        test_graph.modify_weight_of_vertex("Dutch", 2.)
        test_graph.modify_weight_of_vertex("Village", 3.)
        # The reason the values are weird is because the method also increases the value of paintings
        # Default is 3, so we're looking for this
        result = test_graph.find_n_highest_ranked_unexplored_topics()
        correct_result = ['Village', 'Dutch', 'Oil']
        self.assertListEqual(result, correct_result)


if __name__ == '__main__':
    unittest.main()
