"""
Dataset origin: https://universaldependencies.org
"""

from   sklearn.metrics            import accuracy_score, classification_report
from   sklearn.feature_extraction import DictVectorizer
from   conllu                     import parse_incr
from   sklearn.svm                import SVC
from   pathlib                    import Path
import pandas                     as pd
import warnings
import joblib

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_DIR = Path(__file__).resolve().parent # Gets the base directory of the script itself

# Paths - changed to work relatively to the local PC
if (input("1. UD-Datasets\n2. New Datasets")):
    TRAIN_PATH = BASE_DIR / 'ud-datasets' / 'mt_mudt-ud-train.conllu'
    TEST_PATH  = BASE_DIR / 'ud-1datasets' / 'mt_mudt-ud-test.conllu'
else:
    TRAIN_PATH = BASE_DIR / 'datasets' / 'mt_train.vrt'
    TEST_PATH  = BASE_DIR / 'datasets' / 'mt_test.vrt'

DUMP_PATH  = BASE_DIR / 'svm_pos_model.joblib'

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
    X_train_vec = vec.fit_transform(X_train)
    X_test_vec = vec.transform(X_test)
    return X_train_vec, X_test_vec, vec  # Returns the vectorizer itself

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
    X_train_vec, X_test_vec, vec = vectorizer(X_train, X_test)

    print("Training SVM classifier...")
    svm_clf = SVC(kernel='linear', C=1.0)
    svm_clf.fit(X_train_vec, y_train) 

    print("Making predictions...")
    y_pred = svm_clf.predict(X_test_vec)

    print("Saving model...")
    joblib.dump(svm_clf, DUMP_PATH)
    joblib.dump(vec, BASE_DIR / 'vectorizer.joblib') 

    # Evaluation
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

train_model()