class Line:
    chars = []
    size = 0


class Editor:
    lines = Line()
    size = 0
    cursor_row = 0
    cursor_col = 0


def editor_char_under_cursor(editor):
    if editor.cursor_row < editor.size:
        if editor.cursor_col < editor.lines.size:
            return editor.lines.chars[editor.cursor_col]
    return None


def editor_insert_text_before(editor, text):
    if editor.cursor_row > editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)

    line_insert_text_before(editor, text)


def editor_backspace(editor):
    if editor.cursor_row > editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)

    line_backspace(editor)


def editor_delete(editor):
    if editor.cursor_row > editor.size:
        if editor.size > 0:
            editor.cursor_row = editor.size - 1
        else:
            editor_push_new_line(editor)

    line_delete(editor)


def editor_push_new_line(editor):
    editor.size += 1
    editor.cursor_row += 1


def line_insert_text_before(editor, text):
    if editor.cursor_col > editor.lines.size:
        editor.cursor_col = editor.lines.size

    text_size = len(text)
    editor.lines.chars.insert(editor.cursor_col, text)
    editor.lines.size += text_size
    editor.cursor_col += text_size


def line_backspace(editor):
    if editor.cursor_col > editor.lines.size:
        editor.cursor_col = editor.lines.size

    if editor.cursor_col > 0 and editor.lines.size > 0:
        editor.cursor_col -= 1
        editor.lines.size -= 1
        del editor.lines.chars[editor.cursor_col]


def line_delete(editor):
    if editor.cursor_col > editor.lines.size:
        editor.cursor_col = editor.lines.size

    if 0 <= editor.cursor_col < editor.lines.size:
        editor.lines.size -= 1
        del editor.lines.chars[editor.cursor_col]
