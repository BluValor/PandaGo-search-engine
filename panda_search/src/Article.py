import numpy as np


class Article:
    def __init__(self, id_, title, publication, author, date, content):
        self.id_ = id_
        self.title = title
        self.publication = publication
        self.author = author
        self.date = date
        self.content = content
        self.stemmed = []
        self.words_count = dict()
        self.words_vector = []
        self.tfidf = []

    def __str__(self):
        return ' | '.join([self.id_, self.title, self.publication, self.author, self.date, self.content])

    def fill_vector(self, order):
        self.words_vector = [self.words_count[word] if word in self.words_count else 0 for word in order]


class ArticleContainer:
    def __init__(self):
        self.articles = []

    def append(self, article):
        self.articles.append(article)


class Words:
    def __init__(self):
        self.words = dict()
        self.order = []
        self.idf = []

    def __iadd__(self, other):
        for word in other:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1
        return self

    def make_order(self):
        self.order = [key for key in self.words]

    def calculate_idf(self, count):
        self.idf = [np.log10(count / self.words[word]) for word in self.order]
