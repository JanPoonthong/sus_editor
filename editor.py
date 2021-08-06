class Line:
    chars = []
    size = 0
    cursor = 0


class Editor:
    lines = Line()
    size = 0
    capacity = 0
    cursor_row = 0
    cursor_col = 0


def editor_insert_text_before(editor, text):
    if editor.cursor_row >= editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)

    line_insert_text_before(
        editor.lines.chars[editor.cursor_row], text, editor.cursor_col
    )


def editor_backspace(editor):
    if editor.cursor_row >= editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)
    line_backspace(editor.lines.char[editor.cursor_row], editor.cursor_col)


def editor_delete(editor):
    if editor.cursor_row >= editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)
    line_delete(editor.lines.char[editor.cursor_row], editor.cursor_col)


def editor_push_new_line(editor):
    pass


def line_insert_text_before(line, text, col):
    if col > line.size:
        col = line.size

    text_size = len(text)
    line.chars.insert(col, text)
    line.size += text_size
    col += text_size
    line.cursor = col


def line_backspace(line, col):
    if col > line.size:
        col = line.size

    if col > 0 and line.size > 0:
        col -= 1
        line.size -= 1
        del line.chars[col]
        line.cursor -= 1


def line_delete(line, col):
    if col > line.size:
        col = line.size

    if 0 <= col < line.size:
        line.size -= 1
        del line.chars[col]
