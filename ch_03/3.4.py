import string
import math

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

# nltk.download("punkt")
# nltk.download("stopwords")


def read_documents():
    f = open("../datasets/CISI/CISI.ALL")
    merged = ""

    for a_line in f.readlines():
        if a_line.startswith("."):
            merged += "\n" + a_line.strip()
        else:
            merged += " " + a_line.strip()

    documents = {}
    content = ""
    doc_id = ""

    for a_line in merged.split("\n"):
        if a_line.startswith(".I"):
            doc_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".X"):
            documents[doc_id] = content
            content = ""
            doc_id = ""
        else:
            content += a_line.strip()[3:] + " "

    f.close()
    return documents


documents = read_documents()


def read_queries():
    f = open("../datasets/CISI/CISI.QRY")
    merged = ""

    for a_line in f.readlines():
        if a_line.startswith("."):
            merged += "\n" + a_line.strip()
        else:
            merged += " " + a_line.strip()

    queries = {}

    content = ""
    qry_id = ""

    for a_line in merged.split("\n"):
        if a_line.startswith(".I"):
            if not content == "":
                queries[qry_id] = content
                content = ""
                qry_id = ""
            qry_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".W") or a_line.startswith(".T"):
            content += a_line.strip()[3:] + " "
    queries[qry_id] = content
    f.close()

    return queries


queries = read_queries()


def read_mappings():
    f = open("../datasets/CISI/CISI.REL")

    mappings = {}

    for a_line in f.readlines():
        voc = a_line.strip().split()
        key = voc[0].strip()
        current_value = voc[1].strip()
        value = []
        if key in mappings.keys():
            value = mappings.get(key)
        value.append(current_value)
        mappings[key] = value

    f.close()
    return mappings


mappings = read_mappings()


def get_words(text: str):
    word_list = [word for word in word_tokenize(text.lower())]
    return word_list


doc_words = {}
qry_words = {}

for doc_id in documents.keys():
    doc_words[doc_id] = get_words(documents.get(doc_id))

for qry_id in queries.keys():
    qry_words[qry_id] = get_words(queries.get(qry_id))

print(len(doc_words))
print(doc_words.get("1"))
print(len(doc_words.get("1")))
print(len(qry_words))
print(qry_words.get("1"))
print(len(qry_words.get("1")))


def retrieve_documents(doc_words, query):
    docs = []
    for doc_id in doc_words.keys():
        found = False
        i = 0
        while i < len(query) and not found:
            word = query[i]
            if word in doc_words.get(doc_id):
                docs.append(doc_id)
                found = True
            else:
                i += 1
    return docs


docs = retrieve_documents(doc_words, qry_words.get("3"))

print(docs[:100])
print(len(docs))


def process(text: str):
    stoplist = set(stopwords.words("english"))
    st = LancasterStemmer()
    word_list = [
        st.stem(word)
        for word in word_tokenize(text.lower())
        if not word in stoplist and not word in string.punctuation
    ]
    return word_list


word_list = process(documents.get("27"))
print(word_list)
word_list = process("organize, organizing, organizational, organ, organic, organizer")
print(word_list)


def get_terms(text: str):
    stoplist = set(stopwords.words("english"))
    terms = {}
    st = LancasterStemmer()
    word_list = [
        st.stem(word)
        for word in word_tokenize(text.lower())
        if not word in stoplist and not word in string.punctuation
    ]
    for word in word_list:
        terms[word] = terms.get(word, 0) + 1
    return terms


doc_terms = {}
qry_terms = {}
for doc_id in documents.keys():
    doc_terms[doc_id] = get_terms(documents.get(doc_id))
for qry_id in queries.keys():
    qry_terms[qry_id] = get_terms(queries.get(qry_id))

print(len(doc_terms))
print(doc_terms.get("1"))
print(len(doc_terms.get("1")))
print(len(qry_terms))
print(qry_terms.get("1"))
print(len(qry_terms.get("1")))


def collect_vocabulary():
    all_terms = []
    for doc_id in doc_terms.keys():
        for term in doc_terms.get(doc_id).keys():
            all_terms.append(term)
    for qry_id in qry_terms.keys():
        for term in qry_terms.get(qry_id).keys():
            all_terms.append(term)
    return sorted(set(all_terms))


all_terms = collect_vocabulary()
print(len(all_terms))
print(all_terms[:10])


def vectorize(input_features: dict, vocabulary: list):
    output = {}
    for item_id in input_features.keys():
        features = input_features.get(item_id)
        output_vector = []
        for word in vocabulary:
            if word in features.keys():
                output_vector.append(int(features.get(word)))
            else:
                output_vector.append(0)
        output[item_id] = output_vector
    return output


doc_vectors = vectorize(doc_terms, all_terms)
qry_vectors = vectorize(qry_terms, all_terms)

print(len(doc_vectors))
print(len(doc_vectors.get("1460")))
print(len(qry_vectors))
print(len(qry_vectors.get("112")))


def calculate_idfs(vocabulary: list, doc_features: dict):
    doc_idfs = {}
    for term in vocabulary:
        doc_count = 0
        for doc_id in doc_features.keys():
            terms = doc_features.get(doc_id)
            if term in terms.keys():
                doc_count += 1
        doc_idfs[term] = math.log(
            float(len(doc_features.keys())) / float(1 + doc_count), 10
        )
    return doc_idfs


doc_idfs = calculate_idfs(all_terms, doc_terms)
print(len(doc_idfs))
print(doc_idfs.get("system"))


def vectorize_idf(input_terms: dict, input_idfs, vocabulary: list):
    output = {}
    for item_id in input_terms.keys():
        terms = input_terms.get(item_id)
        output_vector = []
        for term in vocabulary:
            if term in terms.keys():
                output_vector.append(input_idfs.get(term) * float(terms.get(term)))
            else:
                output_vector.append(float(0))
        output[item_id] = output_vector
    return output


doc_vectors = vectorize_idf(doc_terms, doc_idfs, all_terms)  # F
print(len(doc_vectors))
print(len(doc_vectors.get("1460")))
