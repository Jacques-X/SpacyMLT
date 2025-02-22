import requests

def etympoligical_origin(word: str) -> int: # Implemented using lookup
    """
    Jivverifika jekk il-kelma hix ta' oriġini Semitica, Rumanzza jew Ingliža.
    Checks if a word is of Semitic, Romance, or English origin.

    0 -> Unknown
    1 -> Semitic
    2 -> Romance
    3 -> English
    """

    url = f"https://en.wiktionary.org/wiki/{word}#Maltese" # force it to seach in the Maltese section
    response = requests.get(url, timeout=5)  # timeout to prevent hanging

    if response.status_code == 200:
        text = response.text
        if "Semitic" in text or "Arabic" in text or "Hebrew" in text:
            return 1
        elif "Romance" in text or "Latin" in text or "Italian" in text or "Sicilian" in text:
            return 2
        elif "English" in text or "Old English" in text:
            return 3
    return 0

def pre_process(word: str) -> str:
    """
    Jġġati lura il-kelma mingħajr l-artikolu.
    Returns the word without the article.
    """
    articles = ['l-', 'il-', 'iċ-', 'iż-', 'id-,', 'in-', 'ir-', 'is-', 'it-', 'ix-', 'iż-', "f'", "tal-", "dal-"]

    for article in articles:
        if word.startswith(article):
            return word[len(article):]
        
    # Capitalisation
    if word[0].isupper():
        word = word.lower()
        
    return word

def filter_word_semitic(word: str) -> list:
    """
    Jġġati lura listaa fejn il-vokali u l-konsonanti doppji (u xi filtri oħra) huma mneħħija mill-kelma li ġiet ingħatat.
    Returns a list with all the vowels and duplicate consonants (+ some other filters) removed from the passed word.
    """
    vowels         = ['a', 'e', 'i', 'o', 'u', 'ie', 'à']
    
    char_list      = []
    vowels_removed = []
    filtered_word  = []

    # Take care of "ie", "għ" and "a'" to put them in one element
    i = 0
    while i < len(word):
        if word[i:i+2] == "ie":
            char_list.append("ie")
            i += 2
        elif word[i:i+2] == "għ":
            char_list.append("għ")
            i += 2
        elif word[i:i+2] == "a'":
            char_list.append("à")
        else:
            char_list.append(word[i])
            i += 1

    # Turn "'" at the end of a word into "għ"
    if char_list and char_list[-1] == "'": 
        char_list[-1] = "għ"

    # Remove Vowels
    for i in char_list:
        if i not in vowels:
            vowels_removed.append(i)

    # Remove Duplicate Consonants
    for i in range(len(vowels_removed)):
        if i == 0 or vowels_removed[i] != vowels_removed[i-1]:
            filtered_word.append(vowels_removed[i])

    # Nom mimmat (m is the first consonant)
    if filtered_word and filtered_word[0] == 'm': 
        filtered_word = filtered_word[1:] 

    # Remove 'st'
    if filtered_word[:2] == ['s', 't']:
        filtered_word = filtered_word[2:]

    return filtered_word

def find_root_semitic(filtered_word: list) -> str:
    """
    Joħroġ ħerq probabbli tal-kelmata Maltija billi jingħata l-konsonanti tagħha biss.
    Extracts the probable root of a Maltese word given only its consonants.
    """

    if len(filtered_word) >= 4:
        return "".join(filtered_word[:4]) 
    
    # Add dashes between letters--------------------------------------------------------

    return "".join(filtered_word)

def stemm(word: str) -> str:
    """
    TO IMPLEMENT
    """
    root   = ""

    word   = pre_process(word) # Can't find the origin with the article or capitalisation
    origin = etympoligical_origin(word)

    if origin == 1: # Semitic
        filtered_word = filter_word_semitic(word)
        root = find_root_semitic(filtered_word)
        return root
    elif origin == 2: # Romance
        return "ERROR: Romance words are not supported yet"
    elif origin == 3: # English
        return "ERROR: English words are not supported yet"
    elif origin == 0: # Unknown
        return "ERROR: could not find word origin"
    
    return "ERROR: something went wrong"
