import panda_search.src.Article as art
import panda_search.src.csv_parser as parser
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer, sent_tokenize
import string
import pickle
import numpy as np


def find_all_words(articles):
    words = dict()
    for article in articles:
        for word in article.stemmed:
            words[word] = 0
    return words


def adjust_text(text):
    return text.replace('—', '-').replace('”', '\"').replace('“', '\"').replace('’', '\'')


def remove_punctuation(text):
    return text.translate(str.maketrans({key: None for key in string.punctuation}))


def remove_stop_words(text):
    tokenized_words = text.split(' ')
    stop_words = stopwords.words('english')
    return ' '.join([word for word in tokenized_words if word not in stop_words])


def stem(word):
    return SnowballStemmer('english').stem(word)


def count_words(text_table):
    counts = dict()
    for word in text_table:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def stem_articles(articles):

    tknzr = TweetTokenizer(reduce_len=True)

    for article in articles:
        text = adjust_text(article.content)
        text = remove_stop_words(text)

        sent_text = sent_tokenize(text)
        text_arr_1 = []
        for sentence in sent_text:
            words = tknzr.tokenize(sentence)
            for word in words:
                text_arr_1.append(word)

        text_arr_2 = []
        for word in text_arr_1:
            tmp = remove_punctuation(word)
            if tmp != '':
                text_arr_2.append(stem(tmp))

        article.stemmed = text_arr_2

    parser.serialize_articles(articles, file_name='article_objects_stemmed')


def count_words_articles(articles):

    for article in articles:
        article.words_count = count_words(article.stemmed)
        article.stemmed = []

    parser.serialize_articles(articles, file_name='article_objects_counts')


def count_words_frequency(articles, file_name='all_words'):

    words = art.Words()

    for article in articles:
        words += article.words_count

    words.make_order()
    words.calculate_idf(len(articles))

    with open(file_name, 'wb') as words_dump:
        pickle.dump(words, words_dump)


def load_words_frequency(file_name='all_words'):
    with open('./' + file_name, 'rb') as words_dump:
        return pickle.load(words_dump)


def make_vectors_articles(words, file_name='article_objects_counts'):

    order = words.order
    idf = words.idf
    articles = parser.load_articles(file_name=file_name)
    # limit = len(articles)

    i = 0
    for article in articles:
        article.fill_vector(order)
        article.words_count = []
        article.tfidf = [(n, value) for n, value in enumerate(np.multiply(article.words_vector, idf)) if value > 0]
        article.words_vector = []
        print(i)
        i += 1

    parser.serialize_articles(articles, file_name='article_objects_vectors')


def normalize_vectors_articles(file_name='article_objects_vectors'):

    articles = parser.load_articles(file_name=file_name)

    for article in articles:
        indexes = [i for i, _ in article.tfidf]
        lengths = [x for _, x in article.tfidf]
        article.tfidf = list(tuple(zip(indexes, lengths / np.linalg.norm(lengths))))

    parser.serialize_articles(articles, file_name='article_objects_normalized')


# nltk.download('stopwords')

# parser.parse_and_serialize_articles()

# articles = parser.load_articles(file_name='article_objects')
# stem_articles(articles)

# articles = parser.load_articles(file_name='article_objects_stemmed')
# count_words_articles(articles)

# articles = parser.load_articles(file_name='article_objects_counts')
# count_words_frequency(articles)

# words = load_words_frequency()
# make_vectors_articles(words)

# normalize_vectors_articles()
