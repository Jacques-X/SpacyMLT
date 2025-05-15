import lemmatiser as l

text =  """
        Is-sistema tal-booking għall-Blue Lagoon reġgħet daħlet fis-seħħ. Dan wara li l-Qorti rrifjutat it-talba minn operaturi tad-dgħajjes biex twaqqafha għax allegaw diskriminazzjoni.
        """

# Call the lemmatise function from the lemmatiser module
lemmatised_tokens = l.lemmatise(text)

# Print the original text and the lemmatised tokens
print("Original Text:")
print(text)
print()
print("Lemmatised Tokens (Root, POS_tag):")
print(lemmatised_tokens)