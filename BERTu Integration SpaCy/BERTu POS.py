import spacy
from spacy.tokens import Doc
from spacy.language import Language
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

#load BERTu tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("MLRS/BERTu")
model = AutoModelForMaskedLM.from_pretrained("MLRS/BERTu")
fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

#custom spaCy pipeline component for masked word prediction
@Language.factory("bertu_fill_mask")
class BERTuFillMaskComponent:
    def __init__(self, nlp, name):
        self.nlp = nlp
        self.name = name
        self.tokenizer = tokenizer
        self.fill_mask = fill_mask  

    def __call__(self, doc):
        #Replaces each token with [MASK] and predicts possible replacements.
        tokens = [token.text for token in doc]
        results = {}

        #process each word by masking it one at a time
        for i in range(len(tokens)):
            masked_sentence = tokens[:i] + ["[MASK]"] + tokens[i+1:]
            masked_text = " ".join(masked_sentence)

            #get predictions from BERTu
            predictions = self.fill_mask(masked_text)

            #store top predictions for the masked word
            results[tokens[i]] = [pred["token_str"] for pred in predictions[:5]]

        #store predictions in the doc's custom attribute
        doc._.bert_predictions = results
        return doc

#register custom attribute in spaCy
Doc.set_extension("bert_predictions", default={}, force=True)

#create a blank spaCy pipeline and add the BERTu component
nlp = spacy.blank("xx")
nlp.add_pipe("bertu_fill_mask", last=True)

'''# Test the model with a Maltese sentence
text = "Il-qattusa qeda [MASK] fil-ġnien."
doc = nlp(text)

#print masked word predictions
for word, predictions in doc._.bert_predictions.items():
    print(f"Word: {word} → Predictions: {predictions}")'''

#save the spaCy model
nlp.to_disk("spacy_bertu_fill_mask")
