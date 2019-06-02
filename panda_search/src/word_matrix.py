import panda_search.src.Article as art
import panda_search.src.csv_parser as parser
import panda_search.src.vector_preparator as prep
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
import pickle
from sklearn.decomposition import TruncatedSVD


def save_matrix(matrix, file_name='words_matrix'):
    with open(file_name, 'wb') as matrix_dump:
        pickle.dump(matrix, matrix_dump)


def load_matrix(file_name='words_matrix'):
    with open('./' + file_name, 'rb') as matrix_dump:
        return pickle.load(matrix_dump)


def build_matrix(articles_name='article_objects_normalized', words_name='all_words', load=False):

    if not load:
        print('Obtaining files...')
        articles = parser.load_articles(file_name=articles_name)
        words = prep.load_words_frequency(file_name=words_name)

        print("Building matrix...")
        result = lil_matrix((len(words.order), len(articles)), dtype=np.float)

        for x in range(len(articles)):
            for y, value in articles[x].tfidf:
                result[y, x] = value

        result = csr_matrix(result)
        save_matrix(result)

    else:
        result = load_matrix()

    print('SVD decomposition...')

    svd = TruncatedSVD(n_components=300, algorithm='arpack', tol=1.0e-14)
    svd_transform_matrix = svd.fit_transform(result)
    save_matrix(svd_transform_matrix, file_name='svd_transform_matrix')
    save_matrix(svd.components_, file_name='svd_components')


# build_matrix()
