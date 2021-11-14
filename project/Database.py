import pandas as pd
import openpyxl

import string
import random

def database_create(path):
    head = ['Question']
    for i in range(1,21):
        head.append('Tag_'+str(i))
    df = pd.DataFrame(index=None, columns=head)
    df.to_excel(path, sheet_name='Database', index=None)

def database_update(path, dataList):
    book = openpyxl.load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book
    df = pd.DataFrame([dataList],index=None, columns=None)
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    for sheetname in writer.sheets:
        df.to_excel(writer, sheet_name='Database', startrow=writer.sheets[sheetname].max_row, index=False, header=False)
    writer.save()

def database_query(path, positive_key_list, negative_key_list):
    df = pd.read_excel(path, sheet_name='Database', keep_default_na= False, na_values=[""])
    print(df)

    #Positive
    for i in range(len(df)):
        tag_exist = 0 
        for p in positive_key_list:
            if p in list(df.loc[i])[1:]:
                tag_exist += 1
        if tag_exist != len(positive_key_list):
            df = df.drop(i)

    #Negative 
    for n in negative_key_list:
        for c in list(df.columns)[1:]:
            df = df.drop(df[df[c] == n].index)
    
    #Search Results
    df = df.reset_index(drop=True)
    search_question_list = []
    search_tag_list = []
    for i in df.index:
        search_list = list(df.loc[i])
        search_question_list.append(search_list[0])
        search_tag_list.append([])
        for tag in search_list[1:]:
            if not pd.isna(tag):
                search_tag_list[i].append(tag)

    if df.empty:
        print("No Results Match")
    else:
        print(df)
        print(search_question_list, '\t', search_tag_list)





excel_path = '/Users/Peace/Desktop/Tag_Database.xlsx'

'''Create (used ONCE when start a new file)'''
# database_create(excel_path)

'''Update'''
data_list = []
for i in range(random.randrange(2, 20)):
    data_list.append(random.choice(string.ascii_letters).lower())
data_list = list(set(data_list))
# database_update(excel_path, data_list)

'''Query'''
database_query(excel_path,['b'],['d'])