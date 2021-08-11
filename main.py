import ctypes
import sys

import sdl2
import sdl2.sdlimage

import editor

FONT_WIDTH = 128
FONT_HEIGHT = 64
FONT_COLS = 18
FONT_ROWS = 7
FONT_CHAR_WIDTH = FONT_WIDTH / FONT_COLS
FONT_CHAR_HEIGHT = FONT_HEIGHT / FONT_ROWS
FONT_SCALE = 5

ASCII_DISPLAY_LOW = 32
ASCII_DISPLAY_HIGH = 127

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Font:
    sprite_sheet = sdl2.SDL_Texture()
    glyph_table = []


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def scc(code):
    if code < 0:
        print(f"SDL ERROR: {sdl2.SDL_GetError()}")
        sys.exit(1)


def scp(ptr):
    if ptr == 0:
        print(f"SDL ERROR: {sdl2.SDL_GetError()}")
        sys.exit(1)
    return ptr


def surface_from_file(file_path):
    """
    :param file_path: Accept file name as a string
    :return data.contents: As SDL_Surface object
    """
    data = sdl2.sdlimage.IMG_Load(file_path)

    if not data:
        print(f"IMG_Load ERROR: {sdl2.sdlimage.IMG_GetError()}")
        sys.exit(1)
    return data.contents


def font_load_from_file(renderer, file_path):
    """
    :return font, the ascii font will be loaded into Font Object(caching)
    """
    font = Font()

    font_surface = surface_from_file(file_path)
    scc(sdl2.SDL_SetColorKey(font_surface, sdl2.SDL_TRUE, 0xFF000000))
    font.sprite_sheet = scp(
        sdl2.SDL_CreateTextureFromSurface(renderer, font_surface)
    )

    sdl2.SDL_FreeSurface(font_surface)

    for asci in range(ASCII_DISPLAY_LOW, ASCII_DISPLAY_HIGH):
        index = asci - ASCII_DISPLAY_LOW
        col = int(index % FONT_COLS)
        row = int(index / FONT_COLS)

        font.glyph_table.append(
            sdl2.SDL_Rect(
                x=int(col * FONT_CHAR_WIDTH),
                y=int(row * FONT_CHAR_HEIGHT),
                w=int(FONT_CHAR_WIDTH),
                h=int(FONT_CHAR_HEIGHT),
            )
        )

    return font


def render_char(renderer, font, c: ord, position, scale):
    dst = sdl2.SDL_Rect(
        x=int(position.x),
        y=int(position.y),
        w=int(FONT_CHAR_WIDTH * scale),
        h=int(FONT_CHAR_HEIGHT * scale),
    )

    c = ord(c)
    assert c >= ASCII_DISPLAY_LOW
    assert c <= ASCII_DISPLAY_HIGH
    index = c - ASCII_DISPLAY_LOW

    scc(
        sdl2.SDL_RenderCopy(
            renderer, font.sprite_sheet, font.glyph_table[index], dst
        )
    )


def render_text_sized(row, renderer, font, editor_obj, pos, scale):
    text = editor_obj.lines[row].chars
    text_size = editor_obj.lines[row].size
    color = 0xFFFFFFFF

    set_texture_color(font.sprite_sheet, color)

    pos.x = 0
    for i in range(text_size):
        render_char(renderer, font, text[i], pos, scale)
        pos.x += FONT_CHAR_WIDTH * scale


def unhex(color):
    # 2 left digits -> R
    r = color >> (8 * 2) & 0xFF
    # 2 middle digits -> G
    g = color >> (8 * 1) & 0xFF
    # 2 right digits -> B
    b = color >> (8 * 0) & 0xFF
    # the last digits -> A
    a = color >> (8 * 3) & 0xFF
    return r, g, b, a


def set_texture_color(texture, color):
    r, g, b, a = unhex(color)
    sdl2.SDL_SetTextureColorMod(texture, r, g, b)
    scc(sdl2.SDL_SetTextureAlphaMod(texture, a))


def render_cursor(renderer, font, editor_obj):
    pos = Pos(
        editor_obj.cursor_col * FONT_CHAR_WIDTH * FONT_SCALE,
        editor_obj.cursor_row * FONT_CHAR_HEIGHT * FONT_SCALE,
    )
    cursor_rect = sdl2.SDL_Rect(
        x=int(pos.x),
        y=int(pos.y),
        w=int(FONT_CHAR_WIDTH * FONT_SCALE),
        h=int(FONT_CHAR_HEIGHT * FONT_SCALE),
    )

    unhex_unpack = unhex(0xFFFFFFFF)
    scc(sdl2.SDL_SetRenderDrawColor(renderer, *unhex_unpack))
    scc(sdl2.SDL_RenderFillRect(renderer, cursor_rect))

    set_texture_color(font.sprite_sheet, 0xFF000000)

    c = editor.editor_char_under_cursor(editor_obj)
    if c:
        render_char(
            renderer,
            font,
            c,
            pos,
            FONT_SCALE,
        )


def save_file(editor_obj):
    with open("output", "w") as file:
        for row in range(editor_obj.size):
            for col in range(editor_obj.lines[row].size):
                file.writelines(
                    editor_obj.lines[row].chars[col].decode("utf-8")
                )
            file.write("\n")
    print("Saved as output")


def left_arrow(editor_obj):
    if editor_obj.cursor_col > 0:
        editor_obj.cursor_col -= 1

def right_arrow(editor_obj):
    if editor_obj.cursor_col < editor_obj.lines[editor_obj.cursor_row].size:
        editor_obj.cursor_col += 1

def down_arrow(editor_obj):
    editor_obj.cursor_row += 1
    editor_obj.lines.append(editor.Line())
    editor_obj.size += 1

def up_arrow(editor_obj):
    if editor_obj.cursor_row > 0:
        editor_obj.cursor_row -= 1


def main_renderer(renderer, editor_obj, font):
    scc(sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
    scc(sdl2.SDL_RenderClear(renderer))

    if any(i.size != 0 for i in editor_obj.lines):
        for row in range(editor_obj.size):
            pos = Pos(0, row * FONT_CHAR_HEIGHT * FONT_SCALE)
            render_text_sized(
                row, renderer, font, editor_obj, pos, FONT_SCALE
            )

    render_cursor(renderer, font, editor_obj)

    sdl2.SDL_RenderPresent(renderer)


def main():
    scc(sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO))
    scc(sdl2.sdlimage.IMG_Init(sdl2.sdlimage.IMG_INIT_PNG))
    window = sdl2.SDL_CreateWindow(
        b"Sus Editor",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        sdl2.SDL_WINDOW_RESIZABLE,
    )
    renderer = scp(
        sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
    )

    font = font_load_from_file(renderer, b"charmap-oldschool_white.png")
    editor_obj = editor.Editor()

    running = True
    while running:
        event = scp(sdl2.SDL_Event())
        if sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False

            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_BACKSPACE:
                    editor.editor_backspace(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    editor.editor_push_new_line(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_DELETE:
                    editor.editor_delete(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_F1:
                    save_file(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    left_arrow(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    right_arrow(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_UP:
                    up_arrow(editor_obj)

                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    down_arrow(editor_obj)

            elif event.type == sdl2.SDL_TEXTINPUT:
                editor.editor_insert_text_before(editor_obj, event.text.text)

            main_renderer(renderer, editor_obj, font)

    sdl2.SDL_Quit()


main()
