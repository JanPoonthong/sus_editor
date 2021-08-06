class Line:
    def __init__(self):
        self.chars = []
        self.size = 0


def line_insert_text_before(line, text, col):
    text_size = len(text)
    line.chars.insert(col, text)
    line.size += text_size


def line_backspace(line, col):
    line.size -= 1
    del line.chars[col]


def line_delete(line, col):
    line.size -= 1
    del line.chars[col]
