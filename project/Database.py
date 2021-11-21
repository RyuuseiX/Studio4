import pandas as pd
import openpyxl
import string
import random
import platform


class Excel_Database:
    def __init__(self):
        os = platform.platform()[0].upper()
        if os == 'W':
            self.excel_path = './Tag_Database.xlsx'
        elif os == 'M':
            self.excel_path = '/Users/Peace/Desktop/Studio4-main/project/Tag_Database.xlsx'

    def database_create(self):
        head = ['Question']
        for i in range(1, 21):
            head.append('Tag_'+str(i))
        df = pd.DataFrame(index=None, columns=head)
        df.to_excel(self.excel_path, sheet_name='Database', index=None)

    def database_update(self, question, tag_list):
        book = openpyxl.load_workbook(self.excel_path)
        writer = pd.ExcelWriter(self.excel_path, engine='openpyxl')
        writer.book = book
        data_list = [question]
        data_list.extend(tag_list)
        df = pd.DataFrame([data_list], index=None, columns=None)
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        for sheet_name in writer.sheets:
            df.to_excel(writer, sheet_name='Database', startrow=writer.sheets[sheet_name].max_row, index=False, header=False)
        writer.save()


    def database_query(self, positive_key_list, negative_key_list):
        df = pd.read_excel(self.excel_path, sheet_name='Database', keep_default_na=False, na_values=[""])
        # print(df)

        # Positive
        for i in range(len(df)):
            tag_exist = 0 
            for p in positive_key_list:
                if p in list(df.loc[i])[1:]:
                    tag_exist += 1
            if tag_exist != len(positive_key_list):
                df = df.drop(i)

        # Negative
        for n in negative_key_list:
            for c in list(df.columns)[1:]:
                df = df.drop(df[df[c] == n].index)
        
        # Search Results
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

        # if df.empty or len(positive_key_list) == 0:
        #     print("No Results Match")
        # else:
        #     # print(df)
        #     print(search_question_list, '\t', search_tag_list)
        if len(positive_key_list) == 0:
            return [],[],[]

        if df.empty:
            return ['No Results Match'], [], []
        else:
            # print(df)
            return search_question_list, search_tag_list, positive_key_list

    def test(self):
        data_list = []
        for i in range(random.randrange(2, 20)):
            data_list.append(random.choice(string.ascii_letters).lower())
        data_list = list(set(data_list))
        self.database_update(data_list[0], data_list[1:])
        # print("PASS !!!")
        self.database_query([], [])



if __name__ == '__main__':

    password = input("Type the Authentication Code: ")  # confirm

    if password == 'confirm' or password == 'C':
        '''Create (used ONCE when start a new file)'''
        db = Excel_Database()
        db.database_create()
        print('-- Database Created Succesfully !! --')
    else:
        print('-- Wrong Authentication Code !! --')
