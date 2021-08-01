import ctypes
import sys

from sdl2 import *
from sdl2.sdlimage import *

FONT_WIDTH = 128
FONT_HEIGHT = 64
FONT_COLS = 18
FONT_ROWS = 7
FONT_CHAR_WIDTH = FONT_WIDTH / FONT_COLS
FONT_CHAR_HEIGHT = FONT_HEIGHT / FONT_ROWS

ACSII_DISPLAY_LOW = 32
# TODO(jan): Maybe 126
ACSII_DISPLAY_HIGH = 127

SCREEN_POS_X, SCREEN_POS_Y = 1920 // 2, 1080 // 2


class SDL_Rect_Ascii(Structure):
    _fields_ = [("x", c_int), ("y", c_int), ("w", c_int), ("h", c_int)]

    def __init__(self, x=0, y=0, w=0, h=0):
        super(SDL_Rect_Ascii, self).__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h


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
    IMG_Init(IMG_INIT_PNG)
    data = IMG_Load(file_path)

    if not data:
        print(f"IMG_Load ERROR: {IMG_GetError()}")
        sys.exit(1)
    return data.contents


def font_object():
    """
    Create black SDL_Texture and 95 of free list space
    :return dict
    """
    font = {
        "spritesheet": SDL_Texture(),
        "glyph_table": [0] * (ACSII_DISPLAY_HIGH - ACSII_DISPLAY_LOW),
    }
    return font


def font_load_from_file(renderer, file_path):
    font = font_object()

    font_surface = surface_from_file(file_path)
    font["spritesheet"] = scp(
        SDL_CreateTextureFromSurface(renderer, font_surface)
    )

    SDL_FreeSurface(font_surface)

    for asci in range(ACSII_DISPLAY_LOW, ACSII_DISPLAY_HIGH):
        # print(f"ASCII: {asci}, {ACSII_DISPLAY_HIGH - ACSII_DISPLAY_LOW}")
        index = asci - ACSII_DISPLAY_LOW
        # print(f"Index: {chr(index)} -> {index} - 32 = {index - 32}")
        # Get each letters in which col -> know col
        col = int(index % FONT_COLS)
        # print(f"Index: {index} % {FONT_COLS} = Col {col}")
        # Get each letters in which row -> know row
        row = int(index / FONT_COLS)
        # print(f"Index: {index} / {FONT_COLS} = Row {row}")
        font["glyph_table"][index] = SDL_Rect(
            x=int(col * FONT_CHAR_WIDTH),
            y=int(row * FONT_CHAR_HEIGHT),
            w=int(FONT_CHAR_WIDTH),
            h=int(FONT_CHAR_HEIGHT),
        )
        # print(chr(asci), font["glyph_table"][index])

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
    # print(index, c, chr(c), font["glyph_table"][index])

    scc(
        SDL_RenderCopy(
            renderer, font["spritesheet"], font["glyph_table"][index], dst
        )
    )


def renderer_text(renderer, font, text, x, y, color, scale):
    SDL_SetTextureColorMod(
        font["spritesheet"],
        # 2 left digits -> R
        color >> (8 * 2) & 0xFF,
        # 2 middle digits -> G
        color >> (8 * 1) & 0xFF,
        # 2 right digits -> B
        color >> (8 * 0) & 0xFF,
    )

    scc(SDL_SetTextureAlphaMod(font["spritesheet"], color >> (8 * 3) & 0xFF))

    for i in range(len(text)):
        render_char(renderer, font, text[i], x, y, scale)
        x += FONT_CHAR_WIDTH * scale
    return True


def main():
    scc(SDL_Init(SDL_INIT_VIDEO))
    window = SDL_CreateWindow(
        b"Sus Editor",
        SCREEN_POS_X,
        SCREEN_POS_Y,
        800,
        600,
        SDL_WINDOW_RESIZABLE,
    )
    renderer = scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED))

    font = font_load_from_file(renderer, b"charmap-oldschool_white.png")

    text_render_completed = False
    while True:
        event = scp(SDL_Event())
        if SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                break
            else:
                scc(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
                scc(SDL_RenderClear(renderer))
                # if text_render_completed is not True:
                text_render_completed = renderer_text(
                    renderer, font, b"Jan Poonthong", 0, 0, 0x00FFFF, 5
                )
                SDL_RenderPresent(renderer)
    SDL_Quit()
    return 0


if __name__ == "__main__":
    main()
