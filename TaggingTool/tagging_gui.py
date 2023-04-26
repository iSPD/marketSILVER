import csv
import math
import os
import re
import time
import tkinter as tk
from tkinter import filedialog as fd
    
def load_product_txt(filename, in_product_list):
    txt_file = open(filename, 'r', encoding='utf-8')
    products = txt_file.readlines()
    txt_file.close()
    for i in range(len(products)):
        str = re.sub('[^가-힣a-zA-Z\s0-9~.&/-]',' ',products[i])
        str = str.strip()
        products[i] = re.sub(' +', " ", str) #remove extra spaces
        
        split = products[i].split(' ')
        in_product_list.append(split)
    in_product_list.sort()
    
def load_product_csv(in_csv_file, in_product_list):
    rdfile_tag = open(os.path.join('',f"{in_csv_file}"), 'r', newline='', encoding='utf-8')
    csvrd_tag = csv.reader(rdfile_tag)
    tag_list = []
    cate_list = []
    for idx, cols in enumerate(csvrd_tag):
        if idx%3 == 0:
            in_product_list.append(cols)
        elif idx%3 == 1:
            tag_list.append(cols)
        else:
            cate_list.append(cols)
    return tag_list, cate_list

def save_tag_data():
    filename = fd.asksaveasfilename(initialdir="/", title="Select file",
                                          filetypes=(("CSV files", "*.csv"), 
                                          ("all files", "*.*")))
    if filename == '':
        return
    
    wrfile_tag = open(os.path.join('',f"{filename}"), 'w', newline='', encoding='utf-8')
    csvwr_tag = csv.writer(wrfile_tag)
    
    cnt = 0
    for product in g_product_list:
        lst_word = []
        lst_tag = []
        lst_cate = []
        for word in product:
            lst_word.append(g_label_list[cnt])
            lst_tag.append(g_entry_list[cnt].get())
            lst_cate.append(g_cate_list[cnt].get())
            cnt = cnt + 1
        csvwr_tag.writerow(lst_word)
        csvwr_tag.writerow(lst_tag)
        csvwr_tag.writerow(lst_cate)
        
        lst_word.clear()
        lst_tag.clear()
        lst_cate.clear()
    
    wrfile_tag.close()
    label1['text'] = "Save\nDone"

def load_txt_data():
    filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("TXT files", "*.txt"),
                                          ("all files", "*.*")))
    if filename == '':
        return
    
    if len(g_label_list) == 0:
        create_data_field(filename, TXT_MODE)
    else:
        update_data_field(filename, TXT_MODE)    
    
def load_tag_data():
    filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("CSV files", "*.csv"),
                                          ("all files", "*.*")))
    if filename == '':
        return
    
    if len(g_label_list) == 0:
        create_data_field(filename, CSV_MODE)
    else:
        update_data_field(filename, CSV_MODE)    

g_product_list = []
g_label_list = []
g_entry_list = []
g_cate_list = []

TXT_MODE = 1
CSV_MODE = 2
MAX_COLS_CNT = 14  
def create_data_field(in_filename, in_mode):
    if in_mode == TXT_MODE:
        load_product_txt(in_filename, g_product_list)
    else:
        tag_list, cate_list = load_product_csv(in_filename, g_product_list)
            
    for row, item in enumerate(g_product_list):        
        curr_col = 0
        for col, word in enumerate(item):
            box_width = 15
            label = tk.Label(canvasFrame, text=f"{word}", width=box_width)
            label.grid(column=col, row=row*3)
            g_label_list.append(f"{word}")
            curr_col = col

        if len(item) < MAX_COLS_CNT:
            empty_cnt = MAX_COLS_CNT - len(item)
            for i in range(empty_cnt):
                tk.Label(canvasFrame, text=f"---", width=15).grid(column=curr_col+i+1, row=row*3)
                
        for col, word in enumerate(item):
            box_width = 15
            entry = tk.Entry(canvasFrame, text=f"{word}", width=box_width)
            entry.delete(0, tk.END)
            if in_mode == CSV_MODE:
                entry.insert(tk.END, f"{tag_list[row][col]}")
            entry.grid(column=col, row=row*3+1)
            g_entry_list.append(entry)
            curr_col = col     
            
        if len(item) < MAX_COLS_CNT:
            empty_cnt = MAX_COLS_CNT - len(item)
            for i in range(empty_cnt):
                tk.Label(canvasFrame, text=f"---", width=15).grid(column=curr_col+i+1, row=row*3+1)  
                
        for col, word in enumerate(item):
            box_width = 15
            entry2 = tk.Entry(canvasFrame, width=box_width)
            entry2.delete(0, tk.END)
            if in_mode == CSV_MODE:
                entry2.insert(tk.END, f"{cate_list[row][col]}")
            entry2.grid(column=col, row=row*3+2)
            g_cate_list.append(entry2)
            curr_col = col   
            
        if len(item) < MAX_COLS_CNT:
            empty_cnt = MAX_COLS_CNT - len(item)
            for i in range(empty_cnt):
                tk.Label(canvasFrame, text=f"---", width=15).grid(column=curr_col+i+1, row=row*3+2)
                             
    if in_mode == CSV_MODE:    
        label1['text'] = "CSV Loading\nDone"
    else:
        label1['text'] = "Text Loading\nDone"
        
def update_data_field(in_filename, in_mode):
    remove_all()
    create_data_field(in_filename, in_mode)

import time    
def remove_all():
    label1['text'] = "Widgets\nare\nRemoved."
    if len(g_label_list) > 0:
        g_label_list.clear()
        g_entry_list.clear()
        g_cate_list.clear()
        g_product_list.clear() 
    
    widget_list = canvasFrame.grid_slaves()
    for item in widget_list:
        item.destroy()
    time.sleep(2)
    
        
def del_widgets():
    remove_all()

def show_null():
    null_cnt = 0
    if len(g_entry_list) > 0:
        for entry in g_entry_list:
            entry_txt = entry.get()
            if entry_txt == '':
                entry['bg'] = '#FFE4E1'
                null_cnt = null_cnt + 1
            elif entry_txt == 'x':
                entry['bg'] = '#E4E1FF'    
            else:
                entry['bg'] = '#FFFFFF'
    label1['text'] = f"Empty Cnt=\n{null_cnt}"

def insert_x():    
    if len(g_entry_list) > 0:
        for entry in g_entry_list:
            entry_txt = entry.get()
            if entry_txt == '':
                entry.insert(tk.END,'x')
                entry['bg'] = '#E4E1FF'
            elif entry_txt == 'x':
                entry['bg'] = '#E4E1FF'
            else:    
                entry['bg'] = '#FFFFFF'
    
def search_word():
    keyword = ent_keyword.get()
    matched_cnt = 0
    if keyword != '':
        if len(g_entry_list) > 0:
            for entry in g_entry_list:
                entry_txt = entry.get()
                if keyword in entry_txt:                    
                    entry['bg'] = '#FFE40D'
                    matched_cnt = matched_cnt + 1
                else:    
                    entry['bg'] = '#FFFFFF'
    label1['text'] = f"Matched CNT =\n{matched_cnt}"                

def insert_cate():
    keyword = ent_keyword.get()
    num = ent_cate.get()
    if keyword != '':
        if len(g_entry_list) > 0:
            for idx,entry in enumerate(g_entry_list):
                entry_txt = entry.get()
                if keyword == entry_txt:
                    g_cate_list[idx].delete(0, tk.END)  #내용 삭제
                    g_cate_list[idx].insert(tk.END, num)
                
def show_cate_null():
    null_cnt = 0
    if len(g_entry_list) > 0:
        for idx,entry in enumerate(g_entry_list):
            entry_txt = entry.get()
            if entry_txt != 'x' and entry_txt != '':
                if g_cate_list[idx].get() == '':
                    g_cate_list[idx]['bg'] = '#FFE4E1'
                    null_cnt = null_cnt + 1
                else:
                    g_cate_list[idx]['bg'] = '#FFFFFF' 
            else:
                g_cate_list[idx]['bg'] = '#FFFFFF'
                
    label1['text'] = f"빈분류 Cnt=\n{null_cnt}"                
    
def update_scrollregion(event):
    photoCanvas.configure(scrollregion=photoCanvas.bbox("all"))
    end_t = time.time()
    
def scroll(event):
    if event.delta==120:
        photoCanvas.yview_scroll(-1, 'page')
    if event.delta==-120:
        photoCanvas.yview_scroll(1, 'page')


dic_tag = dict()
dic_prodword = dict()
def make_tag_dict():
    filename = fd.asksaveasfilename(initialdir="/", title="상품명사전 파일 선택(=5분류ID.csv)",
                                          filetypes=(("CSV files", "*.csv"), 
                                          ("all files", "*.*")))
    if filename == '':
        return
    
    wrfile_prodword = open(os.path.join('',f"{filename}"), 'w', newline='', encoding='utf-8')
    csvwr_prodword = csv.writer(wrfile_prodword)
    
    cnt = 0
    for product in g_product_list:
        for word in product:
            word = g_label_list[cnt]
            tag = g_entry_list[cnt].get()
            cate = g_cate_list[cnt].get()
            if tag != 'x':  
                if word not in dic_prodword.keys():
                    dic_prodword[word] = [tag, cate]
                    
            cnt = cnt + 1
    word_tmp = ''
    tag_tmp = ''
    cate_tmp = ''
    word_flag = False
    for item in dic_prodword.keys():
        if '[' in dic_prodword[item][0]:
            word_flag = True
            word_tmp = word_tmp + f"${item}"
            tag_tmp = dic_prodword[item][0].replace('[','')
            cate_tmp = dic_prodword[item][1].replace('[','')
            continue
        elif ']' in dic_prodword[item][0]:
            word_tmp = word_tmp + f"${item}"  
            word_tmp = word_tmp.strip('$')    
            csvwr_prodword.writerow([word_tmp, tag_tmp, cate_tmp])
            word_flag = False
            
            if '&' in dic_prodword[item][0]:
                word_tmp = item
                tag_tmp = dic_prodword[item][0].split('&')[1]
                cate_tmp = dic_prodword[item][1].split('&')[1]
                csvwr_prodword.writerow([word_tmp, tag_tmp, cate_tmp])
            word_tmp = ''
            tag_tmp = ''
            cate_tmp = ''    
            continue
            
        if word_flag == True:
            word_tmp = word_tmp + f"${item}"
            continue
        else:
            csvwr_prodword.writerow([item, dic_prodword[item][0], dic_prodword[item][1]])
    wrfile_prodword.close()
    
    filename_dic = fd.asksaveasfilename(initialdir="/", title="대표어사전 파일선택(.csv)",
                                          filetypes=(("CSV files", "*.csv"), 
                                          ("all files", "*.*")))
    if filename_dic == '':
        return
    
    if os.path.isfile(filename_dic):
        rdfile_tag = open(os.path.join('',f"{filename_dic}"), 'r', newline='', encoding='utf-8')
        csvrd_tag = csv.reader(rdfile_tag)
    
        for item in csvrd_tag:
            dic_tag[item[0]] = item[1:]
        rdfile_tag.close()
    
    wrfile_tag = open(os.path.join('',f"{filename_dic}"), 'w', newline='', encoding='utf-8')
    csvwr_tag = csv.writer(wrfile_tag)
    
    rdfile_prodword = open(os.path.join('',f"{filename}"), 'r', newline='', encoding='utf-8')
    csvrd_prodword = csv.reader(rdfile_prodword)
    
    for cols in csvrd_prodword:
        if cols[1] not in dic_tag.keys():
            dic_tag[cols[1]] = [cols[0]]
        else:
            if cols[0] not in dic_tag[cols[1]]:
                dic_tag[cols[1]].append(cols[0])
    
    for item in dic_tag.keys():
        tmp_list = []
        tmp_list.append(item)
        for synonym in dic_tag[item]:
            tmp_list.append(synonym)
        csvwr_tag.writerow(tmp_list)
        tmp_list.clear()
            
    wrfile_tag.close()
    rdfile_prodword.close()
    
    label1['text'] = "Dict Save\nDone"
    
if __name__ == '__main__':
    start_t = time.time()
    math.factorial(100000)
    
    root = tk.Tk()    
    root.title("TaggingTool")
    root.resizable(True, True)

    photoFrame = tk.Frame(root, width=1720, height=960, bg="#EBEBEB")

    photoFrame.grid()
    photoFrame.rowconfigure(0, weight=1) 
    photoFrame.columnconfigure(0, weight=1) 

    photoCanvas = tk.Canvas(photoFrame, width=1720, height=960, bg="#EBEBEB")
    photoCanvas.grid(row=0, column=0, sticky="nsew")

    canvasFrame = tk.Frame(photoCanvas, bg="#EBEBEB")
    photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')
    photoCanvas.bind("<MouseWheel>", scroll)
    
    photoScroll = tk.Scrollbar(photoFrame, orient=tk.VERTICAL)
    photoScroll.config(command=photoCanvas.yview)
    photoCanvas.config(yscrollcommand=photoScroll.set)
    photoScroll.grid(row=0, column=1, sticky="ns")
    canvasFrame.bind("<Configure>", update_scrollregion)

    buttonFrame = tk.Frame(root, width=1720, height=960, bg="#EBEBEB")
    buttonFrame.grid(row=0, column=1, sticky="nsew")
    btn_save = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Save",
                command=save_tag_data) 
    btn_save.grid(row=2, column=0, sticky="nsew")
    btn_load = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Load Text",
                command=load_txt_data) 
    btn_load.grid(row=0, column=0, sticky="nsew")
    
    btn_load_tag = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Load CSV",
                command=load_tag_data) 
    btn_load_tag.grid(row=1, column=0, sticky="nsew")
    
    btn_show_null = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#FFE4E1", text="Show Null",
                command=show_null) 
    btn_show_null.grid(row=3, column=0, sticky="nsew")
    
    btn_fill_x = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4E1FF", text="Insert X",
                command=insert_x) 
    btn_fill_x.grid(row=4, column=0, sticky="nsew")
    
    btn_del = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Del Widgets",
                command=del_widgets) 
    btn_del.grid(row=5, column=0, sticky="nsew")
    
    label1 = tk.Label(buttonFrame, width=10, height=3, text="")
    label1.grid(row=6, column=0, sticky="nsew")

    ent_keyword = tk.Entry(buttonFrame, width=20) 
    ent_keyword.grid(row=7, column=0, sticky="nsew")
    btn_search = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Search",
                command=search_word) 
    btn_search.grid(row=8, column=0, sticky="nsew")
    
    ent_cate = tk.Entry(buttonFrame, width=5) 
    ent_cate.grid(row=9, column=0, sticky="nsew")
    btn_cate = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4FFE1", text="Insert No.",
                command=insert_cate) 
    btn_cate.grid(row=10, column=0, sticky="nsew")
    
    btn_show_null2 = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#FFE4E1", text="빈분류표시",
                command=show_cate_null) 
    btn_show_null2.grid(row=11, column=0, sticky="nsew")
    
    btn_make_dict = tk.Button(buttonFrame, width=10, height=2, 
                fg="black", bg="#E4E1FF", text="Dict생성",
                command=make_tag_dict) 
    btn_make_dict.grid(row=12, column=0, sticky="nsew")
    
    root.mainloop()
