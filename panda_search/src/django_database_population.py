import panda_search.src.csv_parser as parser
import panda_search.src.vector_preparator as prep
import panda_search.src.word_matrix as wrdm
import panda_search.src.process_query as pq
from scipy.sparse import csr_matrix
import pickle

import django
import os


def populate_articles():
    print('Populating Database...')
    articles = parser.load_articles()
    i = 21962
    for a in articles:
        ArticleBox.objects.create(title=a.title,
                                  publication=a.publication,
                                  author=a.author,
                                  date=a.date,
                                  content=a.content)
        print(i)
        i += 1

    print('Done.')


def populate_other_data():
    print('Cleaning current DataBox objects...')
    DataBox.objects.all().delete()
    print('Populating Words...')
    DataBox.objects.create(name='all_words')
    DataBox.objects.get(name='all_words').set_data(prep.load_words_frequency())
    print('Populating SVD transform matrix...')
    DataBox.objects.create(name='svd_transform_matrix')
    DataBox.objects.get(name='svd_transform_matrix').set_data(wrdm.load_matrix(file_name='svd_transform_matrix'))
    print('Populating SVD components...')
    DataBox.objects.create(name='svd_components')
    DataBox.objects.get(name='svd_components').set_data(wrdm.load_matrix(file_name='svd_components'))
    print('Done.')


if __name__ == '__main__':
    print('Starting PandaGo database population script...')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panda_go.settings')
    django.setup()
    from panda_search.models import ArticleBox, DataBox
    # populate_articles()
    # populate_other_data()
    print('Database populated.')
