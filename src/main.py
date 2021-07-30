from sdl2 import *
import ctypes
from ctypes import CDLL, byref
from font import *
import os


def surface_from_file(file_path):
    width, height, n, STBI_rgb_alpha = 0, 0, 0, 4
    project_directory = os.path.dirname(os.path.abspath(__file__))
    stb_image = CDLL(os.path.join(project_directory, "stb_image.so"))
    pixels = stb_image.stbi_load(file_path, width, height, n, STBI_rgb_alpha)

    if pixels == None:
        print(
            f"ERROR: couldn't load the file {file_path}: {stb_image.stbi_failure_reason()}"
        )
        exit(1)

    rmask, gmask, bmask, amask = 0, 0, 0, 0
    if SDL_BYTEORDER == SDL_BIG_ENDIAN:
        rmask = 0xFF000000
        gmask = 0x00FF0000
        bmask = 0x0000FF00
        amask = 0x000000FF
    else:
        rmask = 0x000000FF
        gmask = 0x0000FF00
        bmask = 0x00FF0000
        amask = 0xFF000000

    depth = 32
    pitch = 4 * width
    return SDL_CreateRGBSurfaceFrom(
        pixels, width, height, depth, pitch, rmask, gmask, bmask, amask
    )


def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, SDL_WINDOW_RESIZABLE
    )
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    font_surface = surface_from_file("./charmap-oldschool_white.png")
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
