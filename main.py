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

ACSII_DISPLAY_LOW = 32
ACSII_DISPLAY_HIGH = 127

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ALL_KEYS_INPUT = string.ascii_letters + string.punctuation + string.digits


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


class Font:
    def __init__(self):
        self.spritesheet = SDL_Texture()
        self.glyph_table = [0] * (ACSII_DISPLAY_HIGH - ACSII_DISPLAY_LOW)


def font_load_from_file(renderer, file_path):
    font = Font()

    font_surface = surface_from_file(file_path)
    font.spritesheet = scp(SDL_CreateTextureFromSurface(renderer, font_surface))

    SDL_FreeSurface(font_surface)

    for asci in range(ACSII_DISPLAY_LOW, ACSII_DISPLAY_HIGH):
        index = asci - ACSII_DISPLAY_LOW
        col = int(index % FONT_COLS)
        row = int(index / FONT_COLS)

        font.glyph_table[index] = SDL_Rect(
            x=int(col * FONT_CHAR_WIDTH),
            y=int(row * FONT_CHAR_HEIGHT),
            w=int(FONT_CHAR_WIDTH),
            h=int(FONT_CHAR_HEIGHT),
        )

    return font


def render_char(renderer, font, c, x, y, scale):
    dst = SDL_Rect(
        x=int(x),
        y=int(y),
        w=int(FONT_CHAR_WIDTH * scale),
        h=int(FONT_CHAR_HEIGHT * scale),
    )

    assert c >= ACSII_DISPLAY_LOW
    assert c <= ACSII_DISPLAY_HIGH
    index = c - ACSII_DISPLAY_LOW

    scc(
        SDL_RenderCopy(renderer, font.spritesheet, font.glyph_table[index], dst)
    )


def render_text_sized(renderer, font, text, text_size, x, y, color, scale):
    r, g, b, a = unhex(color)

    SDL_SetTextureColorMod(font.spritesheet, r, g, b)

    scc(SDL_SetTextureAlphaMod(font.spritesheet, a))

    for i in range(text_size):
        render_char(renderer, font, ord(text[i]), x, y, scale)
        x += FONT_CHAR_WIDTH * scale
    return 0


def renderer_text(renderer, font, text, x, y, color, scale):
    render_text_sized(renderer, font, text, len(text), x, y, color, scale)


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


def render_cursor(renderer, buffer_cursor, color):
    cursor_rect = SDL_Rect(
        x=int(buffer_cursor * FONT_CHAR_WIDTH * FONT_SCALE),
        y=0,
        w=int(FONT_CHAR_WIDTH * FONT_SCALE),
        h=int(FONT_CHAR_HEIGHT * FONT_SCALE),
    )

    unhex_unpack = unhex(color)
    scc(SDL_SetRenderDrawColor(renderer, *unhex_unpack))
    scc(SDL_RenderFillRect(renderer, cursor_rect))


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
    buffer_capacity = 1024
    buffer = []
    buffer_size = 0
    buffer_cursor = 0

    while True:
        event = scp(SDL_Event())
        if SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                break

            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_BACKSPACE:
                    if buffer_size > 0:
                        buffer.pop()
                        buffer_size -= 1
                        buffer_cursor = buffer_size

                if event.key.keysym.sym == SDLK_LEFT:
                    if buffer_cursor > 0:
                        buffer_cursor -= 1

                if event.key.keysym.sym == SDLK_RIGHT:
                    if buffer_cursor < buffer_size:
                        buffer_cursor += 1

            if event.type == SDL_TEXTINPUT:
                text_size = len(event.text.text)
                free_space = buffer_capacity - buffer_size
                if text_size > free_space:
                    text_size = free_space
                buffer.append(event.text.text)
                buffer_size += text_size
                buffer_cursor = buffer_size

            scc(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
            scc(SDL_RenderClear(renderer))

            if buffer_size != 0:
                render_text_sized(
                    renderer,
                    font,
                    buffer,
                    buffer_size,
                    0,
                    0,
                    0x00FFFF,
                    FONT_SCALE,
                )

            render_cursor(renderer, buffer_cursor, 0xFFFFFF)

            SDL_RenderPresent(renderer)

    SDL_Quit()
    return 0


main()
