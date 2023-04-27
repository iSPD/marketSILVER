
import csv
import os

def loadCSV(in_rddir, in_wrdir, in_combine_file_name):
    rddir = in_rddir
    wrdir = in_wrdir
    combine_file_name = in_combine_file_name
    
    file_list = os.listdir(rddir)
    file_list_csv = [file for file in file_list if file.endswith(".csv")]
    print(file_list_csv)
    
    wrfile = open(os.path.join(wrdir,f"{combine_file_name}"), 'w', newline='', encoding='utf-8')
    writer_csv = csv.writer(wrfile)
            
    for csvfilename in file_list_csv:
        csvfile = open(os.path.join(rddir, csvfilename), 'r', encoding='utf-8')
        rdr = csv.reader(csvfile)
        for idx, row in enumerate(rdr):
            if idx > 0:
                writer_csv.writerow(row)
        csvfile.close()
    wrfile.close()
                    
  
