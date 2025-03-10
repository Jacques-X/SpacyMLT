from   sklearn.metrics import classification_report
from   collections     import defaultdict, Counter
from   pathlib         import Path
import conllu
import joblib

BASE_DIR = Path(__file__).resolve().parent # Gets the base directory of the script itself

# Paths - changed to work relatively to the local PC
# Paths - changed to work relatively to the local PC
if (input("1. UD-Datasets\n2. New Datasets")):
    TRAIN_PATH = BASE_DIR / 'ud-datasets' / 'mt_mudt-ud-train.conllu'
    TEST_PATH  = BASE_DIR / 'ud-datasets' / 'mt_mudt-ud-test.conllu'
else:
    TRAIN_PATH = BASE_DIR / 'datasets' / 'mt_train.vrt'
    TEST_PATH  = BASE_DIR / 'datasets' / 'mt_test.vrt'

DUMP_PATH  = BASE_DIR / 'hmm_pos_model.joblib'

#loading data and parsing sentences (word-tag pairs)
def parse_sentences(path):
    parsed_sentences = []
    with open(path, "r", encoding="utf-8") as f:
        for sentence in conllu.parse_incr(f):
            tokens = [token["form"] for token in sentence]
            pos_tags = [token["upos"] for token in sentence]
            parsed_sentences.append((tokens, pos_tags))
    return parsed_sentences

#train HMM model
def train_hmm(train_data):
    #initialize counts
    initial_counts = Counter()
    transition_counts = defaultdict(Counter)
    emission_counts = defaultdict(Counter)
    tag_counts = Counter()

    #count occurrences of tags, transitions, and emissions
    for sentence in train_data:
        tokens, tags = sentence

        #initial tag counts
        initial_counts[tags[0]] += 1

        for i, tag in enumerate(tags):
            tag_counts[tag] += 1
            emission_counts[tag][tokens[i]] += 1

            if i > 0:
                prev_tag = tags[i - 1]
                transition_counts[prev_tag][tag] += 1

    #convert counts to probabilities
    total_sentences = len(train_data)
    initial_probs = {tag: count / total_sentences for tag, count in initial_counts.items()}

    transition_probs = {
        tag: {next_tag: count / sum(next_tags.values()) for next_tag, count in next_tags.items()}
        for tag, next_tags in transition_counts.items()
    }

    emission_probs = {
        tag: {word: count / sum(words.values()) for word, count in words.items()}
        for tag, words in emission_counts.items()
    }

    return initial_probs, transition_probs, emission_probs, tag_counts.keys()

#viterbi algorithm 
def viterbi(obs, states, start_p, trans_p, emit_p):
    #initialize Viterbi matrix and backpointer path
    V = [{}]
    path = {}

    #initialize base case
    for state in states:
        V[0][state] = start_p.get(state, 0.0001) * emit_p.get(state, {}).get(obs[0], 0.0001)
        path[state] = [state]

    #recursion step
    for t in range(1, len(obs)):
        V.append({})
        new_path = {}

        for curr_state in states:
            (prob, prev_state) = max(
                (V[t-1][prev] * trans_p.get(prev, {}).get(curr_state, 0.0001) * emit_p.get(curr_state, {}).get(obs[t], 0.0001), prev)
                for prev in states
            )
            V[t][curr_state] = prob
            new_path[curr_state] = path[prev_state] + [curr_state]

        path = new_path

    (prob, state) = max((V[-1][y], y) for y in states)
    return path[state]

#evaluate model
def evaluate_model(test_data, states, initial_probs, transition_probs, emission_probs):
    y_true, y_pred = [], []

    #make predictions
    for sentence in test_data:
        words, actual_tags = sentence
        predicted_tags = viterbi(words, states, initial_probs, transition_probs, emission_probs)

        y_true.extend(actual_tags)
        y_pred.extend(predicted_tags)

    print(classification_report(y_true, y_pred, digits=2))

#main execution
def main():
    print("Loading training data...")
    train_sentences = parse_sentences(TRAIN_PATH)

    print("Loading testing data...")
    test_sentences = parse_sentences(TEST_PATH)

    print("Training HMM model...")
    initial_probs, transition_probs, emission_probs, states = train_hmm(train_sentences)

    print("Evaluating model...")
    evaluate_model(test_sentences, states, initial_probs, transition_probs, emission_probs)

if __name__ == "__main__":
    main()
