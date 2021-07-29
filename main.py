import sdl2
import ctypes


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    window = sdl2.SDL_CreateWindow(
        b"Sus Editor", 0, 0, 800, 600, sdl2.SDL_WINDOW_RESIZABLE
    )
    renderer = sdl2.SDL_CreateRenderer(
        window, -1, sdl2.SDL_RENDERER_ACCELERATED
    )

    running = True
    while running:
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
    sdl2.SDL_Quit()
    return 0


main()
