# Created by Elisa Lupin-Jimenez
# A program that, given 2 company names, outputs a list of keyterms that the companies share


# CONSTANTS: change these for the key term result list, and the 2 company names you want to compare
unfiltered_results = r'F:\Elisa\co_tech_results\150k_keyword_list_co_tech_results.txt'
company_1 = 'Oculus'
company_2 = 'HTC'


new_file_name = company_1 + "-" + company_2 + "_compare_terms.txt"
new_file = open(new_file_name, "w+", encoding="utf-8")

company_1_listed = company_1 + ':\n'
company_2_listed = company_2 + ':\n'

company_1_results = set()
company_2_results = set()

with open(unfiltered_results,'r',encoding='utf-8') as f:
    unfiltered_results_text = f.readlines()

company_selected = 0
for line in unfiltered_results_text:
    if company_1_listed == line:
        company_selected = 1
    elif company_2_listed == line:
        company_selected = 2
    elif line == '\n':
        company_selected = 0

    if line and company_selected == 1:
        company_1_results.add(line)
    elif line and company_selected == 2:
        company_2_results.add(line)

results = company_1_results.intersection(company_2_results)

for value in results:
    new_file.write("{}".format(value))

print("Done! Look for {} in the 'Classifier' directory".format(new_file_name))
