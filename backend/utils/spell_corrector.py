import json
import re
import unicodedata
import unidecode

from backend.config.constant import MAP_TO_DISTRICT_HCM
from backend.config.config import Config

def preprocess(sent):
    sent = sent.lower()
    sent = unicodedata.normalize("NFC", sent)
    sent = re.sub('\n', '', sent)
    sent = re.sub(r'\s+', r' ', sent)
    sent = re.sub(r'^\s', '', sent)
    sent = re.sub(r'\s$', '', sent)
    return sent

def processing_after(sent):
    sent = re.sub('\n', '', sent)
    sent = re.sub(r'\s+', r' ', sent)
    sent = re.sub(r'^\s', '', sent)
    sent = re.sub(r'\s$', '', sent)
    sent = re.sub(r'\s+(?=(\.|,))', '', sent)
    sent = re.sub(r'\s+/\s+', '/', sent)
    return sent

def in_dictionary(word):
    try:
        return Config.dictionary[word] != 0
    except:
        return False

# tổng hợp bộ sửa lỗi chính tả (bao gồm ghi tắt, teencode và telex)

def correct_sent(sent):
    sent = preprocess(sent)
    
    # ---------------TRANSFORM Q1 -> QUẬN 1, Q2 -> Quận 2, etc---------
    for key, value in MAP_TO_DISTRICT_HCM.items():
        if key in sent:
            sent = sent.replace(key, value)

    words = re.findall('\w*[~`\']\w*|\w+&\w+|\w+\s?:|\w+|[^\s\w]+', sent)
    sent = ""
    for word in words:
        # sửa lỗi viết tắt
        new_word = replace_one_one(word)
        if new_word == word:
            # sửa lỗi telex
            new_word = fix_telex_word(new_word)
            # sửa lỗi teencode
            new_word = correct_teencode_word(new_word)
            if not in_dictionary(new_word) and not new_word.isdigit() and (len(new_word.split()) == 1):
                new_word = word
        sent += new_word + ' '
    # Sửa lỗi phím gần
    # sent = correct_close_character_sent(sent)
    sent = processing_after(sent)
    # Thêm dấu
    # sent = accent_correct.translate(sent)
    return sent

def fix_telex_word(word):
    try:
        if Config.eng_dic[word] == 1: return word
    except:
        ## define accent_to_telex and additional_keystrokes
        chars = ['ơ', 'ô', 'ê', 'e', 'ă', 'â', 'ư', 'a', 'o', 'i', 'u', 'y']
        accents = ['í', 'ỉ', 'ĩ', 'ì', 'ị']
        accents = [unicodedata.normalize('NFKD', a)[1] for a in accents]
        additional_keystrokes = ['s', 'r', 'x', 'f', 'j']
        accent_to_telex = dict()
        for i in range(len(accents)):
            accent_to_telex[accents[i]] = additional_keystrokes[i]

        accent_telex_errors = dict()
        for c in chars:
            for i, a in enumerate(accents):
                text = ''.join([c, a])
                merged = unicodedata.normalize('NFC', text)

                keystroke = additional_keystrokes[i]
                pattern = f'{c}(.*){keystroke}'
                accent_telex_errors[pattern] = merged + '\\1'

        char_telex_errors = dict()
        for i, c in enumerate(['ư', 'â', 'ă', 'ô', 'ơ', 'ê']):
            parts = unicodedata.normalize('NFKD', c)
            base_c = parts[0]
            keystroke = ['w', 'a', 'w', 'o', 'w', 'e'][i]
            pattern = f'{base_c}(.*){keystroke}'
            char_telex_errors[pattern] = c + '\\1'
        char_telex_errors['d(.*)d'] = 'đ\\1'



        ## covert accents to keystrokes
        word = word.lower()
        ## convert case ddaamff => ddaamf
        check_dup = word[::-1]
        while len(check_dup) >=3:
            if (check_dup[0] == check_dup[1]) and (check_dup[0] not in ['a','e','o','u','d']) and (check_dup[0].isalpha()):
                check_dup = check_dup[1:]
            else:
                break
        word = check_dup[::-1]
        
        word = unicodedata.normalize('NFKD', word)
        for accent, keystroke in accent_to_telex.items():
            word = re.sub(accent, keystroke, word)

        ## push keystrokes to the end of word
        reorder_word = word
        i = 1
        n = len(word)
        while (i < n):
            a = reorder_word[i]
            if a in additional_keystrokes + ['w'] and (reorder_word[i - 1] + a != 'tr'):
                reorder_word = reorder_word[:i] + reorder_word[i + 1:] + a
                n = n - 1
            else:
                i = i + 1
        word = reorder_word

        word = unicodedata.normalize('NFC', word)

        for key, value in char_telex_errors.items():
            word = re.sub(key, value, word)

        ## 'trưong' -> 'trương'
        word = re.sub('ưo', 'ươ', word)

        for key, value in accent_telex_errors.items():
            word = re.sub(key, value, word)

        for key, value in Config.complex_telex.items():
            word = re.sub(key, value, word)
        return word

def replace_one_one(word, dictionary = None):
    '''
    replace teencode with correct one by using dictionary
    Input:
        word        :str - teencode word
        dictionary  : pd.Dataframe - 1-1 dictionary
    return:
        new_word    :str - correct word
    '''
    if dictionary == None:
        dictionary = Config.short_word_dic
        
    new_word = dictionary.get(word, word)
    if new_word == word:
        uni_word = replace_with_regex(word, Config.teencode_re_dic, dictionary)
        new_word = dictionary.get(uni_word, word)
    return new_word

def replace_with_regex(word, regex_list, dic_one_one, check=0):
    '''
    replace teencode with correct one by using rule (regex)
    Input:
        word        : str - teencode word
        regex_list  : pd.DataFrame - teencode regex
        dic_one_one : pd.DataFrame - 1-1 dictionary
        check       : boolean - number of times using this method
    return:
        new_word    : str - correct word
    '''
    new_word = unique_charaters(word)
    for pattern in regex_list.keys():
        if re.search(pattern, new_word):
            new_word = re.sub(pattern, regex_list[pattern], new_word)
            break
    if dic_one_one.get(new_word, new_word) != new_word:
        return dic_one_one.get(new_word, new_word)
    if check == 2 or unidecode.unidecode(new_word) in Config.single_word_dic:
        return new_word
    new_word = replace_with_regex(new_word, Config.teencode_re_dic, Config.short_word_dic, check + 1)
    return new_word

def unique_charaters(sent):
    i = 0
    new_sent = ''
    while i < len(sent):
        j = i + 1
        while (not sent[i].isdigit()) and j < len(sent) and sent[i] == sent[j]:
            j = j + 1
        new_sent += sent[i]
        i = j
    return new_sent

def correct_teencode_word(word):
    word = preprocess(word)
    try:
        if Config.eng_dic[word] == 1: return word
    except:
        new_word = word
        new_word = correct_vowel(new_word, Config.vowel_dic)
        new_word = replace_one_one(new_word, Config.short_word_dic)
        if word == new_word:
            new_word = replace_with_regex(new_word, Config.teencode_re_dic, Config.short_word_dic)
        return new_word
def correct_vowel(word, vowel_dictionary):
    '''
    correct sentence has vowel next to symbol by rule. Ex: a~ -> ã
    Input:
        sent    : str - teencode sentence
        vowel_dictionary: pd.DataFrame - vietnamese_vowel dictionary
    return:
        sent    : str - correct sentence
    '''
    pattern = r'[aăâeêuưiyoôơ][`~\']'
    p = re.search(pattern, word)
    new_word = word
    if p:
        idx = p.span()
        replace_vowel = vowel_dictionary[word[idx[0]]][word[idx[0] + 1]]
        new_word = re.sub(pattern, replace_vowel, new_word)
    return new_word
