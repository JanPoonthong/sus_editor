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


    src = SDL_Rect(
        x=int(col * FONT_CHAR_WIDTH),
        y=int(row * FONT_CHAR_HEIGHT),
        w=int(FONT_CHAR_WIDTH),
        h=int(FONT_CHAR_HEIGHT),
    )

    # Output display
    dst = SDL_Rect(
        x=int(x),
        y=int(y),
        w=int(FONT_CHAR_WIDTH * scale),
        h=int(FONT_CHAR_HEIGHT * scale),
    )

    SDL_SetTextureColorMod(
        font,
        # 2 left digits -> R
        color >> (8 * 2) & 0xFF,
        # 2 middle digits -> G
        color >> (8 * 1) & 0xFF,
        # 2 right digits -> B
        color >> (8 * 0) & 0xFF,
    )

    scc(SDL_RenderCopy(renderer, font, src, dst))


def renderer_text(renderer, font, text, x, y, color, scale):
    for i in range(len(text)):
        render_char(renderer, font, text[i], x, y, color, scale)
        x += FONT_CHAR_WIDTH * scale
    return True


def main():
    scc(SDL_Init(SDL_INIT_VIDEO))
    window = SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, SDL_WINDOW_RESIZABLE
    )
    renderer = scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED))

    font_surface = surface_from_file(b"charmap-oldschool_white.png")
    font_texture = scp(SDL_CreateTextureFromSurface(renderer, font_surface))

    text_render_completed = False
    while True:
        event = scp(SDL_Event())
        if SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                break
            else:
                if text_render_completed is not True:
                    text_render_completed = renderer_text(
                        renderer, font_texture, b"Jan Poonthong", 0, 0, 0x00FFFF, 5
                    )
                    SDL_RenderPresent(renderer)
    SDL_Quit()
    return 0


if __name__ == "__main__":
    main()
