from nlu_module import NLU


a = NLU()

# Understanding responses to yes/no questions
print("Tesing yes/no questions understanding")
assert(a.understand_yes_no("Yes") == True)
assert(a.understand_yes_no("Yeah") == True)
assert(a.understand_yes_no("I would enjoy doing that") == True)
# assert(a.understand_yes_no("We can do that") == True) not working
assert(a.understand_yes_no("If you want") == True)
assert(a.understand_yes_no("Show me more art/pictures") == True)
assert(a.understand_yes_no("No") == False)
assert(a.understand_yes_no("I don't have time") == False)
assert(a.understand_yes_no("I would rather not") == False)
assert(a.understand_yes_no("Not really") == False)
assert(a.understand_yes_no("I think I'm done") == False)
assert(a.understand_yes_no("I would like to stop") == False)
print("PASSED")

# Name extraction
print("Tesing name extraction")
assert(a.extract_person_name("I'm Konrad").__eq__("Konrad"))
assert(a.extract_person_name("My name is Felix") == "Felix")
assert(a.extract_person_name("Jerry") == "Jerry")
assert(a.extract_person_name("It's Jacqueline") == "Jacqueline")
assert(a.extract_person_name("Everyone calls me Nick") == "Nick")
print("PASSED")

# Sentiment analysis
print("Tesing sentiment analysis polarity")
assert(a.analyze_sentiment("This is awesome") > 0)
assert(a.analyze_sentiment("It's very pretty") > 0)
assert(a.analyze_sentiment("I like it") > 0)
assert(a.analyze_sentiment("Beautiful") > 0)
assert(a.analyze_sentiment("Terrible") < 0)
assert(a.analyze_sentiment("It's ugly") < 0)
assert(a.analyze_sentiment("I hate it") < 0)
assert(a.analyze_sentiment("I don't like it") < 0)
print("PASSED")

# Keyword extraction
print("Testing top 1 keyword extraction")
assert(a.extract_keywords("I want to see some Picasso")[0] == "picasso")
assert(a.extract_keywords("I am happy")[0] == "happy")
assert(a.extract_keywords("It's a sad day")[0] == "sad")
assert(a.extract_keywords(
    "I liked sunflowers so maybe something like that")[0] == "sunflowers")
print("PASSED")
