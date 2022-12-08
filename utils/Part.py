class Part:

    def __init__(self):
        self.content = []

    def add(self, text):
        self.content.append(text)

    def getContent(self):
        return self.content
