from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import numpy as np
import string
import re
import nltk
from nltk.tokenize import word_tokenize
import pymorphy3

app = FastAPI()

with open('./model_knn1.pkl', 'rb') as f:
    model = pickle.load(f)

with open('./vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)



def fun_punctuation_text(text):
    text = text.lower()
    text = ''.join([ch for ch in text if ch not in string. punctuation])
    text = ''.join([i if not i.isdigit() else '' for i in text])
    text = ''.join([i if i. isalpha() else ' ' for i in text])
    text = re. sub(r'\s+', ' ', text, flags=re. I)
    text = re.sub(' [a-z] ', '', text, flags=re.I)
    st = '>\xa0'
    text = ''.join([ch if ch not in st else ' ' for ch in text])
    return text

def fun_lemmatizing_text(text):
    tokens = word_tokenize(text)
    res = list()
    for word in tokens:
        p = pymorphy3.MorphAnalyzer(lang='ru').parse(word)[0]
        res.append(p.normal_form)
    text = " ".join(res)
    return text

def fun_tokenize(text):
    russian_stopwords = nltk.corpus.stopwords.words("russian")
    russian_stopwords.extend(['и', 'в', 'во', 'не', 'что', 'как', 'а', 'он', 'она', 'они', 'это', 'то'])
    t = word_tokenize(text)
    tokens = [token for token in t if token not in russian_stopwords]
    text = " ".join(tokens)
    return text

def fun_pred_text(text):
    text = fun_punctuation_text(text)
    text = fun_lemmatizing_text(text)
    text = fun_tokenize(text)
    return text

def predict_cluster(text):
    text_vectorized = vectorizer.transform([fun_pred_text(text)])
    text_vectorized = text_vectorized[:, :model.n_features_in_]
    prediction = model.predict(text_vectorized)
    probabilities = model.predict_proba(text_vectorized)
    rez1 = f"Класс: {prediction[0]}"
    rez2 = f"Вероятности: {probabilities[0]}"
    mapping = {
        0: 'Кластер 1',
        1: 'Кластер 2',
        2: 'Кластер 3',
        3: 'Кластер 4',
        4: 'Кластер 5',
        5: 'Кластер 6',
        6: 'Кластер 7',
        7: 'Кластер 8',
        8: 'Кластер 9',
        9: 'Кластер 10',
        10: 'Кластер 11',
        11: 'Кластер 12',
        12: 'Кластер 13',
        13: 'Кластер 14',
        14: 'Кластер 15',
    }
    selected_cluster = mapping[prediction[0]]
    return selected_cluster, rez2


class Item(BaseModel):
    text: str

@app.post("/predict")
def post_pred_text(item: Item):
    return {'cluster': predict_cluster(item.text)}