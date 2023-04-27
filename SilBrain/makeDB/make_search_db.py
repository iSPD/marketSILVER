
import csv
import os
import re

from sentence.sentence_preprocessing import sentence_preprocessing, spell_check

MAKE_DB_PATH = os.path.dirname(os.path.realpath(__file__))

def make_category_search_db(csv_file_name):
    f_db = open(csv_file_name, 'r', encoding='utf-8')
    rdr = csv.reader(f_db)
    
    search_db = []
    str_cate = ''
    for curr_category_idx, cols in enumerate(rdr): 
        if cols[0] != '':
            if cols[0] == '4':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[6] +' > '+ cols[7] +' > '+ cols[8] +' ------ ' 
            elif cols[0] == '5':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[6] +' > '+ cols[8] +' > '+ cols[9] +' > '+ cols[10] +' ------ ' #cols[10]=5분류
            elif cols[0] == '3':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[5] +' > '+ cols[6] +' ------ ' 
                
        sixthString = cols[13] + '#' + cols[13].replace(' ', '')
        special = cols[14]
        special = special.split('#')
        specialString = ''
        for sp in special:
            specialString += '#' + sp
            specialString += '#' + sp.replace(' ', '')
        
        product_str = cols[12] +' > '+ sixthString + '          '+ specialString
   
        full_category_name = str_cate + product_str
        search_db.append(full_category_name)
    f_db.close()
        
    return search_db

def make_category_search_db_new(csv_file_name):
    f_db = open(csv_file_name, 'r', encoding='utf-8')
    rdr = csv.reader(f_db)
    
    search_db = []
    str_cate = ''
    for curr_category_idx, cols in enumerate(rdr): 
        if cols[0] != '':
            if cols[0] == '4':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[6] +' > '+ cols[7] +' > '+ cols[8] +' ------ ' 
            elif cols[0] == '5':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[6] +' > '+ cols[8] +' > '+ cols[9] +' > '+ cols[10] +' ------ ' #cols[10]=5분류
            elif cols[0] == '3':                
                str_cate = cols[2] +' > '+ cols[4] +' > '+ cols[5] +' > '+ cols[6] +' ------ ' 
                
        sixthString = cols[13] + '#' + cols[13].replace(' ', '')
        special = cols[14]
        special = special.split('#')
        specialString = ''
        for sp in special:
            specialString += '#' + sp
            specialString += '#' + sp.replace(' ', '')
        
        product_str = cols[12] +' > '+ sixthString + '          '+ specialString
   
        full_category_name = str_cate + product_str
        
        full_category_name = full_category_name.replace('C', " ")
        full_category_name = full_category_name.replace(']', " ")
        full_category_name = full_category_name.replace('[', " ")
        full_category_name = full_category_name.replace('(', " ")
        full_category_name = full_category_name.replace(')', " ")
        full_category_name = full_category_name.replace('/', " ")
        full_category_name = full_category_name.replace('>', " ")
        full_category_name = full_category_name.replace('#', " ")
        full_category_name = re.sub(' +', " ", full_category_name)        
        
        search_db.append(full_category_name)
    f_db.close()
        
    return search_db
            
if __name__ == "__main__":
    
    db = make_category_search_db('db/food_combine_search_db.csv')
    print(db)
    
   
    