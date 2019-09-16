# -*- coding: utf-8 -*-
import re


"""
- Percorrer cada elemento da lista de transcrições, que contéra listas com um ou mais elementos;
- Enquanto o laço for e executado, amazenar o índice do elemento atual em uma variável
- verificar se o primeiro  caracter do próximo elemento é uma vogal através do índice do elemento atual, o próximo elemento
será uma lista com um ou mais elementos, 
- Se o próximo elemento for consoante, verifique se existe o elemento atual na lista de substituições, se não, não faça nada



"""

def changes_when_next_word_starts_with_a_consonant(ipa_list) -> 'ipa_list':
    symbols_sub = {'ði':'ðʌ'}
    vowels_symbols = ["ɑ", "æ", "ʌ", "ɔ", "a", "ɛ", "ə", "e", "ɪ", "i", "o", "ʊ", "u"]
    max_index = len(ipa_list) -1

    for index in range(max_index):
        current_element = ipa_list[index]
        next_element = ipa_list[index + 1] if index < max_index else None

        if current_element[0] in symbols_sub and re.sub("ˈ", "", next_element[0])[0] not in vowels_symbols:
            current_element[0] = symbols_sub[current_element[0]]
    return ipa_list


def changes_when_exists_on_preferred_transcriptions(ipa_list: list) -> 'ipa_list':
    symbols_sub = {
        'hwaɪ':'waɪ', "bɑlm": "bɑm", "hwʌt": "wʌt" , "dʒɪst": "dʒʌst",
        "frər": 'fɔr', "gɪd": "gʊd", "hwʌn":"wʌn",
        }
    max_index = len(ipa_list) -1

    for index in range(max_index):
        current_element = ipa_list[index]
        next_element = ipa_list[index + 1] if index < max_index else None

        if current_element[0] in symbols_sub:
            current_element[0] = symbols_sub[current_element[0]]
    return ipa_list

def make_transcription_changes(ipa_list: list,) -> str:
    ipa_list = changes_when_next_word_starts_with_a_consonant(ipa_list)
    ipa_list = changes_when_exists_on_preferred_transcriptions(ipa_list)
    return ipa_list