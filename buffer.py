class Line:
    chars = []
    size = 0
    cursor = 0


def line_insert_text_before(line, text):
    text_size = len(text)
    line.chars.insert(line.cursor, text)
    line.size += text_size
    line.cursor += text_size


def line_backspace(line):
    if line.cursor > 0 and line.size > 0:
        line.cursor -= 1
        line.size -= 1
        del line.chars[line.cursor]


def line_delete(line):
    if 0 <= line.cursor < line.size:
        line.size -= 1
        del line.chars[line.cursor]
