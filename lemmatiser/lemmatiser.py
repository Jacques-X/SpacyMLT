def whole_plural_filter(word):
    """
    Ineħħi l-formi plurali tal-kelma meta dan hu plural sħiħ.
    Filter out plural forms of a word when it is a "whole" plural.
    """

    plural_forms = ['s', 'i', 'ijiet', 'jiet']

    for form in plural_forms:
        if word.endswith(form):
            return word[:-len(form)]

    return word # If no plural form found, return the word as it is

def broken_plural_filter(word):
    """
    Ineħħii l-formi plurali tal-kelma meta dan hu plural miksur.
    Filter out plural forms of a word when it is a "broken" plural.
    """

    # Implement

    return word  # If no plural form found, return the word as it is

def lemmatise(word):
    """
    Lemmatise a word using a rule-based approach.
    """
    return


# ------------------ TESTING ------------------ 
i = 0
while i < 10:
    print(whole_plural_filter(input()))
    print()