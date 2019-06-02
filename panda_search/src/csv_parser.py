import csv
import sys
import pickle
import panda_search.src.Article as art


def parse_articles(path, container):

    csv.field_size_limit(sys.maxsize)

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            container.append(art.Article(row['id'], row['title'], row['publication'], row['author'], row['date'],
                                         row['content']))


def parse_and_serialize_articles(file_name='article_objects'):

    container = art.ArticleContainer()

    parse_articles('./all-the-news/articles1.csv', container)
    parse_articles('./all-the-news/articles2.csv', container)
    # parse_articles('./all-the-news/articles3.csv', container)

    container.articles = container.articles[:60000]

    with open(file_name, 'wb') as article_dump:
        pickle.dump(container, article_dump)


def serialize_articles(articles, file_name='article_objects'):

    container = art.ArticleContainer()
    container.articles = articles

    with open(file_name, 'wb') as article_dump:
        pickle.dump(container, article_dump)


def load_articles(file_name='article_objects'):
    with open('./' + file_name, 'rb') as article_dump:
        return pickle.load(article_dump).articles
