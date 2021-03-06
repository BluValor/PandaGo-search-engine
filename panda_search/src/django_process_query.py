import panda_search.src.vector_preparator as prep
import panda_search.src.word_matrix as wrdm
import panda_search.src.csv_parser as parser
from nltk.tokenize import TweetTokenizer, sent_tokenize
from scipy.sparse import csr_matrix, lil_matrix
import numpy as np

import django
import os


def make_query_vector(query, all_words):

    tknzr = TweetTokenizer(reduce_len=True)

    text = prep.adjust_text(query)
    text = prep.remove_stop_words(text)

    sent_text = sent_tokenize(text)
    tokenized = []
    for sentence in sent_text:
        words = tknzr.tokenize(sentence)
        for word in words:
            tokenized.append(word)

    stemmed = []
    for word in tokenized:
        tmp = prep.remove_punctuation(word)
        if tmp != '':
            stemmed.append(prep.stem(tmp))

    words_count = prep.count_words(stemmed)

    words_vector = [words_count[word] if word in words_count else 0 for word in all_words.order]
    tfidf = [(n, value) for n, value in enumerate(np.multiply(words_vector, all_words.idf)) if value > 0]

    indexes = [i for i, _ in tfidf]
    lengths = [x for _, x in tfidf]
    tfidf = list(tuple(zip(indexes, lengths / np.linalg.norm(lengths))))

    result = lil_matrix((len(all_words.order), 1), dtype=np.float)

    for y, value in tfidf:
        result[y, 0] = value

    return csr_matrix(result)


def count_correlation(query_vector):

    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panda_go.settings')
    # django.setup()
    from panda_search.models import DataBox

    svd_transform_matrix = DataBox.objects.get(name='svd_transform_matrix').value
    svd_components = DataBox.objects.get(name='svd_components').value
    return query_vector.T.dot(svd_transform_matrix).dot(svd_components)


def process_query(query):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panda_go.settings')
    django.setup()
    from panda_search.models import ArticleBox, DataBox

    words = DataBox.objects.get(name='all_words').value
    query_vector = make_query_vector(query, words)

    correlation = list(tuple(enumerate(count_correlation(query_vector)[0])))
    correlation.sort(key=lambda x: x[1], reverse=True)
    return [ArticleBox.objects.get(id=i + 1) for i, _ in correlation[:15]]


# query = 'Why do health care in the USA is bad?'
# query = 'Donald Trump'
# query = 'Make America great again!'
# query = 'Illegal immigrants in France'
# query = 'City in Europe'
# results = process_query(query)
