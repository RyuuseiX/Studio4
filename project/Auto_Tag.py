import pythainlp as pyt
import pandas as pd

# print('loading dataset...')
# df_vector = pd.read_csv('./vector.csv')


def tokenize(question, engine='newmm'):
    if question.text.count('"') >= 2:
        new_word = question.text
        count = 0
        word = ''
        for t in question.text:
            if (t == '"') and (count == 0):
                count = 1
            elif (t == '"') and (count == 1):
                new_word = new_word.replace('"' + word + '"', ' ')
                if question.mode == 'ask':
                    question.add_auto_tag(word)
                elif question.mode == 'search':
                    question.add_tag(word)
                count = 0
                word = ''
            elif count == 1:
                word += t
        question.token = pyt.word_tokenize(new_word, engine=engine, keep_whitespace=False)
    else:
        question.token = pyt.word_tokenize(question.text, engine=engine, keep_whitespace=False)


def pos_tag(question, engine='perceptron', corpus='orchid'):
    question.pos = pyt.pos_tag(question.token, engine=engine, corpus=corpus)


def word_choose(question, pos_choose):
    if question.mode == 'A':
        question.auto_tag = []
    elif question.mode == 'S':
        question.tag = []
    for token, pos in question.pos:
        if (pos in pos_choose) or (pos == pos_choose):
            question.add_key(token)
            if question.mode == 'A':
                question.add_auto_tag(token)
            elif question.mode == 'S':
                question.add_tag(token)


def hierarchy_tag(question):
    pass


def auto_tag(question, tok_eng='newmm', tag_eng='perceptron', corpus='orchid', pos_choose=['NCMN']):
    if question.mode == 'S':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
    elif question.mode == 'A':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
        hierarchy_tag(question)




