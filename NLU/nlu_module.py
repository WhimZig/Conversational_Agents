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
        yes_no_keywords = "yes no done"
        count_yes_no = CountVectorizer(
            ngram_range=(1, 1)).fit([yes_no_keywords])
        self.yes_no_candidates = count_yes_no.get_feature_names_out()

        # Purpose extraction
        #   no idea what purpose keywords would be good
        purpose_keywords = "wallpaper picture painting bedroom"
        count_purpose = CountVectorizer(
            ngram_range=(1, 1)).fit([purpose_keywords])
        self.purpose_candidates = count_purpose.get_feature_names_out()

        # Request details extraction
        #   need to take those from the knowledge graph
        details_keywords = "Picasso positivism cubism Sunflowers happy sad colorful painting oil"
        count_details = CountVectorizer(
            ngram_range=(1, 1)).fit([details_keywords])
        self.details_candidates = count_details.get_feature_names_out()

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

    def __extract_using_candidates__(self, text, candidates):
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        doc_embedding = model.encode([text])
        candidate_embeddings = model.encode(candidates)
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        answer = candidates[distances.argsort()[0][-1]]
        return answer

    # False for a negative answer, True for a positive
    def understand_yes_no(self, text: str) -> bool:
        return (self.__extract_using_candidates__(
            text, self.yes_no_candidates) == 'yes')

    # The top 1 most likely purpose from among candidate purpose keywords
    def extract_purpose_using_candidates(self, text: str):
        return self.__extract_using_candidates__(text, self.purpose_candidates)

    # The top 1 most likely purpose from among candidate detail keywords
    def extract_details_using_candidates(self, text: str):
        return self.__extract_using_candidates__(text, self.details_candidates)
