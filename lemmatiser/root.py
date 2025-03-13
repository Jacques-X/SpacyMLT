import requests

def etympoligical_origin(token: str) -> int: # Implemented using lookup
    """
    Jivverifika jekk il-kelma hix ta' oriġini Semitica, Rumanzza jew Ingliža.
    Checks if a word is of Semitic, Romance, or English origin.

    0 -> Unknown
    1 -> Semitic
    2 -> Romance
    3 -> English
    4 -> Article
    """

    articles = ['il-', 'is-', 'id-', 'in-', 'iz-', 'iż-', 'l-', 's-', 'd-', 'n-', 'z-', 'ż-']

    if token in articles:
        return 4
    else:
        url = f"https://en.wiktionary.org/wiki/{token}#Maltese" # force it to seach in the Maltese section
        response = requests.get(url, timeout=5)  # timeout to prevent hanging

        if response.status_code == 200:
            text = response.text
            if "Semitic" in text or "Arabic" in text or "Hebrew" in text or "Moroccan Arabic" in text:
                return 1
            elif "Romance" in text or "Latin" in text or "Italian" in text or "Sicilian" in text:
                return 2
            elif "English" in text or "Old English" in text:
                return 3
        return 0

def filter_word_semitic(token: str) -> list:
    """
    Jġġati lura lista fejn il-vokali u l-konsonanti doppji (u xi filtri oħra) huma mneħħija mill-kelma li ġiet ingħatat.
    Returns a list with all the vowels and duplicate consonants (+ some other filters) removed from the passed word.
    """
    vowels         = ['a', 'e', 'i', 'o', 'u', 'ie', 'à']
    
    char_list      = []
    vowels_removed = []
    filtered_token  = []

    # Take care of "ie", "għ" and "a'" to put them in one element
    i = 0
    while i < len(token):
        if token[i:i+2] == "ie":
            char_list.append("ie")
            i += 2
        elif token[i:i+2] == "għ":
            char_list.append("għ")
            i += 2
        elif token[i:i+2] == "a'":
            char_list.append("à")
        else:
            char_list.append(token[i])
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
            filtered_token.append(vowels_removed[i])

    # Nom mimmat (m is the first consonant)
    if filtered_token and filtered_token[0] == 'm': 
        filtered_token = filtered_token[1:] 

    # Remove 'st'
    if filtered_token[:2] == ['s', 't']:
        filtered_token = filtered_token[2:]

    return filtered_token

def find_root_semitic(token: list) -> str:
    """
    Joħroġ għerq probabbli tal-kelmaa Maltija billi jingħata l-konsonanti tagħha biss.
    Extracts the probable root of a Maltese word given only its consonants.
    """

    if len(token) >= 4:
        return "".join(token[:4])

    return "".join(token)

def find_root_rom_eng(token: str) -> str:
    """
    Joħroġ iz-zokk morfemiku probabbli tal-kelma Maltija..
    Extracts the probable root of a Maltese.
    """
    root = ""

    prefixes = ["ik", "jik", "j", "ip", "jip"]
    suffixes = ["iet", "i", "joni", "ent", "a", "at", "anti", "aw", "i", "atur", "tat", "azzjoni"]

    if len(token) >= 4:
        for prefix in prefixes:
            if token.startswith(prefix):
                root = token[len(prefix):]
                break

        for suffix in suffixes:
            if token.endswith(suffix):
                root = token[:-len(suffix)]
                break
        
    if root == "":
        root = token

    return root

def find_root(token: str) -> str:
    """
    TO IMPLEMENT
    """
    root = ""

    origin = etympoligical_origin(token)

    if origin == 1: # Semitic
        filtered_token = filter_word_semitic(token)
        root = find_root_semitic(filtered_token)
        return root
    elif origin == 2 or origin == 3: # Romance and English
        root = find_root_rom_eng(token)
        return root 
    elif origin == 4: # Article
        return token
    elif origin == 0: # Unknown
        return "ERROR: could not find word origin"
    
    return "ERROR: something went wrong"
