import nltk
from nltk import word_tokenize


def get_features(text: str):
    # using list comprehensions
    features = {}
    word_list = [word for word in word_tokenize(text.lower())]
    for word in word_list:
        features[word] = True
    return features


input = "What's the best way to split a sentence into words?"
print(get_features(input))
