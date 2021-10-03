import pythainlp as pyt
import pandas as pd

df_vector = pd.read_csv('./vector.csv')


def tokenize(question, engine='newmm'):
    print('tokenizing...')
    question.token = pyt.word_tokenize(question.text, engine=engine, keep_whitespace=False)


def pos_tag(question, engine='perceptron', corpus='orchid'):
    print('pos_tagging...')
    question.pos = pyt.pos_tag(question.token, engine=engine, corpus=corpus)


def word_choose(question, pos_choose):
    print('choosing keyword...')
    for token, pos in question.pos:
        if (pos in pos_choose) or (pos == pos_choose):
            question.add_key(token)
            if question.mode == 'ask':
                question.add_auto_tag(token)
            elif question.mode == 'search':
                question.add_tag(token)


def vectorize(question, df):
    print('vectorizing...')
    for tag in question.auto_tag:
        if tag in list(df.iloc[:, 0]):
            print(tag)
            i = list(df[df['Word'] == tag].index)
            question.add_vector(list(df.iloc[i[0], :]))



def hierarchy_tag(question):
    print('hierarchy tagging...')
    pass


def auto_tag(question, tok_eng='newmm', tag_eng='perceptron', corpus='orchid', pos_choose=['NCMN']):
    if question.mode == 'search':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
    elif question.mode == 'ask':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
        # vectorize(question, df_vector)
        hierarchy_tag(question)




