import csv
import os
import pandas as pd
import shutil

from makeDB.make_search_db import MAKE_DB_PATH

_curr_dir_ = os.path.dirname(os.path.realpath(__file__))

def excelToCSVs(in_excel_file):
    wrdir_user_db = os.path.join(_curr_dir_, 'out_user')
    wrdir_search_db = os.path.join(_curr_dir_, 'out_search')
            
    if os.path.exists(wrdir_user_db):
        shutil.rmtree(wrdir_user_db)
    if os.path.exists(wrdir_search_db):
        shutil.rmtree(wrdir_search_db)    
        
    os.makedirs(wrdir_user_db, exist_ok=True)
    os.makedirs(wrdir_search_db, exist_ok=True)
    
    excel_file_name = in_excel_file
    names = ['01과일', '02건과,견과', '03채소', '04쌀,잡곡', '05축산,계란', '06수산,건어물', '07생수,음료', 
            '08커피,원두,차', '09과자,초콜릿,시리얼', '10면,통조림,가공식품', '11가루,조미료,오일', 
            '12장,소스,드레싱,식초', '13유제품,아이스크림', '14냉장,냉동,간편요리', '15건강식품', 
            '16반찬,간편식,대용식', 
            '01과일_re', '02건과,견과_re', '03채소_re', '04쌀,잡곡_re', '05축산,계란_re', '06수산,건어물_re', '07생수,음료_re', 
            '08커피,원두,차_re', '09과자,초콜릿,시리얼_re', '10면,통조림,가공식품_re', '11가루,조미료,오일_re', 
            '12장,소스,드레싱,식초_re', '13유제품,아이스크림_re', '14냉장,냉동,간편요리_re', '15건강식품_re', 
            '16반찬,간편식,대용식_re']
    excels_sheets = pd.read_excel(excel_file_name,
	sheet_name=names, #[0, 'sheet2'],
	engine='openpyxl')
    
    for sheetname in names:
        if '_re' in sheetname:
            excels_sheets[sheetname].to_csv(f"{wrdir_search_db}/{sheetname}.csv", encoding='utf-8', index=False,float_format='%d', header=False)
        else:
            excels_sheets[sheetname].to_csv(f"{wrdir_user_db}/{sheetname}.csv", encoding='utf-8', index=False,float_format='%d', header=False)

def check_delete_words(in_str):
    out_str = ''
    if 'ddd' in in_str:
        splitted = in_str.split('ddd')
        out_str = splitted[0]
    else:
        out_str = in_str   
    return out_str

def combineCSVs(in_rddir, in_rddir2, in_wrdir):
    rddir = os.path.join(_curr_dir_, in_rddir)
    rddir2 = os.path.join(_curr_dir_, in_rddir2)
       
    wrdir = os.path.join(MAKE_DB_PATH, in_wrdir)
    
    if os.path.exists(wrdir):
        shutil.rmtree(wrdir)
        
    os.makedirs(wrdir, exist_ok=True)
    
    prefix = 'food_combine'
    file_list = os.listdir(rddir)
    file_list.sort() 
    file_list_csv = [file for file in file_list if file.endswith(".csv")]
    
    wrfile_user = open(os.path.join(wrdir,f"{prefix}_user_db.csv"), 'w', newline='', encoding='utf-8')
    writer_csv_user = csv.writer(wrfile_user)
    wrfile_search = open(os.path.join(wrdir,f"{prefix}_search_db.csv"), 'w', newline='', encoding='utf-8')
    writer_csv_search = csv.writer(wrfile_search)
    
    for csvfilename in file_list_csv:
        csvfile_user = open(os.path.join(rddir, csvfilename), 'r', encoding='utf-8')
        rdr_user = csv.reader(csvfile_user)
        csvfile_search = open(os.path.join(rddir2, f"{csvfilename.split('.csv')[0]}_re.csv"), 'r', encoding='utf-8')
        rdr_search = csv.reader(csvfile_search)
        
        search_db_list = []
        for content in rdr_search:
            search_db_list.append(content)
        
        for idx, cols in enumerate(rdr_user):
        
            cols[12] = check_delete_words(cols[12])  #5.5분류
            cols[13] = check_delete_words(cols[13])  #6분류
            cols[14] = check_delete_words(cols[14])  #유의어
            
            cols[16] = check_delete_words(cols[16])  #특화1
            cols[17] = check_delete_words(cols[17])  #특화2
            cols[18] = check_delete_words(cols[18])  #특화3
            cols[20] = check_delete_words(cols[20])  #제외키워드
            if cols[16] == '': 
                cols[15] = ''  #특화개수  
            
            writer_csv_user.writerow(cols[0:21])  
            writer_csv_search.writerow([search_db_list[idx][0], search_db_list[idx][1], search_db_list[idx][2], 
                                        search_db_list[idx][3], search_db_list[idx][4], search_db_list[idx][5], 
                                        search_db_list[idx][6], search_db_list[idx][7], search_db_list[idx][8], 
                                        search_db_list[idx][9], search_db_list[idx][10], search_db_list[idx][11],
                                        cols[12], cols[13], cols[14], cols[15], cols[16], cols[17], cols[18] ])
            
        csvfile_user.close()
        csvfile_search.close()
        search_db_list.clear()
        
    wrfile_user.close()
    wrfile_search.close()


def update_db_from_excel(in_excel_file):
    
    excelToCSVs(in_excel_file)
    combineCSVs('out_user', 'out_search', 'db')
    