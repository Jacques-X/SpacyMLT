from   conllu  import parse_incr
from   pathlib import Path
import pandas  as pd

BASE_DIR = Path(__file__).resolve().parent # Gets the base directory of the script itself

# Paths - changed to work relatively to the local PC
if int(input("1. UD-Datasets\n2. New Datasets\n")) == 1:
    TRAIN_PATH = BASE_DIR / 'ud-datasets' / 'mt_mudt-ud-train.conllu'
    TEST_PATH  = BASE_DIR / 'ud-datasets' / 'mt_mudt-ud-test.conllu'
else:
    TRAIN_PATH = BASE_DIR / 'datasets' / 'train.vrt'
    TEST_PATH  = BASE_DIR / 'datasets' / 'test.vrt'

DUMP_PATH  = BASE_DIR / 'svm_pos_model.joblib'

# Load data
def load_conllu_data(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for sentence in parse_incr(f):
            for token in sentence:
                data.append({"form": token["form"], "upos": token["upos"]})
    return pd.DataFrame(data)

def load_vrt_data(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()  # Assuming space-separated values
            if len(parts) >= 2:  # Ensure it has at least form and POS tag
                data.append({"form": parts[0], "upos": parts[1]})
    return pd.DataFrame(data)

def load_data(path):
    if path.suffix == ".conllu":
        return load_conllu_data(path)
    elif path.suffix == ".vrt":
        return load_vrt_data(path)
    else:
        raise ValueError("Unsupported file format.")
