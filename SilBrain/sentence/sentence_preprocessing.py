import re

from hanspell import spell_checker
from konlpy.tag import Mecab
from nltk.tokenize import word_tokenize

def make_sentence(wordlist):
    sentence = ""
    for word in wordlist:
        sentence = sentence + " " + word
    return sentence

def spell_check(sentence):
    sent = sentence
    spelled_sentence = spell_checker.check(sent)

    hanspell_sentence = spelled_sentence.checked

    return hanspell_sentence

mecab = Mecab('C:\\mecab\\mecab-ko-dic')

def cleaning_josa(sentence):
    stopWords = ["JKB", "JKC", "JKS", "JKG", "JKO", "JKV", "JX", "JC", "MAG", "VV+EC", "VV+ETM", "XSV+ETM", "NNB+VCP+EC"]  # XSV, EC는 배열에 넣지 말기.
    
    word_tokens1 = word_tokenize(sentence)
    word_tokens2 = mecab.pos(sentence)
    
    tokens1_idx = 0
    combine = ''
    combine_valid = []
    full_sentence = ""

    for word, tag in word_tokens2:
        combine = combine + word
        
        if tag not in stopWords:
            combine_valid.append([tag, word])
        else: 
            if word == '다진' or word == '데친':
                combine_valid.append([tag, word])
            
        if word_tokens1[tokens1_idx] == combine:  
                        
            if tag == 'EC':  #XSV + EC, VV + EC, VX + EC 
                if pre_morpheme == 'XSV' or pre_morpheme == 'VV' or pre_morpheme == 'VX':
                    popped = combine_valid.pop()  #Pop EC
                    popped = combine_valid.pop()  #Pop XSV or VV or VX
            elif tag == 'ETM': #VV + ETM, XSV + ETM 
                if pre_morpheme == 'VV' or pre_morpheme == 'XSV':
                    popped = combine_valid.pop()  #Pop ETM, XSV
                    popped = combine_valid.pop()  #Pop VV
            valid_word_str = ''
            
            if len(combine_valid) > 0:
                for morph in combine_valid:
                    valid_word_str = valid_word_str + morph[1]        
            
            full_sentence = full_sentence + " " + valid_word_str    
            combine = ''
            #combine_valid = ''
            combine_valid.clear()
            tokens1_idx = tokens1_idx + 1
        pre_morpheme = tag

    return full_sentence

def sentence_preprocessing(in_sentence):
    
    sent_spell_checked = in_sentence

    spell_check_without_josa = cleaning_josa(sent_spell_checked)  
    stop_words = "사줘 주문 주문해 주문해줘 주문해봐 있잖아 그것 이것 저것 그거 이거 저거 나는 사고 싶어 사봐 봐 좀 사주 거 것 뭐야 말이야" # 먹고 먹을 싶"
    stop_words = stop_words.split(' ')
    word_tokens = word_tokenize(spell_check_without_josa)
    # result = []
    result = ''
    valid_word_cnt = 0
    for word in word_tokens:
        if word not in stop_words:
            word = addSpaceForNNPNNG(word)
            result = result + ' ' + word
            valid_word_cnt = valid_word_cnt + len(word)    
    
    return result, len(word_tokenize(result))

from kiwipiepy import Kiwi
kiwi = Kiwi()

def addSpaceForNNPNNG(in_word):
    word_tokens = kiwi.tokenize(in_word)
    
    len_tokens = len(word_tokens)
    
    result_str = ''
    if len_tokens > 1: 
        nn_cnt = 0
        for item in word_tokens:
            word = item.form
            tag = item.tag
            if tag == 'NNP' or tag == 'NNG':  
                if len(word) > 1:
                    nn_cnt = nn_cnt + 1        
        
        if nn_cnt == len(word_tokens):
            for item in word_tokens:
                word = item.form
                tag = item.tag
                result_str = result_str + word + ' '
            result_str = re.sub(r"\s+$", "", result_str)      
        else:
            result_str = in_word  
    else:
        result_str = in_word          
    return result_str
    
if __name__ == "__main__":
    
    while(True):
        sentence = input("\n전처리할 문장을 입력해주세요.(종료:q) \n-> ")
        if sentence == 'q':
            break
        result, valid_word_cnt = sentence_preprocessing(sentence)
        
        
        

        