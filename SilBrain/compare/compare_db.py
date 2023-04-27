
import csv
import os
import time 
import re

from nltk.tokenize import word_tokenize

from datetime import datetime
from sentence.sentence_preprocessing import sentence_preprocessing, spell_check
from makeDB.make_question_db import make_user_question_db
from makeDB.make_search_db import make_category_search_db, MAKE_DB_PATH
from makeTree.make_tree import make_tree, draw_tree, search_tree

SEARCH_DB_NAME = os.path.join(MAKE_DB_PATH,'db/food_combine_search_db.csv')
USER_DB_NAME = os.path.join(MAKE_DB_PATH,'db/food_combine_user_db.csv')
PRODUCT_DB_NAME = os.path.join(MAKE_DB_PATH, 'free_wow_final.csv')
SIMPLE_TEST_DB_NAME = os.path.join(MAKE_DB_PATH,'db/raw_meat_eggs_re_v3.csv')

def keywordsCompareA(products_list):
    
    while(True):
        #print(f"{products_list}")
        keywords = input("\n'포함할 키워드/제외할 키워드' 를 띄어쓰기 단위로 입력해 주세요(종료:q). ex)국내산 사과/아오리 \n-> ")
        # print(f"{keywords}") 
        if keywords == 'q':
            break
        keyword_list = keywords.split('/')
        # print(f"keyword_list : {keyword_list}")
        included_keyword_list = keyword_list[0].split(' ')
        keyword_cnt1 = len(included_keyword_list)
        
        excluded_keyword_list = []
        
        if len(keyword_list) > 1:
            excluded_keyword_list = keyword_list[1].split(' ')
            keyword_cnt2 = len(excluded_keyword_list)
                                   
        real_cnt = 0
        hit_product_list = []
        for product in products_list:
            real_cnt = 0
            for keyword in included_keyword_list:
                if keyword in product:
                    real_cnt = real_cnt + 1
            if real_cnt == keyword_cnt1:
                hit_product_list.append(product)
        
        final_product_list = []
        if len(keyword_list) > 1:  
            for product in hit_product_list:
                real_cnt = 0
                for keyword in excluded_keyword_list:
                    if keyword not in product or keyword == '':
                        real_cnt = real_cnt + 1
                if real_cnt == keyword_cnt2:
                    final_product_list.append(product)
        else:
            for product in hit_product_list:
                final_product_list.append(product)
                
        if len(final_product_list) == 0:
            print(f"검색 결과가 없습니다.")
        for idx, item in enumerate(final_product_list):
            print(f"[{idx}] {item}")  
            
def compare_keywords_within_crawled_products(list_products, product_name_and_synonyms, special_options_list, excluded_keywords, q_words):
    if 'GOLDEN' in product_name_and_synonyms:
        product_name_and_synonyms = product_name_and_synonyms.replace('GOLDEN', '')
        splitted = product_name_and_synonyms.split(' ')
        name_of_6th = ''
        name_of_synonym = ''
        for keyword in splitted:
            if 'MMM' in keyword:
                name_of_6th = name_of_6th + ' ' + keyword.replace('MMM', '')
            elif 'QQQ' in keyword:
                name_of_synonym = name_of_synonym + ' ' + keyword.replace('QQQ', '')
        product_name_and_synonyms = name_of_6th + '#' + name_of_synonym
                    
    compare_6th_list = compareAnd(product_name_and_synonyms.split('#'), list_products)
    if len(compare_6th_list) == 0:
        compare_6th_list = compareOR(product_name_and_synonyms.split('#'), list_products)    
    
    if len(compare_6th_list) == 0:
        return compare_6th_list
    else:
        compare_option_list = compare_6th_list
        if special_options_list != 'none':
            special_options_list_new = special_options_list.split('&')
            
            for option in special_options_list_new:
                splitted = option.split('/')
                compare_option_list = compareOR(splitted[0].split('#'), compare_option_list)
                extKeywords = splitted[1].split('#')
                if '' in extKeywords:
                    extKeywords.remove('')
                compare_option_list = compareExcluded(extKeywords, compare_option_list)
        
        extKeywords2 = excluded_keywords.split('#')
        if '' in extKeywords2:
            extKeywords2.remove('')
        compare_excluded_list = compareExcluded(extKeywords2, compare_option_list)

        final_list = []
        q_word_and = compareAnd(q_words, compare_excluded_list)
        q_word_or = compareOR(q_words, compare_excluded_list)
        
        for andresult in q_word_and:
            if andresult not in final_list:
                final_list.append(andresult)
        for orresult in q_word_or:
            if orresult not in final_list:
                final_list.append(orresult)
        for idx, result in enumerate(compare_excluded_list):
            if result not in final_list:
                final_list.append(result)    
            
        return final_list

def compare_keywords_within_crawled_products_v2(in_list_products, in_keyword_list, in_q_word_list):
    final_list = []
    
    comp_whole = compareWhole(in_keyword_list, in_list_products)
    
    if len(comp_whole) > 0:
        q_word_and = compareAnd(in_q_word_list, comp_whole)
        q_word_or = compareOR(in_q_word_list, comp_whole)
        for andresult in q_word_and:
            if andresult not in final_list:
                final_list.append(andresult)
        for orresult in q_word_or:
            if orresult not in final_list:
                final_list.append(orresult)
        for idx, result in enumerate(comp_whole):
            if result not in final_list:
                final_list.append(result)    
            
        return final_list
    else:
        return []

def compare_keywords_within_crawled_products_bak(list_products, product_name_and_synonyms, special_options_list, excluded_keywords):
    compare_6th_list = compareOR(product_name_and_synonyms.split('#'), list_products)
    
    if len(compare_6th_list) == 0:
        return compare_6th_list
    else:
        compare_option_list = compare_6th_list
        special_options_list_new = special_options_list.split('&')
        for option in special_options_list_new:
            splitted = option.split('/')
            compare_option_list = compareOR(splitted[0].split('#'), compare_option_list)
            compare_option_list = compareExcluded(splitted[1].split('#'), compare_option_list)
        
        compare_excluded_list = compareExcluded(excluded_keywords.split('#'), compare_option_list)
    
        return compare_excluded_list
    
def keywordsCompareB(in_products_list, in_products_list_user, in_user_sentence):  
    list_of_category_candidates = get_list_of_category_candidates(in_products_list, in_products_list_user, in_user_sentence)
    
    rootnode = make_tree(list_of_category_candidates)

    category_id_and_name_of_6th = ''
    special_options_list = [] 
    excluded_keywords = ''
    category_id_and_name_of_6th, special_options_list, excluded_keywords = search_tree(rootnode)
                
    return category_id_and_name_of_6th, special_options_list, excluded_keywords    

def get_list_of_category_candidates(in_products_list, in_products_list_user, in_user_sentence):
    preprocessed_sentence = in_user_sentence
    
    max_match_cnt = 0 
    match_product_list = []
    match_product_list_user = []
    for row_idx, product in enumerate(in_products_list):  
        match_cnt = howManyWordsMatch(preprocessed_sentence, product)
        if match_cnt > 0 :            
            match_product_list.append([match_cnt, product])
            match_product_list_user.append([match_cnt, in_products_list_user[row_idx]])
            if match_cnt > max_match_cnt: 
                max_match_cnt = match_cnt 
    
    final_product_list = []  
    for product in match_product_list: 
        if product[0] == max_match_cnt:
            final_product_list.append(product)
            
    final_product_list_user = [] 
    final_product_list_user_for_tree = [] 
    for product in match_product_list_user:
        if product[0] == max_match_cnt: 
            final_product_list_user.append(product)     
            final_product_list_user_for_tree.append(product[1]) 
   
    return final_product_list_user_for_tree

def get_list_of_category_candidates_new(in_products_list, in_products_list_user, in_user_sentence, in_main_words):
    preprocessed_sentence = in_user_sentence
    max_match_cnt = 0 
    match_product_list = []
    match_product_list_user = []
    max_main_words_match_cnt = 0
    for row_idx, product in enumerate(in_products_list):  
        match_cnt, main_words_match_cnt = howManyWordsMatch_new(preprocessed_sentence, product, in_main_words)  
        if max_main_words_match_cnt < main_words_match_cnt:
            max_main_words_match_cnt = main_words_match_cnt
        if match_cnt > 0 :             
            match_product_list.append([match_cnt, product])
            match_product_list_user.append([match_cnt, in_products_list_user[row_idx], main_words_match_cnt])
            if match_cnt > max_match_cnt: 
                max_match_cnt = match_cnt 
    
    final_product_list = []     
    for product in match_product_list: 
        if product[0] == max_match_cnt: 
            final_product_list.append(product)
            
    final_product_list_user = [] 
    final_product_list_user_for_tree = [] 
    final_main_words_match_cnt_list = [] 
    for product in match_product_list_user: 
        if product[0] == max_match_cnt: 
            if product[2] >= max_main_words_match_cnt: 
                final_product_list_user.append(product)     
                final_product_list_user_for_tree.append(product[1]) 
                final_main_words_match_cnt_list.append(product[2])                  
        
    return final_product_list_user_for_tree, final_main_words_match_cnt_list, max_match_cnt


def get_list_of_category_candidates_whole(in_products_list, in_products_list_user, in_user_sentence, from_2nd_to_5th):
    preprocessed_sentence = in_user_sentence
    
    match_product_list = []
    match_product_list_user = []
    for row_idx, product in enumerate(in_products_list): 
        splitted = in_user_sentence.split(' ')
        if len(splitted) > 1: 
            if in_user_sentence in product:
                match_product_list.append(product)
                match_product_list_user.append(in_products_list_user[row_idx])
        elif len(splitted) == 1: 
            if from_2nd_to_5th == True: 
                product = product.split('------')[0]
                
            split_product = product.split(' ')
            for product_word in split_product:
                if in_user_sentence == product_word:
                    match_product_list.append(product)    
                    match_product_list_user.append(in_products_list_user[row_idx])
        
    return match_product_list_user

def compareAnd(input_keyword_list, compare_to): 
    real_cnt = 0
    output_list = []
    for dst_sentence in compare_to:
        real_cnt = 0
        for keyword in input_keyword_list:
            if keyword in dst_sentence and keyword != 'none':
                real_cnt = real_cnt + 1
        if real_cnt == len(input_keyword_list):
            output_list.append(dst_sentence)
    return output_list

def compareOR(input_keyword_list, compare_to): 
    output_list = []
    for dst_sentence in compare_to:
        for keyword in input_keyword_list:
            if keyword == 'none': 
                output_list.append(dst_sentence)
                break
            else: 
                splitKeyword = keyword.split(' ')
                splitKeywordLength = len(splitKeyword)
                sameCount = 0
                for sKey in splitKeyword:
                    if sKey in dst_sentence:
                        sameCount += 1
                        
                detectGood = False
                if sameCount == splitKeywordLength:
                    detectGood = True
                
                if detectGood == True:
                    output_list.append(dst_sentence)
                    break   
                if len(keyword.split(' ')) == 2: 
                    keyword = keyword.replace(' ', '') 
                    if keyword in dst_sentence:
                        output_list.append(dst_sentence)
                        break   
    return output_list

def compareExcluded(input_keyword_list, compare_to): 
    output_list = []
        
    for dst_sentence in compare_to:
        real_cnt = 0
        for keyword in input_keyword_list:
            if keyword not in dst_sentence:
                real_cnt = real_cnt + 1
        if real_cnt == len(input_keyword_list):
            output_list.append(dst_sentence)
    return output_list    

def compareWhole(in_main_words_list, in_list_products):
    match_list = []
    if len(in_main_words_list) < 2:
        words = in_main_words_list[0]
    else:
        words = ' '.join(in_main_words_list)
    words = words.strip()
    
    words_nospace = ' ' + words.replace(' ', '') + ' ' 
    words_withspace = ' ' + words.strip() + ' ' 
    for idx, product in enumerate(in_list_products):
        product_only_text = ' ' + product.replace(',', ' ') + ' '
        
        if words_nospace in product_only_text:
            match_list.append(product)
        elif words_withspace in product_only_text:
            match_list.append(product)
    
    return match_list

def howManyWordsMatch(input, compare_to): 
    how_many = 0
    input_split = word_tokenize(input.lower())
                        
    for word in input_split:
        if len(word) < 2: 
            word_1 = ' ' + word + ' '
            word_2 = ' ' + word
            word_3 = word + ' '
            if (word_1 in compare_to) or (word_2 in compare_to) or (word_3 in compare_to):
                how_many = how_many + 1
        else: 
            if word in compare_to:
                how_many = how_many + 1
                print(compare_to)
    return how_many
            
def howManyWordsMatch_new(input, compare_to, main_words): 
    how_many = 0
    main_words_matched_cnt = 0
    input_split = word_tokenize(input.lower())
                        
    for word in input_split:
        if len(word) < 2:
            word_1 = ' ' + word + ' '
            word_2 = ' ' + word
            word_3 = word + ' '
            if (word_1 in compare_to) or (word_2 in compare_to) or (word_3 in compare_to):
                how_many = how_many + 1
        else:            
            if word in compare_to:
                how_many = how_many + 1
    for m_word in main_words:
        if m_word in compare_to:
            main_words_matched_cnt = main_words_matched_cnt + 1
            
    return how_many, main_words_matched_cnt

def compareSpeechTxtToDB_Test(): 
    keywords_1 = input("\nDB파일을 선택하세요.(종료:q)\n-> 1. db/raw_meat_eggs_re_v3.csv\n   2. food_combine_user_db.csv\n->")
    if keywords_1 == '2':
        db_file_name = SEARCH_DB_NAME
    elif keywords_1 == 'q':
        return
    else:
        db_file_name = SIMPLE_TEST_DB_NAME  
    
    db_str_search = make_category_search_db(db_file_name)        
    
    db_str_user = make_user_question_db(USER_DB_NAME)
        
    category_id_and_name_of_6th = ''
    special_options_list = []    
    excluded_keywords = ''
    while(True):
        keywords_1 = input("\n비교 모드를 선택하세요.(종료:q, 포함/제외비교:a, 일치단어수비교:b) \n-> ")
        if keywords_1 == 'q':
            break
        elif keywords_1 == 'a':  
            keywordsCompareA(db_str_search)
        elif keywords_1 == 'b':  
            user_sentence = input("\n비교할 문장을 입력해주세요.(종료:q)(ex: 돼지고기 앞다리살 한근 사줘) \n-> ")   
            if user_sentence == 'q':
                break
            else:
                category_id_and_name_of_6th, special_options_list, excluded_keywords = keywordsCompareB(db_str_search, db_str_user, user_sentence)
       
    return category_id_and_name_of_6th, special_options_list, excluded_keywords

def compareSpeechTxtToDB(sentence_user):
    db_str_search = make_category_search_db(SEARCH_DB_NAME)        
    
    db_str_user = make_user_question_db(USER_DB_NAME)
        
    category_id_and_name_of_6th = ''
    special_options_list = []    
    excluded_keywords = '' 
    
    category_id_and_name_of_6th, special_options_list, excluded_keywords = keywordsCompareB(db_str_search, db_str_user, sentence_user)
       
    return category_id_and_name_of_6th, special_options_list, excluded_keywords

def check_existing_product(in_main_words_list):
    flag_exist = False
    
    words = ' '.join(in_main_words_list)
    words = words.strip()
    
    csv_file = open(PRODUCT_DB_NAME, 'r', encoding='utf-8')
    rdr_products = csv.reader(csv_file)
    
    words_nospace = ' ' + words.replace(' ', '') + ' ' 
    words_withspace = ' ' + words.strip() + ' ' 

    for idx, cols in enumerate(rdr_products):
        if words_nospace in cols[0]:
            flag_exist = True
            break
        if words_withspace in cols[0]:
            flag_exist = True
            break
    csv_file.close()
    
    return flag_exist

def check_existing_product_mix(in_main_words_list):
    flag_exist = False
    
    csv_file = open(PRODUCT_DB_NAME, 'r', encoding='utf-8')
    rdr_products = csv.reader(csv_file)
    
    words = ' '.join(in_main_words_list)
    words = words.strip()    

    if len(in_main_words_list) == 1: 
        words_withspace = ' ' + words.strip() + ' ' 
        for idx, cols in enumerate(rdr_products):
            if words_withspace in cols[0]:
                flag_exist = True
                break
    else: 
        words_nospace = words.replace(' ', '') 
        words_withspace = words 
        for idx, cols in enumerate(rdr_products):
            if words_nospace in cols[0]:
                flag_exist = True
                break
            if words_withspace in cols[0]:
                flag_exist = True
                break
    csv_file.close()
    
    return flag_exist

def check_existing_product_mix_whole(in_main_words_list):
    flag_exist = False
    
    csv_file = open(PRODUCT_DB_NAME, 'r', encoding='utf-8')
    rdr_products = csv.reader(csv_file)
    
    words = ' '.join(in_main_words_list)
    words = words.strip()    

    if len(in_main_words_list) == 1: 
        words_withspace = ' ' + words.strip() + ' '
        for idx, cols in enumerate(rdr_products):
            if words_withspace in cols[0]:
                flag_exist = True
                break
    else: 
        words_withspace = words 
        for idx, cols in enumerate(rdr_products):
            product_only_text = ' ' + cols[0].replace(',', ' ') + ' '
            
            if words_withspace in product_only_text:
                flag_exist = True
                break
           
    csv_file.close()
    
    return flag_exist

if __name__ == "__main__":

    sentence_user = "소고기 국거리 한근 사줘"
    db_str_search = make_category_search_db('makeDB/db/food_combine_search_db.csv')        
    db_str_user = make_user_question_db('makeDB/db/food_combine_user_db.csv')
    
    list_of_category_candidates = get_list_of_category_candidates(db_str_search, db_str_user, sentence_user)
    
    rootnode = make_tree(list_of_category_candidates)

    category_id_and_name_of_6th = ''
    special_options_list = [] 
    excluded_keywords = ''
    category_id_and_name_of_6th, special_options_list, excluded_keywords = search_tree(rootnode)
    
    

