# -*- coding: utf-8 -*-
import re
from .transcribe import convert

def get_the_words_where_the_next_word_is_starts_with_consonant(text: str) -> list(tuple()):
    """
    :param text: string
    :return: list of tuples -> Each tupple has the word and the index of the word
    """
    vowels = ['a', 'e', 'i', 'o', 'u']
    text_word_list = re.split(" ", text)
    result_words = []
    for word in text_word_list:
        try:
            next_element = text_word_list[text_word_list.index(word) + 1]
            if next_element[0] not in vowels:
                result_words.append((word, text_word_list.index(word)))
        except IndexError as e:
            if e == 'list index out of range':
                pass
    return result_words

def pronuciation_changes_by_vowel(word: str) -> str:
    lower_text = word.lower()
    variation_dict = {
        "ði": "ðʌ",
    }
    try:
        word_matches = convert(lower_text)
        return variation_dict[word_matches]
    except KeyError as e:
        return

def general_subs(word: str) -> str:
    variation_dict = {
        "hwʌt": "wʌt", "hˈwɛðɜr":"ˈwɛðɜr", "eɪ":"ə",
    }
    try:
        return variation_dict[word.lower()]
    except KeyError:
        return

def convert_to_ipa2(original_text: str):
    list_to_call_if_matches_get_word_variation = get_the_words_where_the_next_word_is_starts_with_consonant(original_text)
    ipa_text = convert(original_text)
    ipa_text_list = re.split(" ", ipa_text)
    if list_to_call_if_matches_get_word_variation == []:
        return ipa_text
    else:
        for word in list_to_call_if_matches_get_word_variation:
            if pronuciation_changes_by_vowel(word[0].lower()):
                ipa_text_list[word[1]] = pronuciation_changes_by_vowel(word[0].lower())
        for ipa_word in ipa_text_list:
            match = general_subs(ipa_word)
            if match:
                ipa_text_list[ipa_text_list.index(ipa_word)] = match
        return "".join([el + " " for el in ipa_text_list])[:-1]
