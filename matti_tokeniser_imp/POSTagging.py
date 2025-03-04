import malti.tokeniser as mlt
import joblib
from pathlib import Path

"""
DEPENDENCY: pip install malti

This is a Pipeline class that can be used to call the POS tagger for use with the Lemmatizer
"""

class POSTagging:
    def __init__(self):
        self.svm_base_path = Path(__file__).resolve().parent.parent / 'svm_pos'
        self.vectorizer = joblib.load(self.svm_base_path / 'vectorizer.joblib')
        self.model = joblib.load(self.svm_base_path / 'svm_pos_model.joblib')

    def tag_sentence(self, sentence):
        sentence = "Jien għandi ħafna xogħol."
        tokens = mlt.tokenise(sentence)
        features = [{"form": token} for token in tokens]
        features_vec = self.vectorizer.transform(features)
        pos_tags = self.model.predict(features_vec)
        tagged_sentence = list(zip(tokens, pos_tags))
        return tagged_sentence
    
pipeline = POSTagging()
result = pipeline.tag_sentence("Jien għandi ħafna xogħol.")
print(result)