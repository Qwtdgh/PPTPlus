class Page:
    def __init__(self, no):
        self.no = no
        self.content = list()

    def add(self, part):
        self.content.append(part)

    def getNo(self):
        return self.no

    def getContent(self):
        return self.content
