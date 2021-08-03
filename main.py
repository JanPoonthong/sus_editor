import ctypes
import string
import sys
import subprocess

from sdl2 import *
import sdl2.sdlimage

from sdl_rect_ascii import SdlRectAscii

if sys.platform == "win32":
    win32 = ctypes.windll.user32
    SCREEN_RESOLUTION_WIDTH = win32.GetSystemMetrics(0)
    SCREEN_RESOLUTION_HEIGHT = win32.GetSystemMetrics(1)
else:
    output = (
        subprocess.Popen(
            'xrandr | grep "\*" | cut -d" " -f4',
            shell=True,
            stdout=subprocess.PIPE,
        )
        .communicate()[0]
        .decode("utf-8")
    )
    SCREEN_RESOLUTION_WIDTH = int(output[:4])
    SCREEN_RESOLUTION_HEIGHT = int(output[5:])

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
SCREEN_POS_X, SCREEN_POS_Y = (SCREEN_RESOLUTION_WIDTH - SCREEN_WIDTH) // 2, (
    SCREEN_RESOLUTION_HEIGHT - SCREEN_HEIGHT
) // 2
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
    """
    :return dict
    """
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

        font["glyph_table"][index] = SdlRectAscii(
            x=int(col * FONT_CHAR_WIDTH),
            y=int(row * FONT_CHAR_HEIGHT),
            w=int(FONT_CHAR_WIDTH),
            h=int(FONT_CHAR_HEIGHT),
            asci=asci,
        )
        # print(
        #     asci,
        #     type(font["glyph_table"][index]),
        #     font["glyph_table"][index],
        # )

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
            renderer,
            font["spritesheet"],
            font["glyph_table"][index].get_lp_sdl_rect,
            dst,
        )
    )


def render_text_sized(renderer, font, text, text_size, x, y, color, scale):
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

    for i in range(text_size):
        render_char(renderer, font, ord(text[i]), x, y, scale)
        x += FONT_CHAR_WIDTH * scale
    return 0


def renderer_text(renderer, font, text, x, y, color, scale):
    render_text_sized(renderer, font, text, len(text), x, y, color, scale)


def handle_keys_decode(
    event, buffer, buffer_size, buffer_cursor, character_allow
):
    try:
        character = event.text.text.decode("utf-8")
    except UnicodeDecodeError:
        # TODO(jan): Eating the error may effect other place
        character = ""

    free_space = character_allow - buffer_size
    if character == "":
        pass
    elif character in ALL_KEYS_INPUT and free_space > 0:
        buffer.append(character)
        buffer_size += 1
        buffer_cursor = buffer_size

    return buffer, buffer_size, buffer_cursor


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
    rect = SDL_Rect(
        x=int(buffer_cursor * FONT_CHAR_WIDTH * FONT_SCALE),
        y=0,
        w=int(FONT_CHAR_WIDTH * FONT_SCALE),
        h=int(FONT_CHAR_HEIGHT * FONT_SCALE),
    )

    unhex_unpack = unhex(color)
    scc(SDL_SetRenderDrawColor(renderer, (*unhex_unpack)))
    scc(SDL_RenderFillRect(renderer, rect))


def main():
    scc(SDL_Init(SDL_INIT_VIDEO))
    scc(sdl2.sdlimage.IMG_Init(sdl2.sdlimage.IMG_INIT_PNG))
    window = SDL_CreateWindow(
        b"Sus Editor",
        SCREEN_POS_X,
        SCREEN_POS_Y,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SDL_WINDOW_RESIZABLE,
    )
    renderer = scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED))

    font = font_load_from_file(renderer, b"charmap-oldschool_white.png")

    character_allow = 1024
    buffer = []
    buffer_size = 0
    buffer_cursor = 0
    backspace_checker = 0

    while True:
        event = scp(SDL_Event())
        if SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                break

            if SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_BACKSPACE:
                    if backspace_checker % 2 == 0:
                        if buffer_size > 0:
                            buffer.pop()
                            buffer_size -= 1
                            buffer_cursor = buffer_size
                    backspace_checker += 1

            if SDL_TEXTINPUT:
                scc(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
                scc(SDL_RenderClear(renderer))

                buffer, buffer_size, buffer_cursor = handle_keys_decode(
                    event, buffer, buffer_size, buffer_cursor, character_allow
                )

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
