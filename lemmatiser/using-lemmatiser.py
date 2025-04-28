import lemmatiser as l

text = """
    Imbagħad tippreokkupani daqsxejn ukoll il-problema tal-konsumiżmu u ta' l-awtoriżmu li diġa hija karatteristika ta' dan is-seklu u nistenna li se tkompli taċċenna ruħha fil-millennju l-ġdid. Naturalment ma tistax iżżomm lura ċertu progress u ċerti kumditajiet, imma naħseb hu serju jekk wieħed jittraskura u jestranja ruħu mis-sempliċitajiet umani, u tVambjent naturali fil-komunita wkoll.
    """

lemmatised_tokens = l.lemmatise(text)
print()
print(text)
print()
print(lemmatised_tokens)
