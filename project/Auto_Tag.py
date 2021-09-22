import pythainlp as pyt


def tokenize(question, engine='newmm'):
    question.token = pyt.word_tokenize(question.text, engine=engine, keep_whitespace=False)


def pos_tag(question, engine='perceptron', corpus='orchid'):
    question.pos = pyt.pos_tag(question.token, engine=engine, corpus=corpus)


def word_choose(question, pos_choose):
    for token, pos in question.pos:
        if (pos in pos_choose) or (pos == pos_choose):
            question.add_key(token)
            question.add_tag(token)


def vectorize(question):
    pass


def hierarchy_tag(question):
    pass


def auto_tag(question, mode, tok_eng='newmm', tag_eng='perceptron', corpus='orchid', pos_choose=['NCMN']):
    if mode == 's':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
    elif mode == 'a':
        tokenize(question, engine=tok_eng)
        pos_tag(question, engine=tag_eng, corpus=corpus)
        word_choose(question, pos_choose=pos_choose)
        vectorize(question)
        hierarchy_tag(question)




