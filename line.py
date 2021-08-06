LINE_INIT_CAPACITY = 1024


class Line:
    def __init__(self):
        self.chars = []
        self.capacity = 0
        self.size = 0


def line_expand(line, n: int):
    new_capacity = line.capacity

    assert new_capacity >= line.size
    free_space = new_capacity - line.size

    while free_space < n:
        if new_capacity == 0:
            new_capacity = LINE_INIT_CAPACITY
        else:
            new_capacity *= 2

    if new_capacity != line.capacity:
        line.chars.append(new_capacity)


def line_insert_text_before(line, text, col):
    text_size = len(text)
    # line_expand(line, text_size)
    line.chars.insert(col, text)
    line.size += text_size


def line_backspace(line, col):
    line.size -= 1
    del line.chars[col]


def line_delete(line, col):
    line.size -= 1
    del line.chars[col]
