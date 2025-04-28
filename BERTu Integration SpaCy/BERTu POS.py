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
        text = doc.text

        #if the user manually added a [MASK], treat it as a direct fill-mask request
        if "[MASK]" in text:
            try:
                predictions = self.fill_mask(text)
                #only return predictions for the inserted [MASK]
                doc._.bert_predictions = {
                    "[MASK]": [pred["token_str"] for pred in predictions[:5]]
                }
            except Exception as e:
                doc._.bert_predictions = {"[MASK]": [f"Error: {str(e)}"]}
            return doc

        #otherwise, auto-mask each word like before
        tokens = [token.text for token in doc]
        results = {}

        for i in range(len(tokens)):
            masked_sentence = tokens[:i] + ["[MASK]"] + tokens[i+1:]
            masked_text = " ".join(masked_sentence)

            predictions = self.fill_mask(masked_text)
            results[tokens[i]] = [pred["token_str"] for pred in predictions[:5]]

        doc._.bert_predictions = results
        return doc

#register custom attribute in spaCy
Doc.set_extension("bert_predictions", default={}, force=True)

#create a blank spaCy pipeline and add the BERTu component
nlp = spacy.blank("xx")
nlp.add_pipe("bertu_fill_mask", last=True)

#test 1 - automasking every word
print("\n- - Auto-Masking Every Word - -")
text1 = "Il-qattusa qeda torqod fil-ġnien."
doc1 = nlp(text1)

for word, predictions in doc1._.bert_predictions.items():
    print(f"Word: {word} → Predictions: {predictions}")

#test 2+3 - a specific word masked
print("\n- - Specific [MASK] Prediction - -")
text2 = "Il-[MASK] ħabbar il-proposti ġodda"
text3 = "L-[MASK] ħareġ mill-iskola u mar jiekol"
doc2 = nlp(text2)
doc3 = nlp(text3)

for word, predictions in doc2._.bert_predictions.items():
    print(f"Masked Token: {word} → Predictions: {predictions}")


for word, predictions in doc3._.bert_predictions.items():
    print(f"Masked Token: {word} → Predictions: {predictions}")

#save to disk
nlp.to_disk("spacy_bertu_fill_mask")
