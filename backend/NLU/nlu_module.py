from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tree import Tree
from nltk import ne_chunk, pos_tag, word_tokenize
from keybert import KeyBERT


class NLU:
    def __init__(self):
        # Sentiment analysis
        nltk.download('vader_lexicon')
        self.sid = SentimentIntensityAnalyzer()

        # Person's name extraction
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

        # General purpose keyword extraction
        self.kw_model = KeyBERT(model='all-mpnet-base-v2')

        # Keyword / topic extraction using candidates
        # initialize to download the model
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')

        # Yes / No question analysis
        # If we want more false positives than false negatives, remove 'done'
        self.yes_no_candidates = ['yes', 'no', 'done']

        # Purpose extraction
        #   no idea what purpose keywords would be good
        self.purpose_candidates = ['wallpaper',
                                   'picture', 'painting', 'bedroom']

        # Request feature extraction
        #   need to take those from the knowledge graph
        self.feature_candidates = ['picasso', 'positivism', 'cubism',
                                   'sunflowers', 'happy', 'sad', 'colorful', 'painting', 'oil']

        self.feature_mapping_dict = {}

    def load_painting_features_from_file(self, filename):
        self.feature_mapping_dict = {}
        self.feature_candidates = []

        with open(filename) as f:
            for line in f:
                (key, val) = line.split(',')
                self.feature_mapping_dict[val] = key
                self.feature_candidates.append(val)

    # A value from -1 to 1 where -1 is bad, 0 is neutral and 1 is good
    def analyze_sentiment(self, text: str) -> float:
        score = self.sid.polarity_scores(text)['compound']
        return score

    # String with persons name or None
    def extract_person_name(self, text: str):
        nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
        for nltk_result in nltk_results:
            if type(nltk_result) == Tree:
                name = ''
                for nltk_result_leaf in nltk_result.leaves():
                    name += nltk_result_leaf[0] + ' '
                if(nltk_result.label() == 'PERSON'):
                    return name[:-1]

        return None

    # Top keyword_no predicted keywords using KeyBert
    def extract_keywords(self, text: str, keyword_no=1):
        keywords = self.kw_model.extract_keywords(text,

                                                  keyphrase_ngram_range=(1, 1),

                                                  stop_words='english',

                                                  highlight=False,

                                                  top_n=keyword_no)

        keywords_list = list(dict(keywords).keys())
        return keywords_list

    def __extract_using_candidates__(self, text, candidates, top_n=1):
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        doc_embedding = model.encode([text])
        candidate_embeddings = model.encode(candidates)
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        #answer = candidates[distances.argsort()[0][-1]]
        keywords = [candidates[index]
                    for index in distances.argsort()[0][-top_n:]]

        return keywords

    # False for a negative answer, True for a positive
    def understand_yes_no(self, text: str) -> bool:
        return (self.__extract_using_candidates__(
            text, self.yes_no_candidates)[-1] == 'yes')

    # The top 1 most likely purpose from among candidate purpose keywords
    def extract_purpose_using_candidates(self, text: str, top_n=1):
        return self.__extract_using_candidates__(text, self.purpose_candidates, top_n)

    # The top 1 most likely purpose from among candidate detail keywords
    def extract_feature_using_candidates(self, text: str, top_n=3):
        features = self.__extract_using_candidates__(
            text, self.feature_candidates, top_n)

        res = [self.feature_mapping_dict[key] for key in features]
        res.reverse()

        return res
