import ctypes

from sdl2 import *
from sdl2.sdlimage import *


def scc(code):
    if code < 0:
        print(f"SDL ERROR: {SDL_GetError()}")
        exit(1)


def scp(ptr):
    if ptr == 0:
        print(f"SDL ERROR: {SDL_GetError()}")
        exit(1)
    return ptr


def surface_from_file(file_path):
    IMG_Init(IMG_INIT_PNG)
    data = IMG_Load(file_path)

    if not data:
        print(f"IMG_Load ERROR: {IMG_GetError()}")
        exit(1)
    return data.contents


def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, SDL_WINDOW_RESIZABLE
    )
    renderer = scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED))

    font_surface = surface_from_file(b"charmap-oldschool_white.png")
    font_texture = scp(SDL_CreateTextureFromSurface(renderer, font_surface))
    font_rect = SDL_Rect(x=0, y=0, w=font_surface.w, h=font_surface.h)

    running = True
    while running:
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
        scc(SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0))
        scc(SDL_RenderClear(renderer))
        output_rect = SDL_Rect(
            x=0, y=0, w=font_surface.w * 5, h=font_surface.h * 5
        )
        scc(SDL_RenderCopy(renderer, font_texture, font_rect, output_rect))
        SDL_RenderPresent(renderer)
    SDL_Quit()
    return 0


if __name__ == "__main__":
    main()
