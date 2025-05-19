import malti.tokeniser as mlt
import joblib
from pathlib import Path

# Paths
SVM_BASE_PATH = Path(__file__).resolve().parent.parent / 'Part of Speech Taggers/jacques_svm'

# Load the vectorizer and model
vectorizer = joblib.load(SVM_BASE_PATH / 'vectorizer.joblib')
model = joblib.load(SVM_BASE_PATH / 'svm_pos_model.joblib')

# Sentence to tag
sentence = "Dan test għal waqt il-video tal-proġett tal-Universtità ta' Malta."
print(f"\nSentence to tag: {sentence}")

# Step 1: Tokenization
tokens = mlt.tokenise(sentence)
print(f"Tokens: {tokens}")

# Step 2: Feature creation (turn tokens into dict features)
features = [{"form": token} for token in tokens]
print(f"Features: {features}")

# Step 3: Vectorization (convert features into numeric format)
features_vec = vectorizer.transform(features)
print(f"Vectorized Features (shape): {features_vec.shape}")

# Step 4: POS prediction
pos_tags = model.predict(features_vec)
print(f"Predicted POS tags: {pos_tags}")

# Step 5: Combine tokens with tags
tagged_sentence = list(zip(tokens, pos_tags))
print(f"\nTagged sentence: {tagged_sentence}")