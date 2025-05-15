import lemmatiser as l

text =  """
        Il-gvern qassam miljun ewro lil għadd ta’ każini madwar Malta sabiex ikunu jistgħu iwettqu proġetti ta’ fejda għall-komunità jew għall-avvanz mużikali, pirotekniku jew fl-arti tal-armar.
        """

# Call the lemmatise function from the lemmatiser module
lemmatised_tokens = l.lemmatise(text)

# Print the original text and the lemmatised tokens
print("Original Text:")
print(text)
print()
print("Lemmatised Tokens (Root, POS_tag):")
print(lemmatised_tokens)