import csv
import string
import os

excel_file = r"F:\Elisa\text_files\vr-patent-reports\CSV1907171053.csv"
result_dir = r'F:\Elisa\text_files\vr-patent-reports\patent_report_split'
included_cols = [1,2,12,30]

with open(excel_file,'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    index = 0
    for row in reader:
        new_file_name = "csv_{}.txt".format(index)
        index += 1
        new_file = open(os.path.join(result_dir,new_file_name), "w+", encoding="utf-8")
        content = list(row[i] for i in included_cols)
        row_string = str(' '.join(content))
        new_file.write(row_string)
