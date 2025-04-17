from pathlib import Path
import joblib
import pandas as pd

class SVMPosTagger:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.model_path = self.base_dir / 'svm_pos_model.joblib'
        self.vectorizer_path = self.base_dir / 'vectorizer.joblib'
        
        # Load the model and vectorizer
        print("Loading model and vectorizer...")
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    def predict(self, text):
        # Convert input text to DataFrame format
        df = pd.DataFrame({'form': [text]})
        
        # Transform the input using the same vectorizer
        X = self.vectorizer.transform(df.to_dict(orient="records"))
        
        # Make prediction
        prediction = self.model.predict(X)
        return prediction[0]

def main():
    # Example usage
    tagger = SVMPosTagger()
    
    # Test some words
    test_words = ["siġra", "fjura", "karozza", "belt", "ħanut", "aħmar", "blu", "għani", "fqir", "twil", "bilmod", "malajr", "qatt", "hawn", "fuq", "taħt", "ma'", "imma", "għax", "tmur", "tieħu", "tagħmel", "tara", "tisma'", "tikteb", "tgħid", "taħseb", "titkellem", "toqgħod"]
    
    print("\nTesting predictions:")
    print("-" * 30)
    for word in test_words:
        pos_tag = tagger.predict(word)
        print(f"Word: {word:12} POS Tag: {pos_tag}")

if __name__ == "__main__":
    main()