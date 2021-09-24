

class Search_Question:
    def __init__(self):
        self.mode = 'search'
        self.text = ''
        self.token = []
        self.pos = []
        self.keyword = []
        self.tag = []
        self.neg_tag = []

    def save(self):
        tagged_question = [self.text]
        self.tag.sort()
        for tag in self.tag:
            tagged_question.append(tag)

        return tagged_question
        # return self.question, sorted(self.tag)

    def add_text(self, text):
        self.text = text

    def add_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.tag.append(tag)
        elif isinstance(tag_list, str):
            self.tag.append(tag_list)

        self.tag.sort()

    def del_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.tag.remove(tag)
        elif isinstance(tag_list, str):
            self.tag.remove(tag_list)

        self.tag.sort()

    def add_neg_tag(self,tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.neg_tag.append(tag)
        elif isinstance(tag_list, str):
            self.neg_tag.append(tag_list)

        self.neg_tag.sort()

    def del_neg_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.neg_tag.remove(tag)
        elif isinstance(tag_list, str):
            self.neg_tag.remove(tag_list)

        self.neg_tag.sort()

    def add_key(self, key_list):
        if isinstance(key_list, list):
            for key in key_list:
                self.keyword.append(key)
        elif isinstance(key_list, str):
            self.keyword.append(key_list)

        self.keyword.sort()
