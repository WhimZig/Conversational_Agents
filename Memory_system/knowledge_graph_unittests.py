import unittest
from knowledge_graph_mem import *


class TestKnowledgeGraph(unittest.TestCase):

    def test_no_errors(self):
        # Just runs through the most important methods, and makes sure there are no errors
        # Not really informational, but good as a sanity check
        test = KnowledgeGraph()


if __name__ == '__main__':
    unittest.main()
