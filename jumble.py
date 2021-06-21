'''
    Author: Adam Blinzler - adam.blinzler@gmail.com
    
    Complexity - 
        While the algorithm has a couple early release mechanisms, in the case of
        a word in the list that is a candidate for acceptance, the algorithm will
        loop over the character checker a maximum of X times where X is the
        set of unique characters in the input string, in which the maximum value
        of X is 26. This is the case where both the test word and input string
        have all alphabetical characters in them and the input string has more
        instances of each character than the test word.
        So one could say the maximum completion time would be 26 * N where N is
        the length of the word list, so O(N). 
        No parallel processing is implemented in this code. Each word check is 
        independent, the parallelization of this code only limited by the 
        hardware being run on.
'''


import os
import argparse
import re
from collections import Counter

def compile_string_frequency(string):
    return Counter(string)

def is_anagram(test_freq, given_freq):
    '''
        Use character frequency map to test if test is an anagram of the given.
        Return boolean
    '''
    # Sort dictionary by highest frequency to fail early
    for ch, i in sorted(test_freq.items(), key=lambda item: item[1], reverse=True):
        if not ( ch in given_freq and i <= given_freq[ch] ):
            # Both the character needs to be in the given word
            #   and contain enough of them to form the test word
            return False

    return True 

def check_word(test_word, given):
    test_word = test_word.lower()
    if len(test_word) <= given["length"] and test_word != given["string"]:
        # Only need to test for anagrams if the test word isn't longer than the given
        #   and is not the same as the given word
        if is_anagram(compile_string_frequency(test_word), given["freq"]):
            print(test_word)    
    return

def find_anagrams(filepath, given):
    '''
        Open the word text file and check each word against the given
    '''
    with open(filepath, 'r') as f:
        for line in f:
            test_word = line.strip()
            check_word(test_word, given)
    return

def build_given_dict(in_string):
    '''
        Build a dictionary from the input string.
            Could make a class if this grows in complexity.
    '''
    given = dict()
    given["string"] = in_string.lower() 
    given["length"] = len(in_string)
    given["freq"] = compile_string_frequency(given["string"])

    return given


def cli():
    '''
        Build the command line interface
    '''
    my_parser = argparse.ArgumentParser(description='Program will find all anagrams \
                        in text file from given input string. All non alphabet characters are ignored.')
    # Only use required positional arguments
    my_parser.add_argument('path', metavar='path', type=str,
                           help='path to text file of the word list')
    my_parser.add_argument('in_string', metavar='in_string', type=str,
                           help='string of alphabet characters to jumble and check for anagrams')

    args = my_parser.parse_args()

    ## Sanitize inputs
    filepath = args.path
    if not os.path.exists(filepath):
        filepath = False
        print("Error: File path does not exist.")

    # Keep only alphabet characters    
    in_string = re.sub("[^a-zA-Z]+", "", args.in_string)
    if len(in_string) == 0:
        in_string = False
        print("Error: Input string must contain alphabet characters")

    return filepath, in_string

if __name__ == "__main__":
    filepath, in_string = cli()
    
    if filepath and in_string:
        find_anagrams(filepath, build_given_dict(in_string))

    print("--- Jumble Script Completed ---")

