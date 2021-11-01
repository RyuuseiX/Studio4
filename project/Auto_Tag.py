import pythainlp as pyt
import Word_Dict

# print('loading dataset...')
# df_vector = pd.read_csv('./vector.csv')


def tokenize(question, engine='newmm'):
    question.spec_tag = []
    if question.text.count('"') >= 2:
        new_word = question.text
        count = 0
        word = ''
        for t in question.text:
            if (t == '"') and (count == 0):
                count = 1
            elif (t == '"') and (count == 1):
                new_word = new_word.replace('"' + word + '"', ' ')
                if question.mode == 'A':
                    question.add_spec_tag(word)
                elif question.mode == 'S':
                    question.add_spec_tag(word)
                count = 0
                word = ''
            elif count == 1:
                word += t
        question.token = pyt.word_tokenize(new_word, engine=engine, keep_whitespace=False)
    else:
        question.token = pyt.word_tokenize(question.text, engine=engine, keep_whitespace=False)



def hierarchy_tag(question):
    question.auto_tag = []
    question.auto_tag = question.auto_tag.extend(question.spec_tag)

    if question.mode == 'A':
        new_tag = find_hierarchy(question.token, Word_Dict.word_category())
    elif question.mode == 'S':
        new_tag = find_word(question.token, Word_Dict.word_category())

    new_tag = remove_duplicate(new_tag)

    if new_tag is not None:
        question.add_auto_tag(new_tag)


def find_hierarchy(word_list, word_dict):
    tag_list = []

    # 1 token
    for word in word_list:
        found_new_tag = True
        running_word = word
        while found_new_tag:
            found_new_tag = False
            for key in word_dict:
                if running_word in word_dict[key]:
                    found_new_tag = True
                    tag_list.append(running_word)
                    if running_word == key:
                        found_new_tag = False
                    running_word = key
                    break

    # 2 tokens
    for i in range(len(word_list)-1):
        word = word_list[i]+word_list[i+1]
        found_new_tag = True
        running_word = word
        while found_new_tag:
            found_new_tag = False
            for key in word_dict:
                if running_word in word_dict[key]:
                    found_new_tag = True
                    tag_list.append(running_word)
                    if running_word == key:
                        found_new_tag = False
                    running_word = key
                    break

    # 3 tokens
    for i in range(len(word_list) - 2):
        word = word_list[i] + word_list[i + 1] + word_list[i+2]
        found_new_tag = True
        running_word = word
        while found_new_tag:
            found_new_tag = False
            for key in word_dict:
                if running_word in word_dict[key]:
                    found_new_tag = True
                    tag_list.append(running_word)
                    if running_word == key:
                        found_new_tag = False
                    running_word = key
                    break

    return tag_list


def find_word(word_list, word_dict):
    tag_list = []

    # 1 token
    for word in word_list:
        for key in word_dict:
            if word in word_dict[key]:
                tag_list.append(word)
                break

    # 2 tokens
    for i in range(len(word_list) - 1):
        word = word_list[i] + word_list[i + 1]
        for key in word_dict:
            if word in word_dict[key]:
                tag_list.append(word)
                break

    # 3 tokens
    for i in range(len(word_list) - 2):
        word = word_list[i] + word_list[i + 1] + word_list[i + 2]
        for key in word_dict:
            if word in word_dict[key]:
                tag_list.append(word)
                break



    return tag_list


def remove_duplicate(lis):
    if lis is None:
        return []
    elif lis is not None:
        ans_list = []
        for word in lis:
            if word not in ans_list:
                ans_list.append(word)
        return ans_list


def auto_tag(question, tok_eng='newmm'):
    tokenize(question, engine=tok_eng)
    hierarchy_tag(question)




