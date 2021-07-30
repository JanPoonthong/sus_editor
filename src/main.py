from sdl2 import *
import ctypes
from font import *


def surface_from_file(filename):
    w, h, n = 0, 0, 0
    return 0


def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, SDL_WINDOW_RESIZABLE
    )
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    # texture = SDL_CreateTexture(
    #     renderer,
    #     SDL_PIXELFORMAT_INDEX8,
    #     SDL_TEXTUREACCESS_STATIC,
    #     FONT_WIDTH,
    #     FONT_HEIGHT
    # )

    surface = SDL_CreateRGBSurfaceFrom(FONT, FONT_WIDTH, FONT_HEIGHT, 8, FONT_WIDTH,
                                      0xFF, 0xFF, 0xFF, 0xFF)

    running = True
    while running:
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
        SDL_SetRenderDrawColor(renderer, 0, 255, 255, 0)
        SDL_RenderClear(renderer)
        SDL_RenderPresent(renderer)
    SDL_Quit()
    return 0


main()
