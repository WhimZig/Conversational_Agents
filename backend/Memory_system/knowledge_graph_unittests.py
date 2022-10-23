import unittest
from knowledge_graph_for_real import *


class TestKnowledgeGraph(unittest.TestCase):
    try:
        # There's an error with the format of the original file. Doing a generic AF exception is the only fix I
        # can think of quickly. It's horrible, ugly and not good at all. But it works!
        g = rdflib.Graph()
        g.parse('artgraph-rdf/artgraph-facts.ttl')
    except Exception:
        print('Key error was reached')

    def test_no_errors(self):
        # Just runs through the most important methods, and makes sure there are no errors or exceptions
        # Not really informational, but good as a sanity check
        # Method assumes I'm only working with the default test template
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)
        test_graph.find_n_highest_ranked_unexplored_paintings()
        test_graph.find_n_highest_ranked_unexplored_vertexes()
        test_graph.modify_weight_of_vertex('https://www.gennarovessio.com/artgraph-resources#43', 1.5)
        test_graph.find_n_highest_ranked_unexplored_paintings()
        test_graph.mark_vertex_as_explored('https://www.gennarovessio.com/artgraph-resources#43')
        # The storing method isn't tested, so that I don't create too much dummy files

    def test_unexplored_method(self):
        # Gives weight to come vertexes, and makes sure that the returned methods return the highest ranked values
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#43", 1.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#44", 2.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#45", 1.)
        # The reason the values are weird is that the method also increases the value of paintings
        # Default is 3, so we're looking for this
        result = test_graph.find_n_highest_ranked_unexplored_vertexes()
        correct_result = ['The Starry Night', 'The Siesta', 'Dutch']
        self.assertListEqual(result, correct_result)

    def test_correct_painting_weight_modified(self):
        # Modify weights neighboring a painting, now that painting should be worth more
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#43", 1.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#44", 2.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#45", 3.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#46", 3.)

        result = test_graph.find_n_highest_ranked_unexplored_paintings(1)
        correct_result = ['https://www.gennarovessio.com/artgraph-resources#58319']
        self.assertListEqual(result, correct_result)
        # Test passes

    def test_ignoring_explored_vertexes(self):
        # Method will add weight to vertexes and ignore one of them. The ignored vertex should not be returned when
        #   querying results
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#44", 1.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#45", 2.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#46", 3.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#43", 4.)

        test_graph.mark_vertex_as_explored("https://www.gennarovessio.com/artgraph-resources#43")
        test_graph.mark_vertex_as_explored("https://www.gennarovessio.com/artgraph-resources#42")
        result = test_graph.find_n_highest_ranked_unexplored_vertexes()
        correct_result = ['https://www.gennarovessio.com/artgraph-resources#46',
                          'https://www.gennarovessio.com/artgraph-resources#45',
                          'https://www.gennarovessio.com/artgraph-resources#44']
        self.assertListEqual(result, correct_result)

    def test_unexplored_topics(self):
        # Gives weight to come vertexes, and makes sure that the returned methods return the highest ranked values.
        #   focuses on the ones that are topics
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#43", 1.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#44", 2.)
        test_graph.modify_weight_of_vertex("https://www.gennarovessio.com/artgraph-resources#45", 3.)
        # The reason the values are weird is that the method also increases the value of paintings
        # Default is 3, so we're looking for this
        result = test_graph.find_n_highest_ranked_unexplored_topics()
        correct_result = [URIRef('https://www.gennarovessio.com/artgraph-resources#43'),
                          URIRef('https://www.gennarovessio.com/artgraph-resources#44'),
                          URIRef('https://www.gennarovessio.com/artgraph-resources#45')]
        self.assertListEqual(result, correct_result)

    def test_name_retrieval(self):
        # Given a machine name, make sure that the returned name is correct.
        # The test was passed when I tried it out...
        test_graph = KnowledgeGraphArt(g=TestKnowledgeGraph.g)

        # First testing with an artwork
        res = test_graph.find_string_name_with_machine_name(
            URIRef('https://www.gennarovessio.com/artgraph-resources#58319'))

        self.assertEqual(res, 'Country Boy')

        # Second testing with an arbitrary element
        res = test_graph.find_string_name_with_machine_name(
            URIRef('https://www.gennarovessio.com/artgraph-resources#43'))

        self.assertEqual(res, 'realism')


if __name__ == '__main__':
    unittest.main()
