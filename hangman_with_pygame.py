import pygame as pg
from hangman_handler import hangman
from hangman_terminal import word_generator
from string import ascii_lowercase as all_alphabet

man = hangman("hangman_images")
BACKGROUND_COLOR = (171, 135, 255)
FONT_SIZE = 100
objects = []
hangman_obj = []
clock = pg.time.Clock()
themes = [
    "Default",
    "Sports",
    "Countries",
    "Animals",
    "CS",
    "Fruits",
    "Vegetables",
]
man_rect_surf = pg.Surface((450, 600), pg.SRCALPHA)
man_rect = pg.Rect(850, 100, 450, 600)
pg.draw.rect(man_rect_surf, (56, 100, 120), man_rect, 2)

print = lambda *args: ...


def getword(index: int):
    print(themes[index])
    pg.display.set_caption(f"THE HANGMAN GAME -{themes[index]}")
    dic = open(f"{themes[index]}.txt", "r").readlines()
    dic_word = word_generator(dic).lower()
    print(dic_word)
    word_count = [(i, 0) if i in all_alphabet else (i, 1) for i in dic_word]
    return word_count, dic_word


def renderTextCenteredAt(
    screen,
    text,
    colour,
    x,
    y,
    allowed_width,
    size,
    flag=0,
) -> list[pg.Rect]:
    new_size = 0
    rect = pg.Rect(x, y, allowed_width, new_size)
    padd_x = 5
    padd_y = 10
    bounding_box = []
    words = [i for i in text]
    font = pg.font.Font(None, size)
    lines = []
    sep = "" if flag else " "
    fw, fh = 0, 0
    while len(words) > 0:
        line_words = []
        old_width = 0
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(str(line_words[-1]) + sep)
            bounding_box.append(
                pg.Rect(
                    x + old_width + padd_x,
                    y + len(lines) * size + padd_y,
                    fw,
                    fh,
                )
            )
            old_width += fw
            if (
                old_width > allowed_width - fw
            ):  # only if whole font is plotable not small part of it
                print(new_size, text, "yoyoyyo")
                break
        new_size += fh + 10
        line = sep.join(line_words)
        lines.append(line)
    print(lines)
    new_size += fh
    rect.height = new_size
    if not flag:
        pg.draw.rect(screen, BACKGROUND_COLOR, rect)
    # pg.draw.rect(screen, (255, 0, 0), rect, 10)
    for n, line in enumerate(lines):
        fw, fh = font.size(line)
        tx = x + padd_x
        ty = y + n * size + padd_y
        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))
        # print(tx, ty)
    if flag == 0:
        pg.display.update()
    return bounding_box


class alphabet:
    def __init__(self, surface):
        """display all alphabet here"""
        self.rect = pg.Rect(20, 480, 830, 200)
        # pg.draw.rect(surface, (56, 100, 120), self.rect, 2)
        self.surface = surface
        self.box = []
        self.all_alphabet = [[i, 1] for i in all_alphabet]
        # self.all_alphabet = "".join([i[0] if i[1] else "_" for i in all_alphabet])
        self.update()

    def update(self):
        """we mark the used ones and colour not the one in word with red"""
        self.box = renderTextCenteredAt(
            self.surface,
            "".join([i[0] for i in self.all_alphabet]),
            (0, 0, 0),
            self.rect.x,
            self.rect.y,
            self.rect.width,
            FONT_SIZE,
        )
        for n, char in enumerate(self.all_alphabet):
            if not char[1]:
                _box = self.box[n]
                # pg.draw.rect(self.surface, (56, 100, 120), self.box[n], 2)
                pg.draw.line(
                    self.surface,
                    (245, 255, 198),
                    (_box.x, _box.y + _box.height / 2),
                    (_box.x + _box.width - 20, _box.y + _box.height / 2),
                    5,
                )

    def is_collided(self, event):
        for n, el in enumerate(self.box):
            if el.collidepoint(event.pos) and self.all_alphabet[n][1] != 0:
                self.all_alphabet[n][1] = 0
                # pg.draw.rect(self.surface, BACKGROUND_COLOR, self.rect)
                self.update()
                print(event.pos, all_alphabet[n])
                return True, all_alphabet[n]
        return False, None


class Button:
    def __init__(
        self,
        screen,
        x,
        y,
        width,
        height,
        buttonText,
        onclickFunction,
        onePress=False,
    ):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = {
            "normal": (255, 255, 255),
            "hover": (102, 102, 102),
            "pressed": (51, 51, 51),
        }
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        objects.append(self)

    def process(self):
        stop = False
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors["normal"])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors["hover"])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors["pressed"])
                while not stop:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return
                        elif event.type == pg.MOUSEBUTTONUP:
                            stop = True
                if self.onePress:
                    self.onclickFunction()
                    return True
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
                    return True
            else:
                self.alreadyPressed = False
        renderTextCenteredAt(
            self.buttonSurface,
            self.buttonText,
            (0, 0, 0),
            0,
            0,
            self.width,
            25,
            1,
        )
        self.screen.blit(self.buttonSurface, self.buttonRect)
        return False


def word(surface, dic_word):
    """display no of _ for the chosen word by word_generator here"""
    rect = pg.Rect(150, 100, 700, 250)
    # pg.draw.rect(surface, (56, 100, 120), rect, 2)
    # pg.draw.rect(surface, BACKGROUND_COLOR, rect)
    renderTextCenteredAt(
        surface,
        "".join(
            [
                i[0] if i[1] or i[0] == "-" or i[0] == " " or i[0].isdigit() else "_"
                for i in dic_word
            ]
        ),
        (0, 0, 0),
        rect.x,
        rect.y,
        rect.width,
        100,
    )


def body_displayer(screen, rect_surf, rect):
    new = man.update()
    hangman.render(rect_surf, new)
    screen.blit(rect_surf, rect)


def body_reset(screen):
    man.reset()
    man_rect_surf.fill(BACKGROUND_COLOR)
    screen.blit(man_rect_surf, man_rect)


def chooser(screen, n):
    def inside():
        return game(screen, *getword(n))

    return inside


def theme(screen):
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOR)

    if pg.font:
        font = pg.font.Font(None, 100)
        text = font.render("Choose a Theme", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=100)
        background.blit(text, textpos)

    objects.clear()
    btn_WID, btn_HEI = 100, 50
    offset = 80 + btn_WID
    for n, theme_name in enumerate(themes):
        Button(
            screen,
            20 + offset * n,
            screen.get_rect().height / 2 - btn_HEI / 2,
            btn_WID,
            btn_HEI,
            theme_name,
            chooser(screen, n),
        )
    screen.blit(background, (0, 0))
    pg.display.update()
    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                exit(0)
        for obj in objects:
            if obj.process():
                theme(screen)
                return
        pg.display.update()
    return


def game(screen, word_count, dic_word):
    n = 0
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))
    pg.display.flip()

    alpha = alphabet(screen)
    word(screen, word_count)
    running = True
    won = None

    body_reset(screen)
    body_displayer(screen, man_rect_surf, man_rect)
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                exit(0)
            if event.type == pg.MOUSEBUTTONDOWN:
                bol, char = alpha.is_collided(event)
                if bol:
                    word_count = [
                        (i[0], 1) if char == i[0] or i[1] else (i[0], 0)
                        for i in word_count
                    ]
                    word(screen, word_count)
                    print(word_count, dic_word, char, n)
                    if char and not (char in dic_word):
                        n += 1
                        body_displayer(screen, man_rect_surf, man_rect)
                        if n >= 6:
                            running = False
                            won = False
                    if all([i for _, i in word_count]):
                        running = False
                        won = True
        pg.display.update()
    end_screen(screen, won, dic_word)
    return


def end_screen(screen, won, dic_word):
    if won == None:
        return
    running = True
    rec = screen.get_size()
    background = pg.Surface((rec[0] // 2, rec[1]))
    background = background.convert()
    background.fill((255, 172, 228))
    objects.clear()

    def play_func():
        nonlocal running
        running = False

    def setFalse():
        print("Hello")
        main_menu()

    btn_WID, btn_HEI = 100, 50
    Button(
        screen,
        screen.get_rect().width / 2 - btn_WID / 2,
        screen.get_rect().height / 2 - btn_HEI / 2,
        btn_WID,
        btn_HEI,
        "Play Again",
        play_func,
    )
    Button(
        screen,
        screen.get_rect().width / 2 - btn_WID / 2,
        screen.get_rect().height / 2 - btn_HEI / 2 + 100,
        btn_WID,
        btn_HEI,
        "Back",
        setFalse,
    )
    font = pg.font.Font(None, 100)
    dis_str = "YOU WON!" if won else "YOU LOST!"
    yw = pg.font.Font(None, 50).render(
        f"Actual word: {dic_word}", True, (193, 255, 155)
    )
    yw_pos = yw.get_rect(centerx=background.get_width() / 2, y=250)
    text = font.render(dis_str, True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=100)
    background.blit(yw, yw_pos)
    background.blit(text, textpos)
    screen.blit(background, (rec[0] // 4, 0))
    if won:
        body_reset(screen)
        man.flag = 8
    body_displayer(screen, man_rect_surf, man_rect)
    pg.display.flip()

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                exit(0)
        screen.blit(background, (rec[0] // 4, 0))
        for obj in objects:
            obj.process()
        pg.display.update()


def main_menu():
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    pg.display.set_caption("THE HANGMAN GAME")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOR)
    objects.clear()
    if pg.font:
        font = pg.font.Font(None, 100)
        text = font.render("DON'T LET THE MAN HANG", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=100)
        background.blit(text, textpos)

    def play_func():
        print("Play Button Pressed")
        game(screen, *getword(0))

    def theme_func():
        print("Theme Button Pressed")
        theme(screen)

    btn_WID, btn_HEI = 100, 50
    Button(
        screen,
        screen.get_rect().width / 2 - btn_WID / 2,
        screen.get_rect().height / 2 - btn_HEI / 2,
        btn_WID,
        btn_HEI,
        "Play",
        play_func,
    )
    Button(
        screen,
        screen.get_rect().width / 2 - btn_WID / 2,
        screen.get_rect().height / 2 - btn_HEI / 2 + 100,
        btn_WID,
        btn_HEI,
        "Theme",
        theme_func,
    )
    Button(
        screen,
        screen.get_rect().width / 2 - btn_WID / 2,
        screen.get_rect().height / 2 - btn_HEI / 2 + 200,
        btn_WID,
        btn_HEI,
        "Exit",
        exit,
    )
    screen.blit(background, (0, 0))
    pg.display.flip()
    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        screen.blit(background, (0, 0))

        for obj in objects:
            if obj.process():
                main_menu()
                return
        pg.display.flip()
    pg.quit()
    exit(code=0)


if __name__ == "__main__":
    pg.init()
    main_menu()
