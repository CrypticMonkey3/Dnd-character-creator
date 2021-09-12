from typing import *
from pygame.locals import *
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 750
FPS_Clock = pygame.time.Clock()
FPS = 60


class Race:
    def __init__(self, surface, mouse_pos: Tuple[int, int], race: str):
        self.surface = surface
        self.mouse_pos = mouse_pos
        self.race = pygame.image.load(f"Graphics/{race}.png").convert_alpha(self.surface)
        self.rect = self.race.get_rect()

    def draw(self, coord: Tuple[int, int]) -> None:
        """
        Blit image onto the screen.
        :param Tuple[int, int] coord: The coordinates where we'll draw the race image.
        :return: None
        """
        self.surface.blit(self.race, [coord[0], coord[1]])
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

    def enlarge(self) -> None:
        """
        If your mouse is over an image, it will enlarge said image by around 2x and decrease the others as a result.
        :return: None
        """
        if self.get_rect().collidepoint(self.mouse_pos) and self.surface.get_at((self.mouse_pos[0], self.mouse_pos[1]))\
                != (0, 0, 0):
            # if mouse is hovering over an image and the mouse is not hovering over a black border.
            # enlarge image
            self.race = pygame.transform.scale(self.race, (self.get_rect()[0] * 2, self.get_rect()[1] * 2))
            self.draw((self.get_rect()[0] * 2, self.get_rect()[1] * 2))
            # make other images smaller
            print("S")


class Main:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-elf", "Half-orc", "Halfling", "Human", "Tiefling"]
        self.mouse_pos = (0, 0)
        self.image_check = 0

        x = 0
        y = 0
        for counter, race in enumerate(self.races):  # quick for loop before the game- to load all graphics.
            self.races[counter] = Race(self.surface, self.mouse_pos, race)
            self.races[counter].draw((x, y))
            x += 200
            if x == 600:
                y += 250
                x = 0

        self.running = True

    def process(self) -> None:
        """
        The main game process.
        :return: None
        """
        self.check_events()

        try:
            self.races[self.image_check]
        except IndexError:
            self.image_check = 0

        self.races[self.image_check].mouse_pos = self.mouse_pos
        self.races[self.image_check].enlarge()
        print(self.mouse_pos)
        self.image_check += 1

    def check_events(self) -> None:
        """
        Checks for any pygame events.
        :return: None
        """
        event = pygame.event.poll()  # gets one event at a time- stops our use of for loop in main loop.
        if event.type == MOUSEMOTION:  # if mouse is moved
            self.mouse_pos = pygame.mouse.get_pos()  # get it's new position
        elif (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # if X is pressed or ESC is pressed
            self.running = False  # end program

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
