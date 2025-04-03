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

def whole_plural_filter(token: str) -> str:
    """
    Ineħħi l-formi plurali tal-kelma meta dan hu plural sħiħ.
    Filter out plural forms of a word when it is a "whole" plural.
    """
    plural_forms = ['ijiet', 'jiet', 'i', 's']
    for form in plural_forms:
        if len(token) > 4: # Prevent removing i/s which are not plural
            if token.endswith(form):
                return token[:-len(form)]
    return token

def broken_plural_filter(token: str) -> str:
    """
    Ineħħii l-formi plurali tal-kelma meta dan hu plural miksur.
    Filter out plural forms of a word when it is a "broken" plural.
    """
    # Implementazzjoni meħtieġa
    return token  # Jekk ma jsibx plural, irritorna l-kelma kif inhi

def filter_tokens(tokens: list) -> list:
    tokens = normalise(tokens)
    return [broken_plural_filter(whole_plural_filter(token)) for token in tokens]

def lemmatise(sentence: str) -> list:
    """
    Lemmatizza s-sentenza b'sett ta' regoli.
    Lemmatise the sentence using a rule-based approach.
    """
    print("Lemmatising...")

    tokens = mlt.tokenise(sentence)
    filtered_tokens = filter_tokens(tokens)

    features = [{"form": token} for token in filtered_tokens]
    features_vec = vectoriser.transform(features)
    pos_tags = model.predict(features_vec)
    
    roots = [r.find_root(token) for token in filtered_tokens]
    tagged_sentence = list(zip(roots, pos_tags))
    return tagged_sentence