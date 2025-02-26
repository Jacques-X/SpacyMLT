"""
Dataset origin: https://universaldependencies.org
"""

from   sklearn.metrics            import accuracy_score, classification_report
from   sklearn.feature_extraction import DictVectorizer
from   conllu                     import parse_incr
from   sklearn.svm                import SVC
import pandas                     as pd
import warnings
import joblib

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Paths
TRAIN_PATH = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-train.conllu'
TEST_PATH  = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-test.conllu'
DEV_PATH   = '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/datasets/mt_mudt-ud-dev.conllu'

# Load data
def load_data(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for sentence in parse_incr(f):
            for token in sentence:
                data.append({"form": token["form"], "upos": token["upos"]})
    return pd.DataFrame(data)

# Feature extraction
def vectorizer(X_train, X_test):
    vec = DictVectorizer()
    X_train = X_train.to_dict(orient="records")
    X_test = X_test.to_dict(orient="records")
    return vec.fit_transform(X_train), vec.transform(X_test)

def train_model():
    print("Loading training data...")
    df_train = load_data(TRAIN_PATH)
    print("Loading testing data...")
    df_test = load_data(TEST_PATH)

    df_train = df_train.dropna()
    df_test  = df_test.dropna()

    X_train, X_test = df_train[["form"]], df_test[["form"]]
    y_train, y_test = df_train["upos"], df_test["upos"]

    print("Vectorizing data...")
    X_train_vec, X_test_vec = vectorizer(X_train, X_test)

    print("Training SVM classifier...")
    svm_clf = SVC(kernel='linear', C=1.0)
    svm_clf.fit(X_train_vec, y_train) 

    print("Making predictions...")
    y_pred = svm_clf.predict(X_test_vec)

    print("Saving model...")
    joblib.dump(svm_clf, '/Users/jacquesx/My Drive/Semester 2/ICS2000- GAPT/SpacyMLT/svm_pos/svm_pos_model.joblib')

    # Evaluation
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

train_model()