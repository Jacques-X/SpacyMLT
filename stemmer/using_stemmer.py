import stemmer as st

sentence = ["Bonġu", "kif", "int", "jien", "jisimni", "Jacques", "u", "qiegħed", "nivverifika", "l-użu", "tal-lingwa", "Maltija", "f'programm", "li", "jien", "għandi", "nkompli", "nibni", "u", "nippubblika", "għalik", "u", "għal", "kulħadd", "ieħor", "li", "jixtieq", "jikkompeti", "f'dan", "il-ġeneru", "ta'", "programm", "komputazzjonali", "li", "jinkludi", "l-użu", "tal-lingwa", "Maltija", "u", "l-Ingliża", "u", "l-ġermaniża", "u", "l-italjan", "u", "l-franċiża", "u", "l-ispagnol", "u", "l-ġappuniż", "u", "l-ġorġ"]
returned = []

for i in sentence:
    print("processing... " + str(i))
    returned.append(st.stemmer(i)) 

for i in range(len(returned)):
    print(sentence[i] + " -- " + returned[i])
