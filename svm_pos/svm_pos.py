"""
Important link: https://github.com/kadeeraziz/pashto-pos-tagging/blob/main/svm.ipynb
Dataset origin: https://universaldependencies.org
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
import warnings
from time import time

from sklearn.metrics import make_scorer

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

from   conllu import parse_incr
import pandas as pd

# Absolute variables
TRAIN_PATH = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-train.conllu'
TEST_PATH  = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-test.conllu'
DEV_PATH   = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-dev.conllu'

def load_train():
    return parse_dataset(TRAIN_PATH)

def load_test():
    return parse_dataset(TEST_PATH)

def load_dev():
    return parse_dataset(DEV_PATH)

def parse_dataset(dataset): # Importing "form" and "upos" only as only those are needed.
    data = []

    try:
        with open(dataset, "r", encoding="utf-8") as f:
            for sentence in parse_incr(f):
                
                for token in sentence:
                    token_data = {
                        "form": token["form"],
                        "upos": token["upos"]
                    }
                    data.append(token_data)

        df = pd.DataFrame(data)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{dataset}' was not found.")
        return None

def vectroizer(X_train, X_test, y_train):
    vectorizer = DictVectorizer()  

    # Convert X_train and X_test to a list of dictionaries
    X_train = [dict(row) for row in X_train]
    X_test = [dict(row) for row in X_test]

    #vectorizer.fit(X_train)                                    # Train vectorizer
    X_train_vectorized = vectorizer.fit_transform(X_train)  
    X_test_vectorized  = vectorizer.transform(X_test) 

    return X_train_vectorized, X_test_vectorized

def split(data):
    X_data = data.drop("upos", axis=1)
    y_data = data["upos"]
    return X_data, y_data

def train():
    labels     = np.unique(load_train()["upos"])  # Getting all unique labels from the training data
    f1_scorer  = make_scorer(f1_score, average='macro', labels=labels)
    train_data = load_train()
    test_data  = load_test()

    X_train, y_train = split(train_data)
    X_test, y_test   = split(test_data)

    X_train_vectorized, X_test_vectorized = vectroizer(X_train, X_test, y_train)

    svc = SVC()
    parameters = {'kernel': ['linear', 'rbf'], 'C': [0.1, 1, 10]}

    cv = GridSearchCV(svc, parameters, cv=5, n_jobs=-1, scoring=f1_scorer)
    cv.fit(X_train_vectorized, y_train)

    return cv, X_test_vectorized, y_test

def test(cv, X_test_vectorized, y_test):
    start = time()
    pred_val = cv.predict(X_test_vectorized)
    end = time()

    accuracy  = round(accuracy_score(y_test, pred_val), 4)
    precision = round(precision_score(y_test, pred_val, average='macro'), 4)
    recall    = round(recall_score(y_test, pred_val, average='macro'), 4)
    f1score   = round(f1_score(y_test, pred_val, average='macro'), 4)

    print('Accuracy: {} ' .format(accuracy))
    print('F1-score: {} ' .format(f1score))
    print('Precision: {} '.format(precision))
    print('Recall: {} '   .format(recall))
    print('Latency: {}ms' .format(round((end - start)*1000, 1)))

def get_pos():
    pos = ""

    cv, X_test_vectorized, y_test = train()
    test(cv, X_test_vectorized, y_test)

    return pos