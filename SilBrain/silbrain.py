
import os

from compare.compare_db import SEARCH_DB_NAME, USER_DB_NAME, get_list_of_category_candidates, get_list_of_category_candidates_new, get_list_of_category_candidates_whole, compare_keywords_within_crawled_products
from compare.compare_db import check_existing_product_mix_whole
from network.webdriver_setting import driverSettingWin
from network.get_product_list import get_product_list_in_category
from network.get_product_list import keyword_search
from makeDB.make_question_db import make_user_question_db
from makeDB.make_search_db import make_category_search_db, make_category_search_db_new
from makeTree.make_tree import make_tree, draw_tree, search_tree
from updateDB.update_db import update_db_from_excel
from nnp_category.nnp_category import load_nnp_category_db, get_category_candidates_from_NNPCate, get_category_candidates_from_NNPCate_v2, get_nnp_category_info, get_final_candidates

_curr_dir_ = os.path.dirname(os.path.realpath(__file__))
    
def get_category6th_candidates(in_sentence_user):
    
    in_sentence_user = in_sentence_user.replace('#', ' ')
    in_sentence_user = in_sentence_user.strip()
    db_str_search = make_category_search_db(SEARCH_DB_NAME)        
    db_str_user = make_user_question_db(USER_DB_NAME)
    
    list_of_category_candidates = []
    list_of_category_candidates = get_list_of_category_candidates(db_str_search, db_str_user, in_sentence_user)
    
    return list_of_category_candidates
       
def save_file(in_list):
    filePath = './makeDB/db/search_db_str.txt'
    str = '\n'.join(in_list)
    with open(filePath, 'w', newline='\n', encoding='utf-8') as lf:
        lf.writelines(str)

def __get_categories_by_id(db_str_search, db_str_user, in_nnp_cate_info):
    nnp_cate_candidates = []
    cate_ids = in_nnp_cate_info[0][2].split('#')
    for cate_id in cate_ids:
        candi = get_list_of_category_candidates_whole(db_str_search, db_str_user, cate_id, False)
        for item in candi: 
            nnp_cate_candidates.append(item)
    return nnp_cate_candidates, cate_ids

def search_by_q_words(in_q_words_list, in_note_str):
    db_str_search = make_category_search_db_new(SEARCH_DB_NAME)        
    db_str_user = make_user_question_db(USER_DB_NAME)
    q_words_list = in_q_words_list     
    
    words_no_space = ''.join(q_words_list)
    candi_in_5th_db = get_list_of_category_candidates_whole(db_str_search, db_str_user, words_no_space, True)
    
    return candi_in_5th_db, in_note_str


def search_by_main_words(in_user_words_list, in_note_str):
    db_str_search = make_category_search_db_new(SEARCH_DB_NAME)        
    db_str_user = make_user_question_db(USER_DB_NAME)
    save_file(db_str_search) #for debug
        
    final_candidates = []    
    flag_search_by_keyword = False
    
    main_words_list = in_user_words_list     
    
    if len(main_words_list) == 1: 
        nnp_cate_info, main_words, q_words = get_nnp_category_info(main_words_list[0]) 
        nnp_cate_candidates, cate_ids = __get_categories_by_id(db_str_search, db_str_user, nnp_cate_info)
        candi_in_5th_db = get_list_of_category_candidates_whole(db_str_search, db_str_user, main_words_list[0], True)
        
        if len(candi_in_5th_db) > 0:
            final_candidates = candi_in_5th_db.copy()
        else:
            candi_in_6th_db = get_list_of_category_candidates_whole(db_str_search, db_str_user, main_words_list[0], False)
            if len(candi_in_6th_db) > 0: 
                final_candidates = candi_in_6th_db.copy()
            else: 
                flag_search_by_keyword = True
        
    else: 
        main_words_nospace = ''.join(main_words_list)
        candi_in_6th_db = get_list_of_category_candidates_whole(db_str_search, db_str_user, main_words_nospace, False)
        
        if len(candi_in_6th_db) > 0:
            final_candidates = candi_in_6th_db.copy()
        else:
            main_words_with_space = ' '.join(main_words_list)
            candi_in_6th_db_whole = get_list_of_category_candidates_whole(db_str_search, db_str_user, main_words_with_space, False)
            if len(candi_in_6th_db_whole) > 0:
                final_candidates = candi_in_6th_db_whole.copy()
            else: 
                candi_in_6th_db_included, list_of_main_words_match_cnt, max_match_cnt_6th = get_list_of_category_candidates_new(db_str_search, db_str_user, main_words_with_space, main_words_list)
                for idx, candi in enumerate(candi_in_6th_db_included):
                    if list_of_main_words_match_cnt[idx] == len(main_words_list): 
                        final_candidates.append(candi)
                if len(final_candidates) <= 0:
                    flag_search_by_keyword = True
    
    return final_candidates, flag_search_by_keyword, in_note_str

def pre_search(driver, in_sentence_user, do_keyword_search):
    in_sentence_user = in_sentence_user.strip() 
    
    splitted = in_sentence_user.split('#')
    sentence_1st = splitted[0]
    sentence_2nd = ''
    if len(splitted) == 2:
        sentence_2nd = splitted[1]
    
    input_words = []  
        
    nnp_cate_info, main_words_list, q_words = get_nnp_category_info(sentence_1st)    
    if len(main_words_list) == 0: 
        if sentence_2nd != '':
            
            nnp_cate_info2, main_words_list2, q_words2 = get_nnp_category_info(sentence_2nd)
            if len(main_words_list2) > 0: 
                input_words = main_words_list2
    else: 
        input_words = main_words_list  
        
    flag_exist = check_existing_product_mix_whole(input_words) # 한단어, 두 단어 이상 모두 그대로 whole 검색
    
    result_list = []
    result_list_link = []
    
    if flag_exist == True and do_keyword_search == True:
        result_list, result_list_link, rank, rank_link = keyword_search(driver, input_words, do_string_compare=True)
    
    return flag_exist, result_list, result_list_link

def add_note(in_note_str, input_str):
    in_note_str = in_note_str + '\n' + input_str
    return in_note_str

STATUS_NONE = 0
STATUS_CANDIDATE_OK = 1
STATUS_GOTO_KEYWORD_SEARCH = 2
STATUS_GOTO_KEYWORD_SEARCH_DIRECT = 3
STATUS_ERROR = 4

def get_category6th_candidates_new_v3(in_sentence_user):
    note_str = ''
    
    ret_status = STATUS_NONE
    in_sentence_user = in_sentence_user.strip() # 앞뒤공백 제거
    
    nnp_cate_candidates = []
    q_words = []
    q_words2 = []
    ret_main_words = []
    flag_search_by_keyword = False
    
    splitted = in_sentence_user.split('#')
    sentence_1st = splitted[0]
    sentence_2nd = ''
    if len(splitted) == 2:
        sentence_2nd = splitted[1]
    nnp_cate_info, main_words_list, q_words = get_nnp_category_info(sentence_1st)

    if len(main_words_list) == 0: 
        if sentence_2nd != '':
            nnp_cate_info2, main_words_list2, q_words2 = get_nnp_category_info(sentence_2nd)
            if len(main_words_list2) > 0: 
                nnp_cate_candidates, flag_search_by_keyword, note_str = search_by_main_words(main_words_list2, note_str) 
                if len(nnp_cate_candidates) > 0:
                    ret_status = STATUS_CANDIDATE_OK
                else:
                    ret_main_words = main_words_list2
                    ret_status = STATUS_GOTO_KEYWORD_SEARCH
            else: 
                ret_status = STATUS_ERROR
        else: 
            if len(q_words) > 0: 
                nnp_cate_candidates, note_str = search_by_q_words(q_words, note_str)
                if len(nnp_cate_candidates) > 0:
                    ret_status = STATUS_CANDIDATE_OK
                else:
                    ret_status = STATUS_ERROR
            else:
                ret_status = STATUS_ERROR
    else: 
        nnp_cate_candidates, flag_search_by_keyword, note_str = search_by_main_words(main_words_list, note_str)
        
        if len(nnp_cate_candidates) > 0:
            ret_status = STATUS_CANDIDATE_OK
        else:
            if sentence_2nd != '':
                nnp_cate_info2, main_words_list2, q_words2 = get_nnp_category_info(sentence_2nd)
                
                if len(main_words_list2) > 0: 
                    nnp_cate_candidates, flag_search_by_keyword, note_str = search_by_main_words(main_words_list2, note_str)  
                    if len(nnp_cate_candidates) > 0:
                        ret_status = STATUS_CANDIDATE_OK
                    else:
                        ret_main_words = main_words_list2
                        ret_status = STATUS_GOTO_KEYWORD_SEARCH 
                else: 
                    ret_status = STATUS_ERROR
            else:
                ret_main_words = main_words_list
                ret_status = STATUS_GOTO_KEYWORD_SEARCH
    
    q_words_final = []
    candidate_final = []
    if flag_search_by_keyword == False:
        if len(q_words) > 0 or len(q_words2) > 0: 
            for candidate in nnp_cate_candidates:
                for qword in q_words: 
                    if qword in candidate:
                        if candidate not in candidate_final:
                            candidate_final.append(candidate)
                for qword2 in q_words2: 
                    if qword2 in candidate:
                        if candidate not in candidate_final:
                            candidate_final.append(candidate)
                            
            if len(candidate_final) == 0:
                candidate_final = nnp_cate_candidates.copy()
        else: 
            candidate_final = nnp_cate_candidates.copy()
            
        q_words_final = q_words + q_words2

    return ret_status, candidate_final, q_words_final, ret_main_words, note_str
 
def ready_web():
    driver = driverSettingWin()
    return driver

def quit_web(driver):
    driver.quit()    

def pre_curation(driver, in_product6th, in_options, in_excluded, in_tmstamp, in_max_num_of_products):
    q_file_name = os.path.join(_curr_dir_, f"{in_tmstamp}.txt")
    q_words = []
    if os.path.isfile(q_file_name) == True:
        q_file = open(q_file_name, 'r', encoding='utf-8')
        line = q_file.readline()
        line = line.strip()
        if line != 'none':
            q_words = line.split(' ')
    
    splitted = in_product6th.split('&')
    category_id = splitted[0] #194736
    product_name_and_synonyms = splitted[1] 
    
    special_options_list = in_options 
    excluded_keywords = in_excluded 
    
    if len(q_words) > 0:
        new_excluded_keywords = ''
        sp_excluded = excluded_keywords.split('#')
        new_excluded = []
        for q_word in q_words:
            for exc in sp_excluded:
                if exc != q_word:
                    if exc not in new_excluded:
                        new_excluded.append(exc)
        new_excluded_keywords = '#'.join(new_excluded)
    else:
        new_excluded_keywords = excluded_keywords
    result_list, result_list_link = get_product_list_in_category(driver, category_id, product_name_and_synonyms, special_options_list, new_excluded_keywords, q_words, in_max_num_of_products) #임시주석
    
    if len(result_list) < in_max_num_of_products:
        cnt = len(result_list)
    else:
        cnt = in_max_num_of_products      
    
    if cnt == 2: 
        products_cnt2 = []
        links_cnt2 = []
        price0_str = result_list[0].split('#')[1]
        price1_str = result_list[1].split('#')[1]
        prod_0_price = int(price0_str.replace('원','').replace(',',''))
        prod_1_price = int(price1_str.replace('원','').replace(',',''))
        if prod_0_price > prod_1_price: 
            products_cnt2.append(result_list[1])
            products_cnt2.append(result_list[0])
            links_cnt2.append(result_list_link[1])
            links_cnt2.append(result_list_link[0])
            return products_cnt2, links_cnt2   
        else:
            return result_list[0:cnt], result_list_link[0:cnt]     
    
    else:    
        return result_list[0:cnt], result_list_link[0:cnt]

from compare.compare_db import compare_keywords_within_crawled_products_v2
def pre_curation_2(in_product_list, in_product_list_link, in_main_words, in_q_words, in_max_num_of_products):
    
    if len(in_main_words) == 0:
        return [], []
    
    match_list = compare_keywords_within_crawled_products_v2(in_product_list, in_main_words, in_q_words)
    link_list = []
    for matched in match_list:
        for idx, product in enumerate(in_product_list):
            if matched in product:
                link_list.append(in_product_list_link[idx])
                break
    if len(match_list) < in_max_num_of_products:
        cnt = len(match_list)
    else:
        cnt = in_max_num_of_products        
    return match_list[0:cnt], link_list[0:cnt]
            
def update_DB():
    filepath = os.path.dirname(os.path.realpath(__file__))
    update_db_from_excel(os.path.join(filepath, "updateDB/in/Foods_6th_DB_v1.5.xlsx"))

def make_search_keywords(in_user_sentence):
    
    keyword = ''
    nnp_cate_info, lst_main_words, lst_q_words = get_nnp_category_info(user_sentence_list[0])
    
    if len(lst_main_words) == 0 and len(lst_q_words) == 0:  
        if len(user_sentence_list) == 2: 
            nnp_cate_info, lst_main_words, lst_q_words = get_nnp_category_info(user_sentence_list[1])
            if len(lst_main_words) == 0 and len(lst_q_words) == 0: 
                print(f"return null")
            else:     
                for info in nnp_cate_info:
                    if info[1] != 'x':
                        keyword = keyword + ' ' + info[0]
                keyword = keyword.strip()
    else: 
        for info in nnp_cate_info:
            if info[1] != 'x':
                keyword = keyword + ' ' + info[0]
        keyword = keyword.strip()
        
    return keyword, keyword.split(' ') 

from get_timestamp import get_timestamp
def get_category6th_candidates_mix(driver, in_user_sentence, in_max_num_of_products):  
    tmstamp = get_timestamp()
    ret_status = STATUS_NONE
    note_str = ''
    search_keyword = []
    flag_direct_search = False
    flag_string_compare_in_products = True 
    flag_search_keyword_full = True 
    if '@' in in_user_sentence:  
        in_user_sentence = in_user_sentence.replace('@', '')
        search_keyword = in_user_sentence.split('#')
        flag_direct_search = True
    elif '*' in in_user_sentence: 
        in_user_sentence = in_user_sentence.replace('*', '')
        search_keyword = in_user_sentence.split('#')
        flag_search_keyword_full = False
        flag_direct_search = True
    elif '!' in in_user_sentence:
        in_user_sentence = in_user_sentence.replace('!', '')
        search_keyword = in_user_sentence.split('#')
        flag_direct_search = True
        flag_string_compare_in_products = False
        
        
    if flag_direct_search == True:
        ret_status = STATUS_GOTO_KEYWORD_SEARCH_DIRECT
    else:    
        ret_status, list_of_category_candidates, q_words, main_words, note_str = get_category6th_candidates_new_v3(in_user_sentence)            
        
        
    if ret_status == STATUS_CANDIDATE_OK:
        q_word_file = open(os.path.join(_curr_dir_, f"{tmstamp}.txt"), 'w', newline='', encoding='utf-8')
        if len(q_words) == 0:
            q_word_file.write('none')
        else: 
            q_str = ' '.join(q_words)   
            q_word_file.write(q_str)
        q_word_file.close()
            
        rootnode = make_tree(list_of_category_candidates)
        category_id_and_name_of_6th, special_options_list, excluded_keywords = search_tree(rootnode) 
        
        if category_id_and_name_of_6th != '':
            products, links = pre_curation(driver, category_id_and_name_of_6th, special_options_list, excluded_keywords, tmstamp, in_max_num_of_products) 
            
            return tmstamp, 'product-search-done', products, links, note_str  
    elif ret_status == STATUS_GOTO_KEYWORD_SEARCH:
        flag_exist, result_list, result_list_link = pre_search(driver, in_user_sentence, do_keyword_search=True) 
        if flag_exist == True:
            products, links = pre_curation_2(result_list, result_list_link, main_words, q_words, in_max_num_of_products) 
            return tmstamp, 'product-search-now', [], [], note_str
        else:
            num_of_m_words = len(main_words)
            
            combine = ''
            if num_of_m_words == 3:
                combine_1 = main_words[0] + ' ' + main_words[2]
                combine_2 = main_words[1] + ' ' + main_words[2]
                if check_existing_product_mix_whole(combine_1.split(' ')) == True:
                    combine = combine_1
                if check_existing_product_mix_whole(combine_2.split(' ')) == True:
                    combine = combine + '#' + combine_2
                combine = combine.strip('#')                
            elif num_of_m_words == 4:
                combine_1 = main_words[0] + ' ' + main_words[3]
                combine_2 = main_words[1] + ' ' + main_words[3]
                combine_3 = main_words[2] + ' ' + main_words[3]
                combine_4 = main_words[0] + ' ' + main_words[1] + ' ' + main_words[3]
                combine_5 = main_words[0] + ' ' + main_words[2] + ' ' + main_words[3]
                combine_6 = main_words[1] + ' ' + main_words[2] + ' ' + main_words[3]
                if check_existing_product_mix_whole(combine_1.split(' ')) == True:
                    combine = combine_1
                if check_existing_product_mix_whole(combine_2.split(' ')) == True:
                    combine = combine + '#' + combine_2
                if check_existing_product_mix_whole(combine_3.split(' ')) == True:
                    combine = combine + '#' + combine_3
                if check_existing_product_mix_whole(combine_4.split(' ')) == True:
                    combine = combine + '#' + combine_4
                if check_existing_product_mix_whole(combine_5.split(' ')) == True:
                    combine = combine + '#' + combine_5
                if check_existing_product_mix_whole(combine_6.split(' ')) == True:
                    combine = combine + '#' + combine_6    
            
            if combine == '':
                combine = 'none'
            else:
                combine = combine.strip('#')
            main_words.append(combine)            
            return tmstamp, 'is-this-or-that', main_words, [], note_str
    
    elif ret_status == STATUS_GOTO_KEYWORD_SEARCH_DIRECT:
        if flag_search_keyword_full == True:  
            search_keyword_string = search_keyword[0]  
            list_keywords = search_keyword_string.split(' ')
        else:
            search_keyword_string, list_keywords = make_search_keywords(in_user_sentence)
                
        result_list, result_list_link, rank_prod, rank_prod_link = keyword_search(driver, list_keywords, do_string_compare=flag_string_compare_in_products) 
                
        if flag_string_compare_in_products == True:  
            products = []
            links = []
            for keyword in search_keyword: 
                if flag_search_keyword_full == True: 
                    products_tmp, links_tmp = pre_curation_2(result_list, result_list_link, keyword.split(' '), [], in_max_num_of_products) 
                else:
                    nnp_cate_info, lst_main_words, lst_q_words = get_nnp_category_info(keyword)
                    products_tmp, links_tmp = pre_curation_2(result_list, result_list_link, lst_main_words, lst_q_words, in_max_num_of_products) 
                
                list_tmp = []
                for idx, product in enumerate(products_tmp):
                    if product not in products:
                        list_tmp.append(product)
                        products.append(product)
                        links.append(links_tmp[idx])
                list_tmp.clear()
                
            if len(products) == 0:
                products = rank_prod.copy()
                links = rank_prod_link.copy()
         
            if len(products) < in_max_num_of_products:
                cnt = len(products)
            else:
                cnt = in_max_num_of_products                 
            
            if cnt == 2: # DIRTY-CODE
                products_cnt2 = []
                links_cnt2 = []
                price0_str = products[0].split('#')[1]
                price1_str = products[1].split('#')[1]
                prod_0_price = int(price0_str.replace('원','').replace(',',''))
                prod_1_price = int(price1_str.replace('원','').replace(',',''))
                if prod_0_price > prod_1_price: 
                    products_cnt2.append(products[1])
                    products_cnt2.append(products[0])
                    links_cnt2.append(links[1])
                    links_cnt2.append(links[0])
                    return tmstamp, 'product-search-now-alert', products_cnt2, links_cnt2, note_str   
                else:
                    return tmstamp, 'product-search-now-alert', products[0:cnt], links[0:cnt], note_str     
            
            else:    
                return tmstamp, 'product-search-now-alert', products[0:cnt], links[0:cnt], note_str
        else:
            return tmstamp, 'product-search-now-alert', result_list[0:in_max_num_of_products], result_list_link[0:in_max_num_of_products], note_str
            
    elif ret_status == STATUS_ERROR:
        return tmstamp, 'speak-again', [], [], note_str
    
    else:
        return tmstamp, 'error', [], [], note_str
        
            
import sys
if __name__ == "__main__":
    TEST_ON_WEB = True
    if TEST_ON_WEB == True:
        driver = ready_web()
        
    while(True):
        sentence_in = input("문장 입력(q:exit) : ")
        if sentence_in == 'q' or sentence_in == 'ㅂ':
            break
        else:
            
            update_DB()
            sentence_user = sentence_in
            
            TEST_MODE = 1
            
            timestamp, status, list_of_candidates, list_of_links, note_str = get_category6th_candidates_mix(driver, sentence_user, 2)
                
    if TEST_ON_WEB == True:
        quit_web(driver)