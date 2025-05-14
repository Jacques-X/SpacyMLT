import lemmatiser as l

text =  """
        Din is-sentenza qiegħda hawn sabiex nara kemm jaħdem sew dan l-lemmatiser li bnejna fi grupp.
        """

# Call the lemmatise function from the lemmatiser module
lemmatised_tokens = l.lemmatise(text)

# Print the original text and the lemmatised tokens
print()
print("Original Text:")
print(text)
print()
print("Lemmatised Tokens (Root, POS_tag):")
print(lemmatised_tokens)