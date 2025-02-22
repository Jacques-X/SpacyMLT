import stemmer as st

sentence = ["Bonġu", "kif", "int", "jien", "jisimni", "Jacques", "u", "qiegħed", "nivverifika", "l-użu", "tal-lingwa", "Maltija"]
returned = []

for i in sentence:
    print("processing... " + str(i))
    returned.append(st.stemmer(i)) 

for i in range(len(returned)):
    print(sentence[i] + " -- " + returned[i])
