import pygame


class GUI:

    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                res = element.get_event(event)
                if type(element) == TextBox and res != None:
                    return res


class Label:

    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        #self.bgcolor = pygame.Color("white")
        self.font_color = pygame.Color("black")
        self.font = pygame.font.Font(None, self.rect.height - 4)
        #рассчитываем размер шрифта в зависимости от высоты прямоугольника
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        #surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)


class Button(Label):

    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("blue")
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False


class CheckBox(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.check = pygame.Rect([self.rect.x+self.rect.width+5, self.rect.y, self.rect.height, self.rect.height])
        self.pressed = False

    def render(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        pygame.draw.rect(surface, (255, 255, 255), [self.rect.x+self.rect.width+5, self.rect.y, self.rect.height, self.rect.height])
        if self.pressed:
            pygame.draw.rect(surface, (0, 0, 0),
                             [self.rect.x + self.rect.width + 7, self.rect.y+2, self.rect.height-4, self.rect.height-4])
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check.collidepoint(event.pos):
            self.pressed = not self.pressed


class Flash(Label):

    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("blue")
        self.active = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.active:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)


class TextBox(Label):

    def __init__(self, rect, text, secret=False):
        super().__init__(rect, text)
        self.name = text
        self.secret = secret
        if secret:
            self.text2 = ""
        self.active = False
        self.blink = False
        self.blink_timer = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
                if self.secret:
                    return self.text2
                else:
                    return self.text
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
                    if self.secret:
                        self.text2 = self.text2[:-1]
            elif event.key == 118 and event.mod == 64:
                pygame.scrap.init()
                self.text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')[:-6]
            else:
                if self.secret:
                    if event.unicode:
                        self.text += '*'
                    self.text2 += event.unicode
                else:
                    self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        surface.fill(pygame.Color("white"), self.rect)
        super(TextBox, self).render(surface)
        if self.blink and self.active:
            pygame.draw.line(surface, pygame.Color("black"),
                             (self.rendered_rect.right + 2, self.rendered_rect.top + 2),
                             (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))
        color1 = pygame.Color("white")
        color2 = pygame.Color("black")
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)


