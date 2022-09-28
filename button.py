import pygame


class Button:
    BTN_COLOR = pygame.Color("#183037")
    SHADOW_COLOR = pygame.Color("#000000")

    BTN_ON_HOVER_COLOR = pygame.Color("#23444E")
    SHADOW_ON_HOVER_COLOR = pygame.Color("#1F1F1F")

    TEXT_COLOR = pygame.Color("#ffffff")

    BORDER_RADIUS = 9

    def __init__(
        self,
        topleft: tuple[int, int],
        text: str,
        w_diff: int,
        h_diff: int,
        width: int,
        height: int,
        font: pygame.font.Font,
    ):
        self.position = pygame.Vector2(*topleft)
        self.full_btn = self.top_rect = pygame.Rect(
            self.position.x, self.position.y, width, height
        )

        final_width, final_height = width - w_diff, height - h_diff
        self.top_rect = pygame.Rect(
            self.position.x, self.position.y, final_width, final_height
        )
        self.bottom_rect = pygame.Rect(
            self.position.x + w_diff,
            self.position.y + h_diff,
            final_width,
            final_height,
        )

        self.clicked = False
        self.text = font.render(text, False, self.TEXT_COLOR)

    def update(self, screen: pygame.surface.Surface) -> bool:
        clicked = False

        mouse_pos = pygame.mouse.get_pos()
        left_button_state = pygame.mouse.get_pressed()[0]
        is_hovering = self.full_btn.collidepoint(*mouse_pos)

        if not self.clicked and is_hovering and left_button_state == 1:
            self.clicked = True
            clicked = True

            self.top_rect.x = self.bottom_rect.x
            self.top_rect.y = self.bottom_rect.y

        if self.clicked and (left_button_state == 0):
            self.clicked = False

            self.top_rect.x = self.full_btn.x
            self.top_rect.y = self.full_btn.y

        bottom_btn_color = (
            self.SHADOW_COLOR if not is_hovering else self.SHADOW_ON_HOVER_COLOR
        )
        pygame.draw.rect(
            screen, bottom_btn_color, self.bottom_rect, border_radius=self.BORDER_RADIUS
        )

        top_btn_color = self.BTN_COLOR if not is_hovering else self.BTN_ON_HOVER_COLOR
        pygame.draw.rect(
            screen, top_btn_color, self.top_rect, border_radius=self.BORDER_RADIUS
        )

        screen.blit(
            self.text,
            (
                self.top_rect.centerx - self.text.get_width() / 2,
                self.top_rect.centery - self.text.get_height() / 2,
            ),
        )

        return clicked
