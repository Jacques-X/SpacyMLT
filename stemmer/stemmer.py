def filter_vowels(word) -> list:
    vowels = ['a', 'e', 'i', 'o', 'u', 'ie']
    char_list = []
    consonant_list = []

    i = 0
    while i < len(word):
        if word[i:i+2] == 'ie':
            char_list.append('ie')
            i += 2
        else:
            char_list.append(word[i])
            i += 1

    for ch in char_list:
        if ch not in vowels:
            consonant_list.append(ch)

    return consonant_list

def stemmer(word):
    root = " "

    return root

print(filter_vowels("ġirja"))
