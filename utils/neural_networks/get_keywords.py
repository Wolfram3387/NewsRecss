import re
import pymorphy2
import nltk

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
from googletrans import Translator

nltk.download('stopwords')

def preprocess_df(text):
    stop_words_ru = set(stopwords.words('russian'))

    new_words_ru = ["фигура", "изображение", "образец", "использование",
                    "показать", "результат", "большой",
                    "также", "ещё", "вообще", "всё", "пока", "вдвое", "такой", "сейчас",
                    "весь", "здесь", "тоже", "какой", "семь", "восемь", "девять", "другой",
                    "каждый", "мочь", "свой", "нужно", "быть", "это", "еще", "несколько",
                    "некоторый", "которые", "оно"]
    stop_words_ru = set(stop_words_ru.union(new_words_ru))

    def pre_process(text, stop_words):
        text = text.lower()
        text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
        text = re.sub("(\\d|\\W)+", " ", text)
        text = text.split()
        text = [word for word in text if word not in stop_words and len(word) >= 3]
        stemmer = pymorphy2.MorphAnalyzer()
        text = [stemmer.parse(word)[0].normal_form for word in text]
        return ' '.join(text)

    text = text.apply(lambda x: pre_process(x, stop_words_ru))

    cv = CountVectorizer(max_features=10000, ngram_range=(1, 3))
    word_count_vector = cv.fit_transform(text)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    return text, cv, tfidf_transformer

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=15):
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results

def get_keywords(text_ru):
    text = text_ru
    text, cv, tfidf_transformer = preprocess_df(text)

    feature_names = cv.get_feature_names_out()
    word_count_vector = cv.transform(text)

    tf_idf_vector = tfidf_transformer.transform(word_count_vector)

    sorted_items = sort_coo(tf_idf_vector.tocoo())

    keywords_ru = extract_topn_from_vector(feature_names, sorted_items, 10)

    translator = Translator()
    keywords_en = translator.translate(' '.join(keywords_ru)).text

    return keywords_en
