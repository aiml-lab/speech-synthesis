# encoding: utf-8

from devnagari_dict.dict import dict_universal
from devnagari_dict.dict import dict_vowel
from devnagari_dict.dict import dict_consonant
from devnagari_dict.dict import dict_matra
from devnagari_dict.dict import dict_anusvara
# import yaml

# dict_cv = yaml.load(open("devnagari_dict/dict_cv.yml"))
# dict_consonant_schwa = yaml.load(open("devnagari_dict/dict_consonant_schwa.yml"))

# def convertG2P(word):

def delete_schwa(word):
    
    str_len = len(word)

    temp_pos_char = {}
    temp_char_pos = {}

    for i in range(str_len):
        temp_pos_char[i] = word[i]

        if word[i] in temp_char_pos.keys():
            temp_char_pos[word[i]].append(i)
        else:
            tempList = []
            tempList.append(i)
            temp_char_pos[word[i]] = tempList

    temp_hash = {}

    # Rule 1
    for i in range(str_len):
        if word[i] in dict_vowel.keys():
            temp_hash[i] = 'F'
        elif word[i] in dict_consonant.keys():
            if i < str_len - 1:
                if word[i+1] in dict_matra.keys():
                    temp_hash[i] = 'F'
                elif word[i+1] == '्':
                    temp_hash[i] = 'H'
                else:
                    temp_hash[i] = 'U'
            else:
                temp_hash[i] = 'U'

    # Rule 2
    if 'य' in temp_char_pos:
        for index in temp_char_pos['य']:
            if index > 0:
                if temp_hash[index] == 'U':
                    if word[index-1] in {'ि', 'ी', 'ु', 'ू', 'ृ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ'}:
                        temp_hash[index] = 'F'

    # Rule 3 - May be wrong. Verify interpretation from someone!
    r3_list = ['य', 'र', 'ल', 'व']
    prev_H = False
    for index in range(str_len):
        if index in temp_hash.keys():
            if prev_H:
                if word[index] in r3_list and temp_hash[index] == 'U':
                    temp_hash[index] = 'F'
            elif temp_hash[index] == 'H':
                prev_H = True

    # Rule 4
    for index in temp_hash.keys():
        if index < str_len - 1:
            if word[index] in dict_consonant.keys():
                if temp_hash[index] == 'U':
                    if word[index+1] in dict_vowel.keys():
                        temp_hash[index] = 'F'

    # Rule 5
    prev_F = False
    for index in temp_hash.keys():
        if temp_hash[index] == 'F':
            prev_F = True
            break
        if word[index] in dict_consonant.keys() and not prev_F:
            if temp_hash[index] == 'U':
                temp_hash[index] = 'F'
                break

    # Rule 6
    list_index = list(temp_hash.keys())
    reverse_list_index = sorted(list_index, reverse=True)

    for index in reverse_list_index:
        if word[index] in dict_consonant.keys():
            if temp_hash[index] == 'U':
                temp_hash[index] = 'H'
            break

    # Rule 7
    for index in list_index:
        if word[index] in dict_consonant.keys():
            if temp_hash[index] == 'U' and index < str_len - 1:
                if word[index+1] in dict_consonant.keys() and temp_hash[index+1] == 'H':
                    temp_hash[index] = 'F'

    # Rule 8
    for i in range(len(list_index)):
        if i != 0 and i != len(list_index) - 1:
            if temp_hash[list_index[i]] == 'U' and word[list_index[i]] in dict_consonant.keys():
                if word[list_index[i-1]] in dict_consonant.keys() and word[list_index[i+1]] in dict_consonant.keys():
                    if temp_hash[list_index[i-1]] == 'F':
                        if temp_hash[list_index[i+1]] in {'F', 'U'}:
                            temp_hash[list_index[i]] = 'H'
            else:
                temp_hash[list_index[i]] == 'F'

    # Rule 9
    ret_phonemes = []
    for i in range(len(word)):
        if i in temp_hash.keys():
            if word[i] in dict_consonant.keys():
                ret_phonemes.append(dict_consonant[word[i]])
                if i == len(word) - 1:
                    if temp_hash[i] == 'F':
                        ret_phonemes.append('ə')
                else:
                    if word[i+1] != '्' and word[i+1] not in dict_matra.keys():
                        if temp_hash[i] == 'F':
                            ret_phonemes.append('ə')
            elif word[i] in dict_vowel.keys():
                ret_phonemes.append(dict_vowel[word[i]])
        elif word[i] in dict_matra.keys():
            ret_phonemes.append(dict_vowel[dict_matra[word[i]]])
        elif word[i] == 'ं':
            if i == len(word) - 1:
                if ret_phonemes[-1] in dict_vowel.values():
                    ret_phonemes[-1] = ret_phonemes[-1] + '̃'
                else:
                    ret_phonemes.append('ə')
                    ret_phonemes[-1] = ret_phonemes[-1] + '̃'
            else:
                if word[i+1] in {'ट', 'ठ', 'ड', 'ढ', 'ण'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('ɳ')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('ɳ')
                elif word[i+1] in {'च', 'छ', 'ज', 'झ', 'ञ', 'त', 'थ', 'द', 'ध', 'न'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('n')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('n')
                elif word[i+1] in {'क', 'ख', 'ग', 'घ', 'ङ'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('ɳ̃')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('ɳ̃')
                elif word[i+1] in {'प', 'फ', 'ब', 'भ', 'म'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('m')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('m')
                else:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('n')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('n')
        elif word[i] == 'ँ':
            if i == len(word) - 1:
                if ret_phonemes[-1] in dict_vowel.values():
                    ret_phonemes[-1] = ret_phonemes[-1] + '̃'
                else:
                    ret_phonemes.append('ə')
                    ret_phonemes[-1] = ret_phonemes[-1] + '̃'
            else:
                if word[i+1] in {'ड', 'ढ'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('ɳ')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('ɳ')
                elif word[i+1] in {'ज', 'झ', 'द', 'ध'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('n')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('n')
                elif word[i+1] in {'ग', 'घ'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('ɳ̃')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('ɳ̃')
                elif word[i+1] in {'ब', 'भ'}:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes.append('m')
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes.append('m')
                else:
                    if ret_phonemes[-1] in dict_vowel.values():
                        ret_phonemes[-1] = ret_phonemes[-1] + '̃'
                    else:
                        ret_phonemes.append('ə')
                        ret_phonemes[-1] = ret_phonemes[-1] + '̃'


    return ret_phonemes