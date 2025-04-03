import requests
import csv
import os

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

def filter_word_semitic(token: str) -> str:  # Return type changed to str
    """
    Jġġati lura lista fejn il-konsonanti doppji (u xi filtri oħra) huma mneħħija mill-kelma li ġiet ingħatat.
    Returns a string with duplicate consonants (+ some other filters) removed from the passed word.
    """
    char_list = []
    
    # Take care of "ie", "għ" and "a'" to put them in one element
    i = 0
    while i < len(token):
        if i+1 < len(token) and token[i:i+2] == "ie":
            char_list.append("ie")
            i += 2
        elif i+1 < len(token) and token[i:i+2] == "għ":
            char_list.append("għ")
            i += 2
        elif i+1 < len(token) and token[i:i+2] == "a'":
            char_list.append("à")
            i += 2
        else:
            char_list.append(token[i])
            i += 1

    # Turn " ' " at the end of a word into "għ"
    if char_list and char_list[-1] == "'": 
        char_list[-1] = "għ"
        
    # Remove Duplicate Consonants
    filtered_token = []
    for i in range(len(char_list)):
        if i == 0 or char_list[i] != char_list[i-1]:
            filtered_token.append(char_list[i])
            
    # Join the list into a string before returning
    return "".join(filtered_token)

def find_root_semitic(token: list) -> str:
    """
    Joħroġ għerq probabbli tal-kelmaa Maltija billi jingħata l-konsonanti tagħha biss.
    Extracts the probable root of a Maltese word given only its consonants.
    """
    # Remove vowels
    vowels = ["a", "e", "i", "o", "u", "à", "è", "ì", "ò", "ù", "ie"]
    token = [char for char in token if char.lower() not in vowels]
    
    # "m" had been removed but it is part of the root
    if len(token) <= 2:
        token.insert(0, "m")
        
    if len(token) >= 4:
        token = token[:4]
        
    return "".join(token)

def import_affixes() -> list:
    """
    Jimportja prefixes and suffixes minn CSV file.
    Imports prefixes and suffixes from a CSV file.
    """
    prefixes = []
    suffixes = []

    current_dir = os.path.dirname(__file__)
    affixes_file = os.path.join(current_dir, 'affixes.csv')
    with open(affixes_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            suffixes.append(row[0])
            prefixes.append(row[1])

    return prefixes, suffixes

def remove_affixes(token: str) -> str:
    """
    Joħroġ iz-zokk morfemiku probabbli tal-kelma Maltija.
    Extracts the probable root of a Maltese.
    """
    root = ""

    prefixes, suffixes = import_affixes()

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

    print(token)

    if origin == 1: # Semitic
        filtered_token = filter_word_semitic(token)
        filtered_token = remove_affixes(filtered_token)
        root = find_root_semitic(filtered_token)
        return root
    elif origin == 2 or origin == 3: # Romance and English
        root = remove_affixes(token)
        return root 
    elif origin == 4: # Article
        return token
    elif origin == 0: # Unknown
        return "ERROR: could not find word origin"
    
    return "ERROR: something went wrong"
