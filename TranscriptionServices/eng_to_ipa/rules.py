# -*- coding: utf-8 -*-

def is_the_next_word_starts_with_a_consonant(words_in) -> bool:
    vowels = ['a', 'e', 'i', 'o', 'u']
    for word in words_in:
        word_index = words_in.index(word)
        next_element = None
        try:
            next_element = words_in[word_index + 1]
            if next_element[0].lower() not in vowels:
                return True
        except IndexError as e:
            return False



def transcription_changes(text: str, ipa_list: list,) -> str:
    words_in = text.split(" ")
    # This variable will have its content altered, so this copy is important
    words_in_clone = list(words_in)
    next_word_starts_with_a_consonant = {
        "the": "ðʌ",
    }
    preferred_transcritpions = ["bɑm", "wʌt", "dʒʌst", "fɔr",]
    for word in ipa_list:
        # Verify if the next work starts with the vowel and did it to the entire text
        word_index_in_ipa_list = ipa_list.index(word)
        if is_the_next_word_starts_with_a_consonant(words_in_clone) and words_in[word_index_in_ipa_list].lower() in next_word_starts_with_a_consonant.keys():
            ipa_list[word_index_in_ipa_list] = [next_word_starts_with_a_consonant[words_in[word_index_in_ipa_list].lower()]]
        words_in_clone.remove(words_in[word_index_in_ipa_list])
        if len(word) > 1:
            for w in word:
                if w in preferred_transcritpions:
                    ipa_list[word_index_in_ipa_list] = [w]
        else:
            if word in preferred_transcritpions:
                ipa_list[word_index_in_ipa_list] = [w]

    return ipa_list


