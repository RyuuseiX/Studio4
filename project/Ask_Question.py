

class Ask_Question:
    def __init__(self):
        self.mode = 'A'
        self.text = ''
        self.token = []
        self.pos = []
        self.keyword = []
        self.auto_tag = []
        self.manual_tag = []
        self.tagged_question = {}

    def save(self):
        self.tagged_question = {'Question': self.text, 'Tag': []}
        self.tagged_question['Tag'].extend(self.auto_tag)
        self.tagged_question['Tag'].extend(self.manual_tag)

        return self.tagged_question

    def add_text(self, text):
        self.text = text

    def add_auto_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.auto_tag.append(tag)
        elif isinstance(tag_list, str):
            self.auto_tag.append(tag_list)

        self.auto_tag = set(self.auto_tag)
        self.auto_tag = list(self.auto_tag)
        # self.auto_tag.sort()

    def del_auto_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.auto_tag.remove(tag)
        elif isinstance(tag_list, str):
            self.auto_tag.remove(tag_list)

        # self.auto_tag.sort()

    def add_manual_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.manual_tag.append(tag)
        elif isinstance(tag_list, str):
            self.manual_tag.append(tag_list)
        self.manual_tag = set(self.manual_tag)
        self.manual_tag = list(self.manual_tag)
        # self.manual_tag.sort()

    def del_manual_tag(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                self.manual_tag.remove(tag)
        elif isinstance(tag_list, str):
            self.manual_tag.remove(tag_list)

        # self.manual_tag.sort()

    def add_key(self, key_list):
        if isinstance(key_list, list):
            for key in key_list:
                self.keyword.append(key)
        elif isinstance(key_list, str):
            self.keyword.append(key_list)

        # self.keyword.sort()

    def add_vector(self, vec_list):
        if isinstance(vec_list, list):
            for key in vec_list:
                self.vector.append(key)
        elif isinstance(vec_list, str):
            self.vector.append(vec_list)

