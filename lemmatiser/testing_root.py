import malti.tokeniser as mlt
import lemmatiser      as l
import root            as r

text = """
Mr. Chairman jiena ma nafx kemm se jirnexxili ngħid minn dak li ppreparajt għax għamilt manifest 'beyond the year 2000'. Insemmi xi punti. L-ewwel ħaġa jiena naħseb żewġ preokupazzjonijiet fundamentali f'kull soċjeta, u naħseb dawn irridu nirriflettu fuqhom għall-millennju li ġej: jikkonċernaw b'mod bażiku l-ħobż u l-ħelsien. Issa jiena nistenna illi fuq l-ewwel wieħed meta nitkellmu fuq ħobż qed nitkellmu fuq xi ħaġa daqsxejn aktar sofistikata minn sempliċiment biċċa ħobż taħt ħajt tas-sejjieħ, qed nitkellmu fuq nutrimenti, qed nitkellmu fuq għażla miftuħa ta' prodotti u ta' servizzi.
L-istess meta nitkellmu fuq ħelsien nifhem li ma nibqgħux nitkellmu fuq ħelsien f'sens nazzjonalistiku bejn nativi u stranjieri imma xi ħaġa li nħossu bżonn kbir tagħha f'dis-soċjeta, bħala liberta internalizzata. Liberta jiġifieri rikonoxxuta, illi ġewwinija, mhux biss ta' l-istituzzjonijiet imma li tiġi mill-persuni, inklużi l-persuni li jistgħu - speċjalment il-persuni li jistgħu - suġġetti għall-kritika u għall-oppożizzjoni. Dan huwa t-test tal-liberta illi nittama li fil-millennju l-ġdid jintrebaħ forsi iżjed milli s'issa ntrebaħ.
Imbagħad tippreokkupani daqsxejn ukoll il-problema tal-konsumiżmu u ta' l-awtoriżmu li diġa hija karatteristika ta' dan is-seklu u nistenna li se tkompli taċċenna ruħha fil-millennju l-ġdid. Naturalment ma tistax iżżomm lura ċertu progress u ċerti kumditajiet, imma naħseb hu serju jekk wieħed jittraskura u jestranja ruħu mis-sempliċitajiet umani, u tVambjent naturali fil-komunita wkoll.
Naturalment anki l-problema li min jiġi f'din ir-responsabbilta ma jitlagħlux għal rasu, għaliex din ukoll tendenza daqsxejn taċ-ċokon, ta' kollox i ppersonalizzat.
"""

print("Tokenising...")
tokens = mlt.tokenise(text)

print("Normalising...")
filtered_tokens = l.normalise(tokens)

print("Finding roots...")
roots = [r.find_root(token) for token in filtered_tokens]

tagged_text = list(zip(filtered_tokens, roots))
error_words = [element[0] for element in tagged_text if "ERROR: could not find word origin" in element]

print(tagged_text)