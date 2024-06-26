'''
:author: Emily Chen
:date: 2019

Python version of the orthographic redoubling function:

    aangkegtat --> aaNGNGkegtat

and the convert2ipa function:
    
    aangkegtat --> ɑːŋkəxtɑt

'''
import re


def tokenize(word):
    '''
    :param word: the word to tokenize into graphemes
    :type: str

    Tokenizes a given Yupik word into its respective graphemes
    '''

    GRAPHEMES = [
        'ngngw',
        'ngng',
        'ghhw',
        'ghh',
        'ghw',
        'ngw',
        'gg',
        'gh',
        'kw',
        'll',
        'mm',
        'ng',
        'nn',
        'qw',
        'rr',
        'wh',
        'aa',
        'ii',
        'uu',
        'a',
        'e',
        'f',
        'g',
        'h',
        'i',
        'k',
        'l',
        'm',
        'n',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'y',
        'z'
    ]

    # lower-case word so we don't have to worry about casing
    word = word.lower()
    
    result = []

    end = len(word) 
    while end > 0:
        foundGrapheme = False
        
        # attempts to greedy match graphemes starting
        # from the end of the word
        for grapheme in GRAPHEMES:
            if word.endswith(grapheme, 0, end):
                result.insert(0, grapheme)
                end -= len(grapheme) 
                foundGrapheme = True
                break
        
        # if a grapheme was not found, just prepend
        # the character to the final result
        if not foundGrapheme: 
            result.insert(0, word[end-1:end])
            end -= 1

    return result


def tokens2string(tokens):
    '''
    :param tokens: tokens to join into string
    :type: list

    Joins the given list of tokens into a string
    '''
    s = ""
    for i in range(len(tokens)): 
        s += tokens[i]

    return s


def redouble(graphemes):
    '''
    :param graphemes: graphemes that comprise the tokenized word
    :type: list

    Redoubles all of the relevant consonants in a tokenized Yupik word,
    effectively undoing the orthographic undoubling rules (see page 5 in
    Jacobson (2001))
    '''

    DOUBLED_FRICATIVE = ['ll', 'rr', 'gg', 'ghh', 'ghhw']

    DOUBLEABLE_FRICATIVE = ['l', 'r', 'g', 'gh', 'ghw']
    DOUBLEABLE_NASAL     = ['n', 'm', 'ng', 'ngw']

    UNDOUBLEABLE_UNVOICED_CNS = ['p', 't', 'k', 'kw', 'q', 'qw', 'f', 's', 'wh']

    double ={'l'  : 'll',
             'r'  : 'rr',
             'g'  : 'gg',
             'gh' : 'ghh',
             'ghw': 'ghhw',
             'n'  : 'nn',
             'm'  : 'mm',
             'ng' : 'ngng',
             'ngw': 'ngngw'}

    # copy the list of tokenized graphemes
    result = graphemes

    i = 0
    while (i+1 < len(result)):
        first  = result[i]
        second = result[i+1]
    
        # Rule 1A: Redouble a fricative that appears BEFORE a stop or one of the voiceless
        #          fricatives, where doubling is not used to show voicelessness.
        if (first in DOUBLEABLE_FRICATIVE and
            second in UNDOUBLEABLE_UNVOICED_CNS):
            result[i] = double[first]
            i += 2

        # Rule 1B: Redouble a fricative that appears AFTER a stop or one of the voiceless
        #          fricatives, where doubling is not used to show voicelessness.
        elif (first in UNDOUBLEABLE_UNVOICED_CNS and
              second in DOUBLEABLE_FRICATIVE):
            result[i+1] = double[second]
            i += 2

        # Rule 2: Redouble a nasal that appears after a stop or one of the voiceless fricatives,
        #         where doubling is not used to show voicelessness.
        elif (first in UNDOUBLEABLE_UNVOICED_CNS and
              second in DOUBLEABLE_NASAL):
            result[i+1] = double[second]
            i += 2

        # Rule 3A: Redouble a fricative or nasal that appears after a fricative where doubling is
        #          used to show voicelessness
        elif (first in DOUBLED_FRICATIVE and
              (second in DOUBLEABLE_FRICATIVE or
              second in DOUBLEABLE_NASAL)):
            result[i+1] = double[second]
            i += 2

        # Rule 3B: Redouble a fricative or nasal that appears before grapheme -ll-
        elif (first in DOUBLEABLE_FRICATIVE and
              second == "ll"):
            result[i] = double[first]
            i += 2

        else:
            i += 1

    return result



def convert2ipa(graphemes):
    '''
    :param graphemes: graphemes that comprise the tokenized word
    :type: list

    Converts each grapheme in the tokenized Yupik word to its
    respective IPA counterpart
    '''

    ipa = {
           # vowels                                                                                                                     
           "i":"\u0069",                # LATIN SMALL LETTER I
           "a":"\u0251",                # LATIN SMALL LETTER ALPHA
           "u":"\u0075",                # LATIN SMALL LETTER U
           "e":"\u0259",                # LATIN SMALL LETTER SCHWA

           "ii":"\u0069\u02D0",         # LATIN SMALL LETTER I to I with IPA COLON
           "aa":"\u0251\u02D0",         # LATIN SMALL LETTER ALPHA to ALPHA with IPA COLON
           "uu":"\u0075\u02D0",         # LATIN SMALL LETTER U to U with IPA COLON
 
           # stops                                                                                                                      
           "p" :"\u0070",               # LATIN SMALL LETTER P
           "t" :"\u0074",               # LATIN SMALL LETTER T
           "k" :"\u006B",               # LATIN SMALL LETTER K
           "kw":"\u006B\u02B7",         # LATIN SMALL LETTER K with MODIFIER LETTER SMALL W
           "q" :"\u0071",               # LATIN SMALL LETTER Q
           "qw":"\u0071\u02B7",         # LATIN SMALL LETTER Q with MODIFIER LETTER SMALL W
 
           # voiced fricatives                                                                                                          
           "v"  :"\u0076",              # LATIN SMALL LETTER V
           "l"  :"\u006C",              # LATIN SMALL LETTER L
           "z"  :"\u007A",              # LATIN SMALL LETTER Z
           "y"  :"\u006A",              # LATIN SMALL LETTER J
           "r"  :"\u0279",              # LATIN SMALL LETTER TURNED R
           "g"  :"\u0263",              # LATIN SMALL LETTER GAMMA
           "w"  :"\u0263\u02B7",        # LATIN SMALL LETTER GAMMA with MODIFIER LETTER SMALL W
           "gh" :"\u0281",              # LATIN LATTER SMALL CAPITAL INVERTED R
           "ghw":"\u0281\u02B7",        # LATIN LATTER SMALL CAPITAL INVERTED R with MODIFIER LETTER SMALL W
   
           # voiceless fricatives                                                                                                       
           "f"   :"\u0066",             # LATIN SMALL LETTER F
           "ll"  :"\u026C",             # LATIN SMALL LETTER L WITH BELT
           "s"   :"\u0073",             # LATIN SMALL LETTER S
           "rr"  :"\u0282",             # LATIN SMALL LETTER S WITH HOOK
           "gg"  :"\u0078",             # LATIN SMALL LETTER X
           "wh"  :"\u0078\u02B7",       # LATIN SMALL LETTER X with MODIFIER LETTER SMALL W
           "ghh" :"\u03C7",             # GREEK SMALL LETTER CHI
           "ghhw":"\u03C7\u02B7",       # GREEK SMALL LETTER CHI with MODIFIER LETTER SMALL W
           "h"   :"\u0068",             # LATIN SMALL LETTER H
   
           # voiced nasals                                                                                                              
           "m"  :"\u006D",              # LATIN SMALL LETTER M
           "n"  :"\u006E",              # LATIN SMALL LETTER N
           "ng" :"\u014B",              # LATIN SMALL LETTER ENG
           "ngw":"\u014B\u02B7",        # LATIN SMALL LETTER ENG with MODIFIER LETTER SMALL W
   
           # voiceless nasals                                                                                                           
           "mm":"\u006D\u0325",          # LATIN SMALL LETTER M   with COMBINING RING BELOW
           "nn":"\u006E\u0325",          # LATIN SMALL LETTER N   with COMBINING RING BELOW
           "ngng":"\u014B\u030A",        # LATIN SMALL LETTER ENG with COMBINING RING ABOVE
           "ngngw":"\u014B\u030A\u02B7", # LATIN SMALL LETTER ENG with COMBINING RING ABOVE and MODIFIER LETTER SMALL W
          }

    result = []

    if graphemes[-1] == '*':
        graphemes = graphemes[0:-1]  # Remove '*' marking strong gh. It's not needed in the IPA.

    for grapheme in graphemes:
        if grapheme in ipa:
            result.append(ipa[grapheme])
        else:
            result.append(grapheme)

    return result


def main():
    pass


if __name__ == "__main__":
    main()
