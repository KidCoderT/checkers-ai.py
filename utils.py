from pygame.font import Font
from pygame import Surface


class FontManager:
    """A simple Pygame Font Manager"""

    def __init__(self):
        self.__fonts = {}

    def create_font(self, font_name: str, font_size: int) -> Font:
        """Creates a new font instance

        Args:
            font_name (str): the path of the font
            font_size (int): the size for the font

        Returns:
            pygame.font.Font: the created font
        """
        font = Font(font_name, font_size)
        self.__fonts[(font_name, font_size)] = font

        return font

    def get_font(self, font_id: tuple[str, int]) -> Font:
        return self.__fonts[font_id]

    def create_text(self, font_id: tuple[str, int], text, color: tuple) -> Surface:
        """Creates a new text with the given font id, text and color

        Args:
            font_id (tuple[str, int]): the font id
            text (str): the text for the font
            color (tuple): the color for the text

        Returns:
            pygame.surface.Surface: _description_
        """
        try:
            self.__fonts[font_id]
        except KeyError:
            self.create_font(*font_id)

        finally:
            font = self.__fonts[font_id]

        text = font.render(text, False, color)
        return text
