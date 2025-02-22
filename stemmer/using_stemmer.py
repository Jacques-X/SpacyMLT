import stemmer as st

sentence = ["Bonġu", "kif", "int", "jien", "jisimni", "Jacques", "u", "qiegħed", "nivverifika", "l-użu", "tal-lingwa", "Maltija", "f'dan", "il-programm"]
returned = []

for i in sentence:
    print(str(i) + " -- " + st.stemm(i))
