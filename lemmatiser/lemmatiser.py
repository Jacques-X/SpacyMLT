from   pathlib         import Path
import malti.tokeniser as mlt
import joblib

# Define the base directory as the directory where the script is located
base_dir = Path(__file__).resolve().parent

# Loading the vectoriser and SVM model
vectoriser = joblib.load(base_dir / 'vectorizer.joblib')
model      = joblib.load(base_dir / 'svm_pos_model.joblib')


def normalise(tokens):
    """
    Ineħħi l-puntiżżjoni mill-lista ta' tokens u jagħmel l-ittri kollha lower case.
    Filter out punctuation from the list of tokens and convert all letters to lower case.
    """
    punctuation = {'.', ',', ';', ':', '!', '?'}
    return [token.lower() for token in tokens if token not in punctuation]

def whole_plural_filter(token):
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

def broken_plural_filter(token):
    """
    Ineħħii l-formi plurali tal-kelma meta dan hu plural miksur.
    Filter out plural forms of a word when it is a "broken" plural.
    """
    # Implementazzjoni meħtieġa
    return token  # Jekk ma jsibx plural, irritorna l-kelma kif inhi

def filter_tokens(tokens):
    tokens = normalise(tokens)
    return [broken_plural_filter(whole_plural_filter(token)) for token in tokens]

def lemmatise(sentence):
    """
    Lemmatise a word using a rule-based approach.
    """
    tokens = mlt.tokenise(sentence)
    filtered_tokens = filter_tokens(tokens)

    features = [{"form": token} for token in filtered_tokens]
    features_vec = vectoriser.transform(features)
    pos_tags = model.predict(features_vec)
    tagged_sentence = list(zip(tokens, pos_tags))
    return tagged_sentence

# ------------------ TESTING ------------------ 
string = "Bonġu, din is-sentenza hi biss sabiex nara l-kapaċita tat-tokeniser tal-Malti."
lemmatised_tokens = lemmatise(string)
print(lemmatised_tokens)
