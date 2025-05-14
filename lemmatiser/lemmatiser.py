from   pathlib         import Path
import malti.tokeniser as mlt
import root            as r
import joblib

# Define the base directory as the directory where the script is located
base_dir = Path(__file__).resolve().parent

# Loading the vectoriser and SVM model
vectoriser = joblib.load(base_dir / 'vectorizer.joblib')
model      = joblib.load(base_dir / 'svm_pos_model.joblib')

def normalise(tokens: list) -> list:
    """
    Ineħħi l-puntiżżjoni mill-lista ta' tokens u jagħmel l-ittri kollha lower case.
    Filter out punctuation from the list of tokens and convert all letters to lower case.
    """
    punctuation = {'.', ',', ';', ':', '!', '?'}
    return [token.lower() for token in tokens if token not in punctuation]

def lemmatise(sentence: str) -> list:
    """
    Lemmatizza s-sentenza b'sett ta' regoli.
    Lemmatise the sentence using a rule-based approach.
    """
    print("Lemmatising...")

    tokens = mlt.tokenise(sentence)

    print(tokens)
    print("\n\n")

    features = [{"form": token} for token in tokens]
    features_vec = vectoriser.transform(features)
    pos_tags = model.predict(features_vec)
    
    roots = [r.find_root(token, pos_tag) for token, pos_tag in zip(tokens, pos_tags)]
    tagged_sentence = list(zip(roots, pos_tags))
    return tagged_sentence