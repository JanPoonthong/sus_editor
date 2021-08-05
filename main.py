import ctypes
import string
import sys

import sdl2.sdlimage
from sdl2 import *

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
ALL_KEYS_INPUT = string.ascii_letters + string.punctuation + string.digits

BUFFER_CAPACITY = 1024
buffer = []


def scc(code):
    if code < 0:
        print(f"SDL ERROR: {SDL_GetError()}")
        sys.exit(1)


def scp(ptr):
    if ptr == 0:
        print(f"SDL ERROR: {SDL_GetError()}")
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
    scc(SDL_SetColorKey(font_surface, SDL_TRUE, 0xFF000000))
    font.sprite_sheet = scp(
        SDL_CreateTextureFromSurface(renderer, font_surface)
    )

    SDL_FreeSurface(font_surface)

    for asci in range(ASCII_DISPLAY_LOW, ASCII_DISPLAY_HIGH):
        index = asci - ASCII_DISPLAY_LOW
        col = int(index % FONT_COLS)
        row = int(index / FONT_COLS)

        font.glyph_table.append(
            SDL_Rect(
                x=int(col * FONT_CHAR_WIDTH),
                y=int(row * FONT_CHAR_HEIGHT),
                w=int(FONT_CHAR_WIDTH),
                h=int(FONT_CHAR_HEIGHT),
            )
        )

    return font


class Font:
    def __init__(self):
        self.sprite_sheet = SDL_Texture()
        self.glyph_table = []


def render_char(renderer, font, c, pos, scale):
    dst = SDL_Rect(
        x=int(pos.x),
        y=int(pos.y),
        w=int(FONT_CHAR_WIDTH * scale),
        h=int(FONT_CHAR_HEIGHT * scale),
    )

    c = ord(c)
    assert c >= ASCII_DISPLAY_LOW
    assert c <= ASCII_DISPLAY_HIGH
    index = c - ASCII_DISPLAY_LOW

    scc(
        SDL_RenderCopy(
            renderer, font.sprite_sheet, font.glyph_table[index], dst
        )
    )


def render_text_sized(renderer, font, text, text_size, pos, color, scale):
    set_texture_color(font.sprite_sheet, color)

    pos.x = 0
    for i in range(text_size):
        render_char(renderer, font, text[i], pos, scale)
        pos.x += FONT_CHAR_WIDTH * scale


# def renderer_text(renderer, font, text, pos, color, scale):
#     render_text_sized(renderer, font, text, len(text), pos, color, scale)


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


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def set_texture_color(texture, color):
    r, g, b, a = unhex(color)
    SDL_SetTextureColorMod(texture, r, g, b)
    scc(SDL_SetTextureAlphaMod(texture, a))


def render_cursor(renderer, font, buffer, buffer_size, buffer_cursor):
    pos = Pos(buffer_cursor * FONT_CHAR_WIDTH * FONT_SCALE, 0)
    cursor_rect = SDL_Rect(
        x=int(pos.x),
        y=int(pos.y),
        w=int(FONT_CHAR_WIDTH * FONT_SCALE),
        h=int(FONT_CHAR_HEIGHT * FONT_SCALE),
    )

    unhex_unpack = unhex(0xFFFFFFFF)
    scc(SDL_SetRenderDrawColor(renderer, *unhex_unpack))
    scc(SDL_RenderFillRect(renderer, cursor_rect))

    set_texture_color(font.sprite_sheet, 0xFF000000)

    if buffer_cursor < buffer_size:
        render_char(renderer, font, buffer[buffer_cursor], pos, FONT_SCALE)


def buffer_insert_text_before_cursor(text, buffer_size, buffer_cursor):
    text_size = len(text)
    free_space = BUFFER_CAPACITY - buffer_size
    if text_size > free_space:
        text_size = free_space
    buffer.insert(buffer_cursor, text)
    buffer_size += text_size
    buffer_cursor += text_size
    return buffer_size, buffer_cursor


def del_buffer_text_before_cursor(buffer_size, buffer_cursor):
    if buffer_cursor > 0 and buffer_size > 0:
        buffer_size -= 1
        buffer_cursor -= 1
        del buffer[buffer_cursor]
    return buffer_size, buffer_cursor


def buffer_delete(buffer_size, buffer_cursor):
    if buffer_cursor >= 0 and buffer_cursor < buffer_size:
        buffer_size -= 1
        del buffer[buffer_cursor]
    return buffer_size, buffer_cursor


def main():
    scc(SDL_Init(SDL_INIT_VIDEO))
    scc(sdl2.sdlimage.IMG_Init(sdl2.sdlimage.IMG_INIT_PNG))
    window = SDL_CreateWindow(
        b"Sus Editor",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SDL_WINDOW_RESIZABLE,
    )
    renderer = scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED))

    font = font_load_from_file(renderer, b"charmap-oldschool_white.png")

    buffer_size = 0
    buffer_cursor = 0
    pos = Pos(0, 0)

    while True:
        event = scp(SDL_Event())
        if SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                break

            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_BACKSPACE:
                    buffer_size, buffer_cursor = del_buffer_text_before_cursor(
                        buffer_size, buffer_cursor
                    )

                elif event.key.keysym.sym == SDLK_DELETE:
                    buffer_size, buffer_cursor = buffer_delete(
                        buffer_size, buffer_cursor
                    )

                elif event.key.keysym.sym == SDLK_LEFT:
                    if buffer_cursor > 0:
                        buffer_cursor -= 1

                elif event.key.keysym.sym == SDLK_RIGHT:
                    if buffer_cursor < buffer_size:
                        buffer_cursor += 1

            elif event.type == SDL_TEXTINPUT:
                buffer_size, buffer_cursor = buffer_insert_text_before_cursor(
                    event.text.text, buffer_size, buffer_cursor
                )

            scc(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
            scc(SDL_RenderClear(renderer))

            if buffer_size != 0:
                render_text_sized(
                    renderer,
                    font,
                    buffer,
                    buffer_size,
                    pos,
                    0xFFFFFFFF,
                    FONT_SCALE,
                )

            render_cursor(renderer, font, buffer, buffer_size, buffer_cursor)

            SDL_RenderPresent(renderer)

    SDL_Quit()


main()
