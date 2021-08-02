from sdl2 import SDL_Rect


class SdlRectAscii:
    """
    :return SDL_Rect(x=int, y=int, w=int, h=int, ascii=chr)
    """

    def __init__(self, x, y, w, h, asci):
        self.get_lp_sdl_rect = SDL_Rect(x, y, w, h)
        self.asci = chr(asci)

    def __repr__(self):
        return f"SDL_Rect(x={self.get_lp_sdl_rect.x}, y={self.get_lp_sdl_rect.y}, w={self.get_lp_sdl_rect.w}, h={self.get_lp_sdl_rect.h}, ascii={self.asci})"
