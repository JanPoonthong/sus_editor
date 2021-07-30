from sdl2 import *
import ctypes


def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, SDL_WINDOW_RESIZABLE
    )
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

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
