import lemmatiser as l

string = "Bonġu, din is-sentenza hi biss biex nara l-kapaċita tat-tokeniser tal-Malti."

lemmatised_tokens = l.lemmatise(string)
print()
print(string)
print()
print(lemmatised_tokens)
