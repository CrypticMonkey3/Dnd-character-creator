from tkinter import *
from tkinter import ttk
import tkinter.font as font
from selenium import webdriver
from pygeckodriver import geckodriver_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import os.path

WIDTH = 400
HEIGHT = 304


class WebScraper:
    def __init__(self, user_agent, url: str = ""):
        self.USER_AGENT = user_agent
        self._HEADER = {"user-agent": self.USER_AGENT}
        self.driver = None
        self.url = url

    def remote_web_for(self, link) -> None:
        """
        Creates a remote web-driver for the given link.
        :param str link: The link we want to get to.
        :return: None
        """
        self.driver = webdriver.Firefox(executable_path=geckodriver_path)  # creates separate (remote) window of
        # firefox.
        self.driver.get(link)  # gets the page associated to the given link.
        self.url = link

    def click_button(self, xpath: str) -> None:
        """
        Clicks a button on the current web-driver.
        :param str xpath: The xpath to get to the button, which will then get clicked.
        :return: None
        """
        self.driver.find_element_by_xpath(xpath).click()

    def wait(self, time) -> None:
        """
        Let's the driver wait for a couple moments.
        :param int time: The amount of time we are waiting for.
        :return: None
        """
        WebDriverWait(self.driver, time)

    def close(self) -> None:
        """
        Closes the current web-driver.
        :return: None
        """
        self.driver.close()


class SetupGUI:
    def __init__(self, root):
        self.scraper = WebScraper("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/93.0")
        self.option = StringVar()
        self.title_message = "Dnd Startup"

        # Basic root stuff
        self.root = root
        self.root.title(self.title_message)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        # setting the main frame.
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid()
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # setting any image objects
        self.dndimage_obj = PhotoImage(file="Graphics/Leather texture.png")
        self.dndimage_label = ttk.Label(self.mainframe, image=self.dndimage_obj)

        # setting any text objects.
        self.title = ttk.Label(self.mainframe, text="Welcome to Dnd Startup", font=font.Font(size=13))

        # setting any radiobuttons
        self.gui_version = ttk.Radiobutton(self.mainframe, text="GUI version", variable=self.option, value="GUI")
        self.text_version = ttk.Radiobutton(self.mainframe, text="Text-based version", variable=self.option,
                                            value="TEXT")

        # setting up any buttons.
        self.download_button = ttk.Button(self.mainframe, text="Download")

    def dispatcher(self, event: str) -> None:
        """
        Handles all user input/ events
        :param str event: The event
        :return: None
        """
        if event == "DOWNLOAD":
            try:
                self.scraper.remote_web_for("https://github.com/CrypticMonkey3/Dnd-character-creator")
                self.scraper.click_button("//summary[normalize-space()='Code']")
                # clicks the 'Code' button.
                # normalize-space() trims the left and right side of the text of any whitespaces.
                # so we are finding the text: 'summary' that says 'Code', which will then be clicked.
                self.scraper.click_button("//a[normalize-space()='Download ZIP']")
                self.scraper.wait(7)
                self.scraper.close()
                if self.title_message != "Dnd Startup":
                    self.title_message = "Dnd Startup"

            except WebDriverException:
                self.scraper.close()
                self.title_message += " -> No Internet available"

            if os.path.exists(r"C:\Users\olive\Downloads\Dnd-character-creator-main.zip"):
                # add the green dnd logo instead of the red one.
                ...

        self.root.title(self.title_message)

    def process(self) -> None:
        """
        The processes to do before the program is going to be run, like any bindings, gridding, etc.
        :return: None.
        """
        # Gridding
        self.dndimage_label.grid(column=0, row=0, sticky=(N, W))
        self.title.grid(column=1, row=0, sticky=(N, W))
        self.gui_version.grid(column=1, row=0, sticky=(N, W), pady=50)
        self.text_version.grid(column=1, row=0, sticky=(N, W), pady=70)
        self.download_button.grid(column=1, row=0, sticky=(S, E), pady=278)

        # things for the dispatcher
        self.download_button.config(command=lambda: self.dispatcher("DOWNLOAD"))

    def run(self) -> None:
        """
        Leads up to the running of the program.
        :return: None
        """
        self.process()
        self.root.mainloop()


setup = SetupGUI(Tk())
setup.run()
