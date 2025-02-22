import requests

def etympoligical_origin(word: str) -> int:
    """
    Jivverifika jekk il-kelma hix ta' oriġini Semitica, Rumanzza jew Ingliża.
    Checks if a word is of Semitic, Romance, or English origin.

    0 -> Unknown
    1 -> Semitic
    2 -> Romance
    3 -> English
    """

    url = f"https://en.wiktionary.org/wiki/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        text = response.text
        if "Semitic" in text:
            return 1
        elif "Romance" in text or "Latin" in text or "Italian" in text:
            return 2
        elif "English" in text or "Old English" in text:
            return 3
    return 0

def filter_word(word: str) -> list:
    """
    Jgħati lura listaa fejn il-vokali u l-konsonanti doppji (u xi filtri oħra) huma mneħħija mill-kelma li ġiet ingħatat.
    Retruns a list with all the vowels and duplicate consonants (+ some other filters) removed from the passed word.
    """
    # Lists to be used later
    vowels         = ['a', 'e', 'i', 'o', 'u', 'ie']
    char_list      = []
    filtered_word  = []
    vowels_removed = []

    # Take care of 'ie' and 'għ' to put them in one element
    i = 0
    while i < len(word):
        if word[i:i+2] == 'ie':
            char_list.append('ie')
            i += 2
        elif word[i:i+2] == 'għ':
            char_list.append('għ')
            i += 2
        else:
            char_list.append(word[i])
            i += 1

    # Remove Vowels
    for i in char_list:
        if i not in vowels:
            vowels_removed.append(i)

    # Remove Duplicate Consonants
    for i in range(len(vowels_removed)):
        if i == 0 or vowels_removed[i] != vowels_removed[i-1]:
            filtered_word.append(vowels_removed[i])

    # Nom mimmat (m is the first consonant)
    if filtered_word[0] == 'm':
        filtered_word = filtered_word[1:]

    # Remove 'st'
    if filtered_word[:2] == ['s', 't']:
        filtered_word = filtered_word[2:]

    return filtered_word

def find_root(filtered_word: list) -> str:
    """
    Joħroġ għerq probabbli tal-kelmata Maltija billi jingħata l-konsonanti tagħha biss.
    Extracts the probable root of a Maltese word given only its consonants.
    """

    if len(filtered_word) >= 4:
        return filtered_word[:4]  # Take the first three consonants as an approximation
    return filtered_word  # Return as is if less than 3 consonants

def stemmer(word: str):
    """
    TO IMPLEMENNT
    """

    origin = etympoligical_origin(word)

    if (origin == 1): # Semitic
        filtered_word = filter_word(word)
        root = find_root(filtered_word)
        return root
    elif (origin == 2): # Romance
        return "ERROR: Romance words are not supported yet"
    elif (origin == 3): # English
        return "ERROR: English words are not supported yet"
    elif (origin == 0): # Unknown
        return "ERROR: could not find word origin"
    
    return "ERROR: something went wrong"


# ------------------ TESTING ------------------ 
i = 0
while i < 10:
    print(stemmer(input()))
    print()