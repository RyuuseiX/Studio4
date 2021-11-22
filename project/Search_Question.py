

class Search_Question:
    def __init__(self):
        self.mode = 'S'
        self.text = ''
        self.token = []
        self.auto_tag = []
        self.spec_tag = []
        self.disable_tag = []
        self.pos_tag = []
        self.neg_tag = []
        self.tagged_question = {}

    def save(self):
        self.tagged_question = {'Question': self.text, 'Tag': [], 'Neg_Tag': self.neg_tag}
        self.tagged_question['Tag'].extend(self.auto_tag)
        self.tagged_question['Tag'].extend(self.pos_tag)

        for tag in self.disable_tag:
            if tag in self.tagged_question['Tag']:
                self.tagged_question['Tag'].remove(tag)

        return self.tagged_question

    def add_text(self, text):
        self.text = text

    def add_auto_tag(self, tag_list):
        if self.auto_tag is None:
            self.auto_tag = []
            self.auto_tag.extend(self.spec_tag)
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.auto_tag.append(tag)
        elif isinstance(tag_list, str):
            self.auto_tag.append(tag_list)

        self.auto_tag = remove_duplicate(self.auto_tag)

    def del_auto_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.auto_tag.remove(tag)
        elif isinstance(tag_list, str):
            if tag_list == '!CLEAR_ALL!':
                self.auto_tag = []
            else:
                self.auto_tag.remove(tag_list)


    def add_spec_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.spec_tag.append(tag)
        elif isinstance(tag_list, str):
            self.spec_tag.append(tag_list)

        self.spec_tag = remove_duplicate(self.spec_tag)

    def del_spec_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.spec_tag.remove(tag)
        elif isinstance(tag_list, str):
            if tag_list == '!CLEAR_ALL!':
                self.spec_tag = []
            else:
                self.spec_tag.remove(tag_list)


    def add_pos_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.pos_tag.append(tag)
        elif isinstance(tag_list, str):
            self.pos_tag.append(tag_list)

        self.pos_tag = remove_duplicate(self.pos_tag)

    def del_pos_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.pos_tag.remove(tag)
        elif isinstance(tag_list, str):
            if tag_list == '!CLEAR_ALL!':
                self.pos_tag = []
            else:
                self.pos_tag.remove(tag_list)

    def add_neg_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.neg_tag.append(tag)
        elif isinstance(tag_list, str):
            self.neg_tag.append(tag_list)

        self.neg_tag = remove_duplicate(self.neg_tag)

    def del_neg_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.neg_tag.remove(tag)
        elif isinstance(tag_list, str):
            if tag_list == '!CLEAR_ALL!':
                self.neg_tag = []
            else:
                self.neg_tag.remove(tag_list)


def remove_duplicate(lis):
    if lis is None:
        return []
    elif lis is not None:
        ans_list = []
        for word in lis:
            if word not in ans_list:
                ans_list.append(word)
        return ans_list
