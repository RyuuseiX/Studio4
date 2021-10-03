import pythainlp as pyt
import pandas as pd

df_vector = pd.read_csv('./vector.csv')

text = 'แม่กินข้าวอยู่หน้าบ้าน'
pos_list = pyt.pos_tag(pyt.word_tokenize(text))
print(pos_list)

tag_list = []
for tok, pos in pos_list:
    if pos == 'NCMN':
        tag_list.append(tok)
        print(df_vector[df_vector['Word'] == tok].index)

print(tag_list)

print(list(df_vector.iloc[100, :]))

