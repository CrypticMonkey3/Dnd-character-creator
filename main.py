from random import randrange
from pygame.locals import *
from typing import *
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

    def draw(self, coord: Tuple[int, int], set_rect: bool = True) -> None:
        """
        Blit image onto the screen.
        :param Tuple[int, int] coord: The coordinates where we'll draw the race image.
        :param bool set_rect: Checks whether we want to set the rect of an image.
        :return: None
        """
        self.surface.blit(self.image, [coord[0], coord[1]])
        if set_rect:
            self.set_rect(coord)
        pygame.display.update(Rect(coord[0], coord[1], self.image.get_width(), self.image.get_height()))

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
        self.rect = Rect(coord[0], coord[1], self.image.get_width(), self.image.get_height())

    def get_name(self) -> str:
        """
        Gets the name of the chosen thing.
        :return: str
        """
        return self.name

    def get_image(self) -> pygame.Surface:
        """
        Gets the image object
        :return: pygame.Surface
        """
        return self.image


class Select(Sprite):
    def __init__(self, surface, image, mouse_pos: Tuple[int, int]):
        super().__init__(surface, image)
        self.mouse_pos = mouse_pos
        self.selectable = False

    def hover(self, rgb: Tuple[int, int, int], replacement_colour: Tuple[int, int, int], set_rect: bool = True) -> None:
        """
        If your mouse is hovering over an image, it will change the border colour, and will tell the program that it's
        selectable.
        :param Tuple[int, int, int] rgb: The colour to replace the original colour.
        :param Tuple[int, int, int] replacement_colour: The original colour.
        :param bool set_rect: Whether we want to set the new rect of the image or not.
        :return: None
        """
        px_array = pygame.PixelArray(self.image)
        if self.get_rect().collidepoint(self.mouse_pos) and self.surface.get_at((self.mouse_pos[0], self.mouse_pos[1]))\
                != (0, 0, 0) and pygame.mouse.get_focused() != 0:
            # if mouse pos is over an image, and where the mouse is over is not black (the border) and the mouse is on
            # the screen
            px_array.replace(replacement_colour, rgb)
            self.selectable = True
        else:
            px_array.replace(rgb, replacement_colour)
            self.selectable = False

        px_array.close()  # close the px_array
        self.draw((self.get_rect()[0], self.get_rect()[1]), set_rect)  # draw new results onto the screen

    def is_selectable(self) -> bool:
        """
        Returns True, if object is selectable, False otherwise.
        :return: bool
        """
        return self.selectable

    def set_selectable(self, select: bool) -> None:
        """
        Sets the selectivity of the object.
        :param bool select: Whether we can now select the object or not.
        :return: None
        """
        self.selectable = select


class Box(Sprite):
    def __init__(self, surface, image: str, category: str, value: int = 0):
        super().__init__(surface, image)
        self.category = category
        self.value = value
        self.found_font_size = False
        self.prev_font_size = (0, 0)
        self.font = 1

    def title(self, font_size: int, width: int = 127, height: int = 24) -> int:
        """
        Finds length of category, and depending on that length find a suitable font size, and display on box.
        :param int width: The amount of pixels wide the text has to be before it's acceptable.
        :param int height: The amount of pixels high the text has to be before it's acceptable.
        :param int font_size: Our initial font size
        :return: int, 1 to increase font size, -1 to decrease, 0 if it's an acceptable font size.
        """
        # need a way to tell whether font needs to increase or not: perhaps using 1 for increase, -1 for decrease, 0
        # otherwise.
        self.font = pygame.font.SysFont("Calibri", font_size)
        size = self.font.size(self.category)




    def get_value(self) -> int:
        """
        Gets the value of the category.
        :return: int
        """
        return self.value


class StatsGenerator:
    def __init__(self, image_name: str = "", stats=None):
        self.stats = stats
        if self.stats is None:
            self.stats = {}
        self.race_name = image_name

    def roll(self) -> dict:
        """
        Rolls 4D6 and records the three highest scores per ability.
        :return: The dictionary of the stats.
        """
        ability_score = []
        scores_temp = []
        for ability in range(6):  # loop around 6 times/ number of abilities there are.
            for i in range(4):  # loop around the number of dice per ability (4).
                scores_temp.append(randrange(1, 7))  # add it to the end of the temporary list
            scores_temp.sort()  # sort list, so highest items
            ability_score.append(scores_temp[-1] + scores_temp[-2] + scores_temp[-3])
            scores_temp.clear()

        self.stats["Strength"] = ability_score[0]
        self.stats["Dexterity"] = ability_score[1]
        self.stats["Charisma"] = ability_score[2]
        self.stats["Constitution"] = ability_score[3]
        self.stats["Intelligence"] = ability_score[4]
        self.stats["Wisdom"] = ability_score[5]

        return self.stats

    def set_name(self, name) -> None:
        """
        Sets name of users chosen race.
        :return: None
        """
        self.race_name = name

    def modifier(self, category: str, amount: int) -> dict:
        """
        Modifies the stats of the character chosen.
        :param str category: The stat category we are manipulating, ie Strength, dex, etc.
        :param int amount: The amount we are increasing that stat category by.
        :return: The new dict.
        """
        self.stats[category] += amount
        return self.stats


class Main:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-elf", "Half-orc", "Halfling", "Human", "Tiefling"]
        self.classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue",
                        "Sorcerer", "Warlock", "Wizard"]
        self.race_description = {"Dragonborn": "Born of dragons, as their name proclaims, the dragonborn walk proudly "
                                               "through a world that greets them with fearful incomprehension. Shaped "
                                               "by draconic gods or the dragons themselves, dragonborn originally "
                                               "hatched from dragon eggs as a unique race, combining the best "
                                               "attributes of dragons and humanoids. Some dragonborn are faithful "
                                               "servants to true dragons, others form the ranks of soldiers in great "
                                               "wars, and still others find themselves adrift, with no clear calling "
                                               "in life. Racial traits include your Strength score increasing by 2, "
                                               "and your Charisma score increasing by 1.",

                                 "Dwarf": "The members of this race are hearty and steadfast, standing about 4-1/2 "
                                          "feet tall but powerfully built and extremely broad. They have a strong "
                                          "connection to mountains and rocky places. They can live to be more than "
                                          "400 years old. In game terms, dwarves receive a +2 to Constitution. "
                                          "They also receive bonuses against poison, spells, and magical effects. "
                                          "Dwarves also have darkvision, the ability to see up to 60 feet in the dark.",

                                 "Human": "These are people just like you and us. They are adaptable, flexible, "
                                          "and extremely ambitious. Compared to the other races, humans are "
                                          "relatively short-lived. In game terms, humans get an extra feat on all "
                                          "their stats.",

                                 "Elf": "Elves have a strong connection to the natural world, especially woodlands. "
                                          "They can live to be more than 700 years old. Known for being artists of "
                                          "both song and magic, elves have an affinity for spell-casting and lore. "
                                          "They stand about 5-1/2 feet tall, appearing graceful and frail. Elves "
                                          "receive a +2 to Dexterity. They are immune to sleep effects and receive "
                                          "a bonus against enchantment spells. Elves have low-light vision and a "
                                          "racial bonus on Listen, Search, and Spot checks.",

                                 "Halfling": "The members of this race are clever and capable — much more so than "
                                             "their small size might indicate. Standing about 3 feet tall, with slim, "
                                             "muscular builds, halflings are athletic and outgoing. Curious to a fault "
                                             "and usually with a daring to match, halflings love to explore. They tend "
                                             "to live well past 100. Halflings receive a +2 Dexterity to reflect their "
                                             "small statures. They also receive bonuses to Climb, Jump, Listen, and "
                                             "Move Silently checks, as well as a bonus to all saving throws due to "
                                             "their fearlessness and ability to avoid damage.",

                                 "Tiefling": "Tieflings tended to have an unsettling air about them, and most people "
                                             "were uncomfortable around them, whether they were aware of the "
                                             "tiefling's unsavory ancestry or not. While some looked like normal "
                                             "humans, most retained physical characteristics derived from their "
                                             "ancestor, with the most common such features being horns, "
                                             "non-prehensile tails, and pointed teeth. Some tieflings also had eyes "
                                             "that were solid orbs of black, red, white, silver, or gold, while "
                                             "others had eyes more similar to those of humans. Other, more unusual "
                                             "characteristics included a sulfurous odor, cloven feet, or a general "
                                             "aura of discomfort they left on others. In game terms, get an "
                                             "additional +2 in their charisma stat and a +1 in their intelligence.",

                                 "Gnome": "Gnomes, or the Forgotten Folk as they were sometimes known, were small "
                                          "humanoids known for their eccentric sense of humor, inquisitiveness, and "
                                          "engineering prowess. Having had few overt influences on the world's history "
                                          "but many small and unseen ones, gnomes were often overlooked by the powers "
                                          "that be, despite their craftiness and affinity for illusion magic. Gnomes "
                                          "were present in nearly every human city and most caravan-stop villages "
                                          "where other cultures and non-human races were at least tolerated."
                                          "In game terms- this character will increase your intelligence stat by +2.",

                                 "Half-orc": "Half-orcs were humanoids born of both human and orc ancestry by a "
                                             "multitude of means. Having the combined physical power of their orcish "
                                             "ancestors with the agility of their human ones, half-orcs were "
                                             "formidable individuals. Though they were often shunned in both human "
                                             "and orcish society for different reasons, half-orcs have proven "
                                             "themselves from time to time as worthy heroes and dangerous villains. "
                                             "Their existence implied an interesting back story that most would not "
                                             "like to dwell on. In game terms, your strength stat gets +2, whilst your "
                                             "constitution stat gets a +1 bonus.",

                                 "Half-elf": "Half-elves (also called Cha'Tel'Quessir in elven) were humanoids born "
                                             "through the union of an elf and a human. Whether a half-elf was raised "
                                             "by their human parent or their elven parent, they often felt isolated "
                                             "and alone. Because they took around twenty years to reach adulthood, "
                                             "they matured quickly when raised by elves, making them feel like an "
                                             "outsider in either place. Like their elven parents, half-elves were "
                                             "immune to the effects of the enchantment of magic, whilst also "
                                             "inheriting the ability to see keenly in low-light conditions, with "
                                             "little or no ill effect, and had enhanced senses of sight and hearing "
                                             "compared to their human brethren. In game terms- they receive +2 in "
                                             "Charisma, and +1 to any other ability scores."
                                 }

        self.user_stats = {}
        self.mouse_pos = (0, 0)
        self.dnd_class = ""
        self.dnd_race = ""
        self.image_check = 0

        self.stats_gen = StatsGenerator(stats=self.user_stats)
        self.races = self.spawn(self.races, 200, 250, True, True, 0, 0)
        self.classes = self.spawn(self.classes, 0, 0, False, True, 0, 0)
        self.back = Select(self.surface, "BACK", self.mouse_pos)
        self.roll = Select(self.surface, "Roll", self.mouse_pos)
        self.box = Select(self.surface, "Box", self.mouse_pos)

        self.running = True
        self.choose_race = True
        self.choose_class = False
        self.dice_roller = False
        self.begin_roll = False
        self.race_potential_index = -1  # the potential to select an image of a race
        self.class_potential_index = -1
        self.draw_once = True

    def process(self) -> None:
        """
        The main game process.
        :return: None
        """
        if not self.choose_race:
            self.back.mouse_pos = self.mouse_pos
            self.back.hover((133, 0, 255), (255, 0, 0))

        if self.choose_race:
            self.hov_image(self.races, (0, 0, 255), (0, 0, 0))

        elif self.choose_class:
            self.hov_image(self.classes, (236, 208, 208), (255, 255, 255))

        elif self.dice_roller:
            self.roll.mouse_pos = self.mouse_pos
            self.roll.hover((0, 0, 255), (255, 255, 255))
            if self.begin_roll:  # if roll button is pressed.
                self.stats_gen.set_name(self.races[self.race_potential_index].get_name())
                self.user_stats = self.stats_gen.roll()
                self.begin_roll = False  # so it won't continuously generate new rolls

            if self.user_stats:
                # sort numbers into boxes/ stat categories, allow dragging.
                ...
            else:
                # draw in the boxes
                if self.draw_once:
                    self.box.draw((25, 50))
                    self.render_text("Wisdom", 48, 60, (0, 0, 0), 30, update_rect=(48, 60, 120, 25))
                    self.box.draw((25, HEIGHT // 2 + 65))
                    self.render_text("Strength", 48, HEIGHT // 2 + 73, (0, 0, 0), 30, update_rect=(48, HEIGHT // 2 + 75,
                                                                                                   120, 25))
                    self.box.draw((225, 50))
                    self.render_text("Intelligence", 241, 60, (0, 0, 0), 25, update_rect=(241, 60, 120, 25))
                    self.box.draw((225, HEIGHT // 2 + 65))
                    self.render_text("Dexterity", 244, HEIGHT // 2 + 73, (0, 0, 0), 30, update_rect=(244, HEIGHT // 2 +
                                                                                                     75, 120, 25))
                    self.box.draw((425, 50))
                    self.render_text("Constitution", 438, 60, (0, 0, 0), 25, update_rect=(438, 60, 125, 25))
                    self.box.draw((425, HEIGHT // 2 + 65))
                    self.render_text("Charisma", 444, HEIGHT // 2 + 73, (0, 0, 0), 30, update_rect=(444, HEIGHT // 2 +
                                                                                                    73, 120, 25))
                    self.draw_once = False

        self.check_events()
        self.image_check += 1

    def hov_image(self, images: list, colour_r: Tuple[int, int, int], colour_o: Tuple[int, int, int]) -> None:
        """
        Manages all hovering actions of the mouse on an image, and anything the user selects (as a result).
        :param list images: Image list.
        :param Tuple[int, int, int] colour_r: The replacement of the original colour, if mouse is over an image.
        :param Tuple[int, int, int] colour_o: The original colour which will be replaced or regained.
        :return: None
        """
        try:
            images[self.image_check]
        except IndexError:
            self.image_check = 0

        images[self.image_check].mouse_pos = self.mouse_pos
        images[self.image_check].hover(colour_r, colour_o, False)

        if images[self.image_check].is_selectable() and self.choose_race:
            self.race_potential_index = self.image_check

        elif images[self.image_check].is_selectable() and self.choose_class:
            self.class_potential_index = self.image_check

    def set(self, classes: bool = False, roller: bool = False) -> None:
        """
        Sets one of the interfaces onto the screen.
        :param bool classes: True, if we want to reset the classes
        :param bool roller: True, if the user wants to proceed on the ability roller.
        :return: None
        """
        if classes:
            # save name chosen
            self.dnd_race = self.races[self.race_potential_index].get_name()

            # add a background for description of character
            self.surface.fill((0, 0, 0), Rect(0, 0, 300, 750))
            pygame.display.update(Rect(0, 0, 300, 750))

            # add chosen image to top left screen
            image_px_array = pygame.PixelArray(self.races[self.race_potential_index].get_image())
            image_px_array.replace((0, 0, 255), (0, 0, 0))
            image_px_array.close()
            self.races[self.race_potential_index].draw((50, 25), False)

            # add back button
            self.back.draw((0, 0))

            # add description of race
            render_string = self.race_description[self.races[self.race_potential_index].get_name()]
            self.render_text(render_string, 20, 300, (255, 255, 255), 16, 20)

            # spawn new images
            self.spawn(self.classes, 100, 187, True, False, 300, 0)

            # set new variables.
            self.choose_race = False
            self.choose_class = True
            self.races[self.race_potential_index].set_selectable(False)

        elif roller:
            # save dnd class
            self.dnd_class = self.classes[self.class_potential_index].get_name()

            # reset screen to white.
            self.surface.fill((255, 255, 255))
            pygame.display.update()

            # display button to begin roll.
            self.roll.draw(((WIDTH // 2) - 50, HEIGHT // 2 - 60))

            # switch bool variables.
            self.dice_roller = True
            self.choose_class = False
            self.classes[self.class_potential_index].set_selectable(False)

    def check_events(self) -> None:
        """
        Checks for any pygame events.
        :return: None
        """
        event = pygame.event.poll()  # gets one event at a time- stops our use of for loop in main loop.
        if event.type == MOUSEMOTION:  # if mouse is moved
            self.mouse_pos = pygame.mouse.get_pos()  # get it's new position

        if event.type == MOUSEBUTTONUP and self.races[self.race_potential_index].is_selectable() and self.choose_race:
            # if the mouse selects something on the screen and the user is selecting their race.
            # set original rect so, we can re-arrange race menu accordingly later.
            self.set(True)

        elif event.type == MOUSEBUTTONUP and self.classes[self.class_potential_index].is_selectable() and \
                self.choose_class:
            # once we have selected our class, we move onto the dice roller
            self.set(roller=True)

        elif event.type == MOUSEBUTTONUP and self.back.is_selectable():
            # if we have clicked on the back button.
            if self.choose_class:
                self.choose_class = False
                self.choose_race = True

            elif self.dice_roller:
                self.draw_once = True
                self.set(True)

        elif event.type == MOUSEBUTTONUP and self.roll.is_selectable():
            # if we have pressed the roll button.
            self.begin_roll = True

        elif (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # if X is pressed or ESC is pressed
            self.running = False  # end program

    def render_text(self, text: str, x_start: int, y_start: int, rgb: Tuple[int, int, int], font_size: int,
                    y_increment: int = 0, limit: int = 37,
                    update_rect: Tuple[int, int, int, int] = (0, 300, 300, 450)) -> None:
        """
        Renders the score. For loop in here should be alright as we're loading a new selection page for the user.
        :param int y_increment: How much the y axis will be incremented.
        :param str text: The message we are displaying on the screen.
        :param int x_start: The top left corner of the message in the x position.
        :param int y_start: The top left corner of the message in the y position.
        :param Tuple[int, int, int] rgb: RGB value of the text- the colour the message is going to be in.
        :param int font_size: The size of the font.
        :param int limit: Line limit before we move to a new line.
        :param Tuple[int, int, int, int] update_rect: The rect to which we will update the screen.
        :return: None
        """
        split_text = text.split(" ")  # splits text
        font = pygame.font.SysFont("Calibri", font_size)  # gathers type of font and size
        temp_text = ""  # temporary string

        if len(split_text) == 1:
            temp_text = text

        else:
            for word in split_text:  # for each word in the split text variable.
                if len(word) + len(temp_text) < limit:  # if length of word and length of temporary string has not
                    # reached the limit
                    temp_text += f"{word} "  # add the word on the temporary string.
                else:
                    text_surface = font.render(temp_text, False, rgb)  # make text surface
                    self.surface.blit(text_surface, [x_start, y_start])  # blit text at coordinates
                    temp_text = f"{word} "  # any word carried over is the start of the new temporary string.
                    y_start += y_increment  # increment y axis

        # in case loop stopped and there was some left over text, render and blit it.
        text_surface = font.render(temp_text, False, rgb)
        self.surface.blit(text_surface, [x_start, y_start])
        # update screen
        pygame.display.update(Rect(update_rect))

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

        if make_class:
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
