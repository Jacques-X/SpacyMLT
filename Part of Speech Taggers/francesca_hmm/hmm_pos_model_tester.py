from pathlib import Path
import joblib

class HMMPosTagger:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.model_path = self.base_dir / 'hmm_pos_model.joblib'

        print("Loading HMM model...")
        self.initial_probs, self.transition_probs, self.emission_probs, self.states = joblib.load(self.model_path)

    def viterbi(self, obs):
        V = [{}]
        path = {}

        for state in self.states:
            V[0][state] = self.initial_probs.get(state, 0.0001) * self.emission_probs.get(state, {}).get(obs[0], 0.0001)
            path[state] = [state]

        for t in range(1, len(obs)):
            V.append({})
            new_path = {}

            for curr_state in self.states:
                (prob, prev_state) = max(
                    (V[t-1][prev] * self.transition_probs.get(prev, {}).get(curr_state, 0.0001) *
                     self.emission_probs.get(curr_state, {}).get(obs[t], 0.0001), prev)
                    for prev in self.states
                )
                V[t][curr_state] = prob
                new_path[curr_state] = path[prev_state] + [curr_state]

            path = new_path

        (prob, state) = max((V[-1][y], y) for y in self.states)
        return path[state]

    def predict(self, word):
        tag_sequence = self.viterbi([word])
        return tag_sequence[0] if tag_sequence else "UNKNOWN"

def main():
    tagger = HMMPosTagger()

    # Test set of words
    test_words = [
    "siġra", "fjura", "karozza", "belt", "ħanut", "aħmar", "blu", "għani", "fqir", "twil",
    "bilmod", "malajr", "qatt", "hawn", "fuq", "taħt", "ma'", "imma", "għax",
    "tmur", "tieħu", "tagħmel", "tara", "tisma'", "tikteb", "tgħid", "taħseb", "titkellem", "toqgħod"
]


    print("\nTesting predictions:")
    print("-" * 30)
    for word in test_words:
        tag = tagger.predict(word)
        print(f"Word: {word:12} POS Tag: {tag}")

if __name__ == "__main__":
    main()