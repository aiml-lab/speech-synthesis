# encoding: utf-8

from dict import dict_universal
from dict import dict_vowel
from dict import dict_consonant
from dict import dict_matra

import yaml

phoneme_delim = '_'

dict_cv = {}

for consonant in dict_consonant:
    for matra in dict_matra:
        temp = consonant + matra
        dict_cv[temp] = dict_consonant[consonant] + phoneme_delim + dict_vowel[dict_matra[matra]]

dict_consonant_schwa = {}

for consonant in dict_consonant:
    dict_consonant_schwa[consonant] = dict_consonant[consonant] + phoneme_delim + 'ə'

# print(dict_cv)

with open('dict_cv.yml', 'w') as yaml_file:
    yaml.dump(dict_cv, yaml_file, default_flow_style=False)

with open('dict_consonant_schwa.yml', 'w') as yaml_file:
    yaml.dump(dict_consonant_schwa, yaml_file, default_flow_style=False)
