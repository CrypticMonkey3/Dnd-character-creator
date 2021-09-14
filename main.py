from typing import *
from pygame.locals import *
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 750
FPS_Clock = pygame.time.Clock()
FPS = 60


class Sprite:
    def __init__(self, surface, image: str):
        self.surface = surface
        self.name = image
        self.image = pygame.image.load(f"Graphics/{image}.png").convert_alpha(self.surface)
        self.rect = self.image.get_rect()

    def draw(self, coord: Tuple[int, int]):
        """
        Blit image onto the screen.
        :param Tuple[int, int] coord: The coordinates where we'll draw the race image.
        :return: None
        """
        self.surface.blit(self.image, [coord[0], coord[1]])
        self.set_rect(coord)
        pygame.display.update(self.get_rect())

    def get_rect(self):
        """
        Returns rectangular binding of an object.
        :return: Rect of image
        """
        return self.rect

    def set_rect(self, coord) -> None:
        """
        Sets the rectangular binding of an object
        :param Tuple[int, int] coord: Coordinates of left, and top.
        :return: None
        """
        self.rect = Rect(coord[0], coord[1], 200, 250)


class Select(Sprite):
    def __init__(self, surface, image, mouse_pos: Tuple[int, int]):
        super().__init__(surface, image)
        self.mouse_pos = mouse_pos
        self.selectable = False

    def hover(self, rgb: Tuple[int, int, int]) -> None:
        """
        If your mouse is hovering over an image, it will change the border colour, and will tell the program that it's
        selectable
        :return: None
        """
        px_array = pygame.PixelArray(self.image)
        if self.get_rect().collidepoint(self.mouse_pos) and self.surface.get_at((self.mouse_pos[0], self.mouse_pos[1]))\
                != (0, 0, 0, 255) and pygame.mouse.get_focused() != 0:
            # if mouse pos is over an image, and where the mouse is over is not black (the border) and the mouse is on
            # the screen
            px_array.replace((0, 0, 0), rgb)  # replace all occurrences of black with black
            self.selectable = True
        else:
            px_array.replace(rgb, (0, 0, 0))  # replace all occurrences of blue with black
            self.selectable = False

        px_array.close()  # close the px_array
        self.draw((self.get_rect()[0], self.get_rect()[1]))  # draw new results onto the screen


class Main:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-elf", "Half-orc", "Halfling", "Human", "Tiefling"]
        self.classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue",
                        "Sorcerer", "Warlock", "Wizard"]
        self.mouse_pos = (0, 0)
        self.dnd_class = ""
        self.dnd_race = ""
        self.image_check = 0

        self.races = self.spawn(self.races, 200, 250, True, True, 0, 0)
        self.classes = self.spawn(self.classes, 0, 0, False, True, 0, 0)

        self.running = True
        self.choose_race = True
        self.choose_class = False
        self.potential_index = -1  # the potential to select an image

    def process(self) -> None:
        """
        The main game process.
        :return: None
        """
        if self.choose_race:
            try:
                self.races[self.image_check]
            except IndexError:
                self.image_check = 0

            self.races[self.image_check].mouse_pos = self.mouse_pos
            self.races[self.image_check].hover((0, 0, 255))

            if self.races[self.image_check].selectable:
                self.potential_index = self.image_check

        elif self.choose_class:
            ...

        self.check_events()
        self.image_check += 1

    def check_events(self) -> None:
        """
        Checks for any pygame events.
        :return: None
        """
        event = pygame.event.poll()  # gets one event at a time- stops our use of for loop in main loop.
        if event.type == MOUSEMOTION:  # if mouse is moved
            self.mouse_pos = pygame.mouse.get_pos()  # get it's new position
        if event.type == MOUSEBUTTONUP and self.races[self.potential_index].selectable:  # if the mouse selects something on the screen.
            if self.choose_race:  # if the user is selecting their race.
                # select that image and move onto a different stage
                self.dnd_race = self.races[self.potential_index].name
                self.choose_race = False
                self.choose_class = True
        elif (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # if X is pressed or ESC is pressed
            self.running = False  # end program

    def spawn(self, image_list: list, x_increment: int, y_increment: int, draw: bool, make_class: bool, x_start: int,
              y_start: int) -> List:
        """
        Makes an image class and draw it (if needed)
        :param list image_list: The image list we are manipulating.
        :param int x_increment: How much we are increasing in the x axis.
        :param int y_increment: How much we are increasing in the y axis.
        :param bool draw: True, if we will blit the image on the screen, False, if not.
        :param bool make_class: True, if we want to make the images an object, False, otherwise.
        :param int x_start: Where the x position will start.
        :param int y_start: Where the y position will start.
        :return: The new object list
        """
        x = x_start
        y = y_start
        for counter, image in enumerate(image_list):
            if make_class:
                image_list[counter] = Select(self.surface, image_list[counter], self.mouse_pos)
            if draw:
                image_list[counter].draw((x, y))

            x += x_increment
            if x == 600:
                y += y_increment
                x = x_start

        return image_list

    def run(self) -> None:
        """
        Controls main game loop
        :return: None
        """
        while self.running:
            self.process()
            # set the caption to show the FPS to two decimal places
            pygame.display.set_caption(f"FPS: {FPS_Clock.get_fps():4.2f}")
            FPS_Clock.tick(FPS)


if __name__ == "__main__":
    program = Main()
    program.run()
