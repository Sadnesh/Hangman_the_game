# import pg as pg


# def gen(rect, image):
#     surf = pg.Surface((600, 600))
#     surf.blit(image, rect)
import pygame as pg
import os

b = 10


class hangman:
    def __init__(self, path):
        self.image = self.load_image(path)
        self.flag = 0
        self.old = self.image[0].copy()

    def load_image(self, path):
        obj = []
        for i in os.listdir(path):
            # you can add any file type you want here
            if i.endswith(".png") and i.split(".")[0].isnumeric():
                temp = pg.image.load(os.path.join(path, i))
                rec = temp.get_rect()
                temp = temp.subsurface((b, b, rec.width - 2 * b, rec.height - 2 * b))
                obj.append(temp.copy())
        return obj

    def update(self):
        edge_cases = [4, 6, 7]
        this = self.image[self.flag % len(self.image)].copy()
        to = self.old
        self.flag += 1
        if self.flag in edge_cases:
            to, this = this, to
        to.blit(this, (0, 0))
        self.old = to
        return self.old

    @staticmethod
    def render(rect_surf, image: pg.Surface):
        width = rect_surf.get_width()
        height = rect_surf.get_height()
        new_size = (width, height)
        image = aspect_scale(image, *new_size)
        rec = image.get_rect()
        rec.center = width // 2, height // 2
        rect_surf.blit(image, rec)

    def reset(self):
        self.old = self.image[0].copy()
        self.flag = 0


def aspect_scale(img, bx, by):
    """Scales 'img' to fit into box bx/by.
    This method will retain the original image's aspect ratio"""
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pg.transform.scale(img, (sx, sy))


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((450, 600))
    man = hangman("hangman_images")
    img = man.update()
    done = False
    bg = (127, 127, 127)
    while not done:
        for event in pg.event.get():
            screen.fill(bg)
            hangman.render(screen, img)
            # rect = img.get_rect()
            # rect.center = 200, 150
            # screen.blit(img, rect)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    man.reset()
                img = man.update()

            if event.type == pg.QUIT:
                done = True
        pg.display.update()
