from bs4 import BeautifulSoup
import requests
import csv
import os
import re

def etymological_origin(token: str) -> int:
    """
    Jivverifika jekk il-kelma hix ta' oriġini Semitica, Rumanza jew Ingliża billi tanalizza
    t-taqsima tal-etimoloġija fuq il-Wiktionary.
    Checks if a word is of Semitic, Romance, or English origin by analyzing
    the etymology section on Wiktionary.

    Args:
        token: The word (string) to check.

    Returns:
        int:
            0 -> Unknown or error
            1 -> Semitic
            2 -> Romance
            3 -> English
            4 -> Article
    """
    token = token.strip()
    if not token:
        return 0 # Empty token

    articles = ['il-', 'is-', 'id-', 'in-', 'iz-', 'iż-', 'l-', 's-', 'd-', 'n-', 'z-', 'ż-', 'għal-', 'għall-', 'tal-', 'tal-']
    normalized_token = token.lower()
    if normalized_token in articles or f"{normalized_token}-" in articles:
        return 4

    # Construct the URL, forcing it to the Maltese section
    url = f"https://en.wiktionary.org/wiki/{token}#Maltese"
    headers = { 
        'User-Agent': 'MalteseEtymologyChecker/1.0 (https://example.com/bot; your_email@example.com)'
    }

    try:
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 0 # Network error or HTTP error

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the Maltese language section
    maltese_section_header = soup.find('span', {'class': 'mw-headline', 'id': 'Maltese'})
    if not maltese_section_header:
        maltese_section_header = soup.find(lambda tag: tag.name in ['h1','h2','h3'] and tag.get('id') == 'Maltese' and 'mw-headline' in tag.get('class', []))
        if not maltese_section_header:
            maltese_headers = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'Maltese', re.I))
            if maltese_headers:
                maltese_section_header = maltese_headers[0].find('span', class_='mw-headline') 
            if not maltese_section_header:
                return 0

    etymology_text = ""
    current_element = maltese_section_header.parent 

    while current_element:
        current_element = current_element.find_next_sibling()
        if current_element is None:
            break
        if current_element.name == 'h2':
            break

        etymology_header_span = current_element.find('span', {'class': 'mw-headline', 'id': lambda x: x and x.startswith('Etymology')})

        if etymology_header_span:
            etym_content_element = current_element.find_next_sibling()
            while etym_content_element:
                if etym_content_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    is_another_etymology = etym_content_element.find('span', {'class': 'mw-headline', 'id': lambda x: x and x.startswith('Etymology')})
                    if not (etym_content_element.name >= current_element.name and is_another_etymology) : 
                         break


                if etym_content_element.name == 'p': 
                    etymology_text += etym_content_element.get_text(separator=' ', strip=True) + " "
                elif etym_content_element.name in ['ul', 'ol', 'dl']: 
                    etymology_text += etym_content_element.get_text(separator=' ', strip=True) + " "

                etym_content_element = etym_content_element.find_next_sibling()

    if not etymology_text:
        maltese_content_element = maltese_section_header.parent.find_next_sibling()
        temp_text = ""
        while maltese_content_element and maltese_content_element.name != 'h2':
            temp_text += maltese_content_element.get_text(separator=' ', strip=True) + " "
            maltese_content_element = maltese_content_element.find_next_sibling()
        if not temp_text:
            etymology_text = soup.get_text(separator=' ', strip=True)
        else:
            etymology_text = temp_text

    etymology_text_lower = etymology_text.lower()

    semitic_keywords = ["semitic", "arabic", "sħem", "għarbi", "aramaic", "phoenician", "hebrew", "lixandra", "moroccan arabic"]
    romance_keywords = ["romance", "latin", "italian", "sicilian", "norman", "french", "catalan", "spanish", "rumanz", "latin", "taljan", "sqalli"]
    english_keywords = ["english", "old english", "middle english", "ingliż"]

    if any(keyword in etymology_text_lower for keyword in english_keywords):
        return 3
    elif any(keyword in etymology_text_lower for keyword in romance_keywords):
        return 2
    elif any(keyword in etymology_text_lower for keyword in semitic_keywords):
        return 1
    else:
        return 0 # Unknown origin

def filter_word_semitic(token: str) -> str:  # Return type changed to str
    """
    Jgħati lura lista fejn il-konsonanti doppji (u xi filtri oħra) huma mneħħija mill-kelma li ġiet ingħatat.
    Returns a string with duplicate consonants (+ some other filters) removed from the passed word.
    """
    char_list = []

    # Turn " ' " at the end of a word into "għ"
    if char_list and char_list[-1] == "'": 
        char_list[-1] = "għ"
    
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
        
    # Remove Duplicate Consonants
    filtered_token = []
    for i in range(len(char_list)):
        if i == 0 or char_list[i] != char_list[i-1]:
            filtered_token.append(char_list[i])
            
    # Join the list into a string before returning
    return "".join(filtered_token)

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

def remove_affixes_recursive(token: str, prefixes: list, suffixes: list, depth: int = 0, max_depth: int = 3) -> str:
    """
    Recursively removes prefixes and suffixes from a Maltese word to find its morphemic stem.
    """
    if depth >= max_depth or len(token) < 3:
        return token
    
    original_token = token
    
    # Try removing prefixes
    for prefix in sorted(prefixes, key=len, reverse=True):  # Sort by length to try longer prefixes first
        if token.startswith(prefix) and len(token) > len(prefix) + 2:  # Ensure we don't remove too much
            new_token = token[len(prefix):]
            # Recursively try to remove more affixes
            return remove_affixes_recursive(new_token, prefixes, suffixes, depth + 1, max_depth)
    
    # Try removing suffixes
    for suffix in sorted(suffixes, key=len, reverse=True):  # Sort by length to try longer suffixes first
        if token.endswith(suffix) and len(token) > len(suffix) + 2:  # Ensure we don't remove too much
            new_token = token[:-len(suffix)]
            # Recursively try to remove more affixes
            return remove_affixes_recursive(new_token, prefixes, suffixes, depth + 1, max_depth)
    
    # If no affixes were removed, return the original token
    return original_token

def extract_consonants(token: str) -> list:
    """
    Extracts consonants from a token while applying Maltese-specific rules.
    """
    vowels = ["a", "e", "i", "o", "u", "ā", "ī", "ū", "è", "ì", "ò", "ù"]
    consonants = []
    
    # Process the token character by character
    i = 0
    while i < len(token):
        if token[i].lower() not in vowels:
            # Don't add the same consonant twice in a row (gemination)
            if not consonants or token[i] != consonants[-1]:
                consonants.append(token[i])
        i += 1
    
    # Special handling: għ and ħ are important consonants in Maltese roots
    # Make sure they're preserved if present
    special_consonants = ["ʕ", "ħ"]
    for consonant in special_consonants:
        if consonant in token and consonant not in consonants:
            consonants.append(consonant)
    
    return consonants

def is_likely_quadriliteral(token: str, consonants: list) -> bool:
    """
    Determines if a word is likely to have a quadriliteral root.
    """
    # Quadriliteral patterns in Maltese often follow specific patterns
    quadriliteral_patterns = [
        # Common verb forms
        "ċaqċaq", "gemgem", "gerger", "farfar",
        # Common patterns
        "CVCCVC", "CCVCCVC"
    ]
    
    # Check for reduplicated form (C1VC2C1VC2)
    if len(consonants) >= 4 and consonants[0] == consonants[2] and consonants[1] == consonants[3]:
        return True
    
    # Check token length - quadriliterals tend to be longer
    if len(token) >= 6:
        return True
        
    # Default to False for shorter words
    return False

def identify_triliteral_root(token: str, consonants: list) -> str:
    """
    Attempts to identify the most likely triliteral root from a set of consonants.
    """
    # Common prefixes that might introduce additional consonants
    prefix_consonants = ["m", "n", "t", "j", "s"]
    
    # If we have a consonant that typically comes from a prefix, remove it
    if len(consonants) > 3 and consonants[0] in prefix_consonants:
        return ''.join(consonants[1:4])
    
    # Check for special cases with 'n' infix in Form VII/VIII verbs
    if len(consonants) > 3 and consonants[1] == "n":
        return consonants[0] + consonants[2] + consonants[3]
    
    # Check for 't' infix in Form VIII verbs
    if len(consonants) > 3 and consonants[1] == "t":
        return consonants[0] + consonants[2] + consonants[3]
    
    # Default to first three consonants if no pattern is detected
    return ''.join(consonants[:3])

def find_root_semitic(token: str) -> str:
    """
    Extracts the probable root of a Maltese word based on Semitic morphological patterns.
    Handles triliteral and quadriliteral roots according to Maltese phonological rules.
    """
    # Extract consonants while preserving certain patterns
    consonants = extract_consonants(token)
    
    # Root determination based on number of consonants
    if len(consonants) == 0 or len(consonants) == 1:
        return token  # Return original if no/one consonant/s found
    elif len(consonants) == 2:
        # For two-consonant words, try to determine if there's an elided root letter
        # Common in Maltese are weak verbs that lose middle/final radical
        if 'ie' in token or 'għ' in token:
            # Likely a hollow verb with middle radical w/y that became ie
            return consonants[0] + 'w' + consonants[1]  # Assume middle weak radical
        else:
            # Try to determine if it's final-weak (e.g., "ra" -> r-'-y)
            return consonants[0] + consonants[1] + 'għ'  # Assume final weak radical
    elif len(consonants) == 3:
        # Classic triliteral root - common in Semitic languages
        return ''.join(consonants)
    elif len(consonants) >= 4:
        # Could be quadriliteral or triliteral with gemination or affixation
        # Use first four consonants if present, otherwise use first three
        if is_likely_quadriliteral(token, consonants):
            return ''.join(consonants[:4])
        else:
            # Probably triliteral with additional consonants from affixes
            # Try to identify the most likely consonants for the root
            return identify_triliteral_root(token, consonants)
    
    # Fallback
    return ''.join(consonants[:4])

def remove_affixes(token: str) -> str:
    """
    Improved version of remove_affixes that uses recursive approach.
    """
    prefixes, suffixes = import_affixes()
    return remove_affixes_recursive(token, prefixes, suffixes)

def find_root(token: str, pos_tag: str) -> str:
    """
    Isib l-għerq/zokk morfemiku tal-kelma li jkun ingħata.
    Finds the root/morphemic stem of the given word.
    """
    root = ""

    if token.startswith('i'):
        token = token[1:]
    origin = etymological_origin(token)    

    if origin == 1 and (pos_tag == "VERB" or pos_tag == "NOUN" or pos_tag == "ADJ" or pos_tag == "AUX"): # Semitic
        filtered_token = filter_word_semitic(token)
        filtered_token = remove_affixes(filtered_token)
        print(filtered_token + "\n")
        root = find_root_semitic(filtered_token)
        root = (root + " " + str(origin))
        return root
    elif origin == 2 or origin == 3: # Romance and English
        root = remove_affixes(token)
        return root 
    elif origin == 4: # Article
        return token
    elif origin == 0: # Unknown
        return token
    
    return token