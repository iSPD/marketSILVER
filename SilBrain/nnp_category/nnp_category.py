
import csv
import os

_curr_dir_ = os.path.dirname(os.path.realpath(__file__))

from nnp_category.word_frequency import get_word_frequency_from_wordlist

def load_nnp_category_db():
    db_nnp_cate = []
    rddir = os.path.join(_curr_dir_, 'db')
    
    IS_SIMPLE = False  
    
    if IS_SIMPLE == True:
        file_nnp_cate = open(os.path.join(rddir, 'nnp_category_all_simple.csv'), 'r', encoding='utf-8')
    else:
        file_nnp_cate = open(os.path.join(rddir, 'nnp_category_all_v2.csv'), 'r', encoding='utf-8')
    
    rdr_nnp_cate = csv.reader(file_nnp_cate)
    
    if IS_SIMPLE == True:
        for cols in rdr_nnp_cate:
            db_nnp_cate.append(cols)
    else:
        for cols in rdr_nnp_cate:
            db_nnp_cate.append([cols[0],cols[1],cols[2],cols[4],cols[3]])
    file_nnp_cate.close()
    
    return db_nnp_cate

def __function2(in_nnp_cate_db, in_sentence_user):
    candidates_by_word = {}
    candidates_all = []
    splitted = in_sentence_user.split(' ') 
    
    empty_list_words = []  
    save_cateID_only = [] 
    valid_word_count = len(splitted)  
    main_words = []
    for user_word in splitted:
        sub_candidates = []
        sign = ''        
        for cols in in_nnp_cate_db:  
            if user_word == cols[1]: 
                sign = cols[0]
                sub_candidates.append(cols)
                candidates_all.append(cols)
                print(cols)
                save_cateID_only.append(cols[3])
                
        
        candidates_by_word[user_word] = sub_candidates.copy()
        
        len_list = len(sub_candidates)
        
        if sign == 'm':
            if user_word not in main_words:
                main_words.append(user_word)
        if len_list == 0:
            empty_list_words.append(user_word)
            valid_word_count = valid_word_count - 1
        
        sub_candidates.clear()
    
    frequency_dic = get_word_frequency_from_wordlist(save_cateID_only)
    
    wow_dic = {}  
    m_dic = {}  
    golden = []
    candidates = []
    max_freq = 0
    wow_words = [] 
    for item in frequency_dic:
        id_in_freq = item[0]   
        freq_in_freq = item[1] 
        
        if max_freq < freq_in_freq:
            max_freq = freq_in_freq  
        if freq_in_freq > (max_freq-1): 
            wow_dic[id_in_freq] = 0   
            m_dic[id_in_freq] = 0   
            for candidate in candidates_all: 
                id = candidate[3]
                if id == id_in_freq:
                    if candidate[2] == 'W':
                        wow_dic[id_in_freq] = wow_dic[id_in_freq] + 1
                        if candidate[1] not in wow_words:
                            wow_words.append(candidate[1])  
                    if candidate[0] == 'm':
                        m_dic[id_in_freq] = m_dic[id_in_freq] + 1
            
            if freq_in_freq == valid_word_count and wow_dic[id_in_freq] == valid_word_count and m_dic[id_in_freq] > 0:
                golden.append(id_in_freq)
            else:
                if m_dic[id_in_freq] != 0: 
                    candidates.append(id_in_freq)
        else:
            continue
        
    if len(golden) > 0:
        print(golden)
        return golden, wow_words, main_words, True, max_freq  
    else:
        print(candidates)
        return candidates, wow_words, main_words, False, max_freq


def __function3(in_nnp_cate_db, in_sentence_user):
    candidates_all = []
    splitted = in_sentence_user.split(' ') 

    empty_list_words = []  
    save_cateID_only = [] 
    save_cateName_only = [] 
    valid_word_count = len(splitted)  
    main_words = []
    q_words = []
    for user_word in splitted:
        sub_candidates = []
        sign = ''        
        for cols in in_nnp_cate_db:   
            sign = cols[0]
                    
            if user_word == cols[1]:
                print(cols)
                if sign == 'm': 
                    sub_candidates.append(cols)
                    candidates_all.append(cols)
                    save_cateID_only.append(cols[3])    
                    save_cateName_only.append(cols[4])            
                    if user_word not in main_words:
                        main_words.append(user_word)
                elif sign == 'q':
                    if user_word not in q_words:
                        q_words.append(user_word)
                
        len_list = len(sub_candidates)
        if len_list == 0:
            empty_list_words.append(user_word)
            valid_word_count = valid_word_count - 1
            
        sub_candidates.clear()
    
    frequency_dic = get_word_frequency_from_wordlist(save_cateID_only)
    
    wow_dic = {}  
    m_dic = {}  
    golden = []
    candidates = []
    max_freq = 0
    wow_words = []
    for item in frequency_dic:
        id_in_freq = item[0]   
        freq_in_freq = item[1] 
        
        if max_freq < freq_in_freq:
            max_freq = freq_in_freq  
        if freq_in_freq > (max_freq-1): 
            wow_dic[id_in_freq] = 0   
            m_dic[id_in_freq] = 0   
            for candidate in candidates_all: 
                id = candidate[3]
                if id == id_in_freq:
                    if candidate[2] == 'W':
                        wow_dic[id_in_freq] = wow_dic[id_in_freq] + 1
                        if candidate[1] not in wow_words:
                            wow_words.append(candidate[1])  
                    if candidate[0] == 'm':
                        m_dic[id_in_freq] = m_dic[id_in_freq] + 1
            
            if freq_in_freq == valid_word_count and wow_dic[id_in_freq] == valid_word_count and m_dic[id_in_freq] > 0:
                
                golden.append(id_in_freq)
            else:
                if m_dic[id_in_freq] != 0: 
                    candidates.append(id_in_freq)
        else:
            continue    
    
    return save_cateID_only, main_words, q_words, empty_list_words

   
def __function4(in_nnp_cate_db, in_sentence_user):
   
    info_in_order = []
    candidates_all = []
    splitted = in_sentence_user.split(' ') 

    empty_list_words = []  
    save_cateID_only = [] 
    save_cateName_only = [] 
    valid_word_count = len(splitted)  
    main_words_list = []
    q_words = []
    for user_word in splitted:
        sub_candidates = []
        sub_ids = ''  
        sign = ''        
        for cols in in_nnp_cate_db:   
            sign = cols[0]
                    
            if user_word == cols[1]:
                if sign == 'm': 
                    sub_candidates.append(cols)
                    sub_ids = sub_ids + '#' + cols[3]
                    candidates_all.append(cols)
                    save_cateID_only.append(cols[3])    
                    save_cateName_only.append(cols[4])            
                    if user_word not in main_words_list:
                        main_words_list.append(user_word)
                elif sign == 'q':
                    sub_candidates.append(cols)
                    if user_word not in q_words:
                        q_words.append(user_word)                
        
        len_list = len(sub_candidates)
            
        curr_sign = ''    
        if len_list == 0:
            curr_sign = 'x'
            empty_list_words.append(user_word)
            valid_word_count = valid_word_count - 1
        else:# q or m
            curr_sign = sub_candidates[0][0]
        info_in_order.append([user_word, curr_sign, sub_ids.strip('#')])       
        
        sub_candidates.clear()

    return info_in_order, main_words_list, q_words
      
def get_category_candidates_from_NNPCate(in_nnp_cate_db, in_sentence_user):
    candidates, wow_words, main_words_list, is_golden, max_freq = __function2(in_nnp_cate_db, in_sentence_user)
    
    return candidates, wow_words, main_words_list, is_golden, max_freq


def get_category_candidates_from_NNPCate_v2(in_nnp_cate_db, in_sentence_user):
    candidates_all, main_words_list, q_words, empty_list_words = __function3(in_nnp_cate_db, in_sentence_user)
    
    return candidates_all, main_words_list, q_words, empty_list_words

def get_nnp_category_info(in_sentence_user):
    db_nnp_category = load_nnp_category_db()
    info_in_order, main_words_list, q_words = __function4(db_nnp_category, in_sentence_user)
    
    return info_in_order, main_words_list, q_words

def get_final_candidates(in_6th_db, in_nnpcate_db):     
    final_candidates = []
    final_candidates = in_6th_db.copy()
    
    for item in in_nnpcate_db:
        if item not in in_6th_db:
            final_candidates.append(item)
            
    return final_candidates
    