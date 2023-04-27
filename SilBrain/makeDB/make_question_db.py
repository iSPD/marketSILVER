
import csv
import re
from sentence.sentence_preprocessing import sentence_preprocessing, spell_check

def clean_category_name(in_str):
    names = in_str.split('>')
    out_str = ''
    for name in names:
        hashwords = name.split('#')
        representative_word = hashwords[0]    
        if len(hashwords) > 0:
            for hashword in hashwords:
                if 'C' in hashword:
                    representative_word = hashword.replace('C','')
                    break
        representative_word = representative_word.replace('[','')    
        representative_word = representative_word.replace(']','')
        out_str = out_str + '>' + representative_word
    
    return out_str

def make_user_question_db(csv_file_name):
    user_question_db = []    
    f_db_user = open(csv_file_name, 'r', encoding='utf-8')
    rdr_user = csv.reader(f_db_user)
    str_cate_user = ''
    semi_category = ''
    category_id = ''
    for idx, cols in enumerate(rdr_user): 
        if cols[0] != '':
            semi_category = ''
            if cols[0] == '4':
                category_id = cols[7]
                str_cate_user = cols[2] +'>'+ cols[4] +'>'+ cols[6] +'>'+ cols[8]
            elif cols[0] == '5':
                category_id = cols[9]
                str_cate_user = cols[2] +'>'+ cols[4] +'>'+ cols[6] +'>'+ cols[8] +'>'+ cols[10]    #cols[10]=5분류
            elif cols[0] == '3':
                category_id = cols[5]
                str_cate_user = cols[2] +'>'+ cols[4] +'>'+ cols[6]
                    
        if cols[12] != '':
            semi_category = cols[12]
        str_cate_user = clean_category_name(str_cate_user)     
        str_cate_user = re.sub(r"^>+","",str_cate_user)  
        name_for_user = '> K6&' + category_id + '&' + cols[13]   
        if cols[14] != '': 
            synonyms = cols[14] 
            name_for_user = name_for_user + '&' + synonyms 
               
        if semi_category != '':   
            full_category_name = str_cate_user + '>' + semi_category + name_for_user               
        else:                     
            full_category_name = str_cate_user + name_for_user    
        
        option_for_user_full = '' 
        if cols[15] != '':    

            int_option_cnt = int(cols[15])
            for idx in range(0, int_option_cnt):
                option_for_user_full = option_for_user_full + '&' + cols[16+idx]
            option_for_user_full = re.sub(r"^&+","",option_for_user_full)  
            full_category_name = f"{full_category_name}>K7_{int_option_cnt}_{option_for_user_full}"  
        
        except_keywords = ''
        if cols[20] != '':
            except_keywords = cols[20]
            full_category_name = f"{full_category_name}>K8_{except_keywords}"

        user_question_db.append(full_category_name)
        
    return user_question_db

            
if __name__ == "__main__":
    
    db = make_user_question_db('db/food_combine_user_db.csv')
    print(db)
    