import lemmatiser as l

text =  """
        Il-misraħ tar-raħal kien armat għall-festa.
        """

# Call the lemmatise function from the lemmatiser module
lemmatised_tokens = l.lemmatise(text)

# Print the original text and the lemmatised tokens
print("Original Text:")
print(text)
print()
print("Lemmatised Tokens (Root, POS_tag):")
print(lemmatised_tokens)