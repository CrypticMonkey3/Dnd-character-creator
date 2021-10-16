from tkinter import *
from tkinter import ttk
import tkinter.font as font
import os.path
counter = 0
while counter != 1:  # looped so that if we did need to install something, we can import that module.
    try:
        from selenium import webdriver
        from pygeckodriver import geckodriver_path
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import *
        counter += 1
    except ModuleNotFoundError:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygeckodriver"])
        # subprocess.check_call() runs the arguments from within and waits for it to be complete.
        # sys.executable retrieves the path to where the instruction should be executed, in this case our python
        # environment.
        # So, it runs and installs selenium and the pygeckodriver onto the current python environment.

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
        try:
            self.driver.close()
        except AttributeError:
            pass
        except WebDriverException:  # if there was no response from the headless connection.
            pass


class SetupGUI:
    def __init__(self, root):
        self.scraper = WebScraper("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/93.0")
        self.option = StringVar()
        self.title_message = "Dnd Startup"

        # Basic root stuff
        self.root = root
        self.root.title(self.title_message)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)  # users can't resize the window

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
        self.error_message = ttk.Label(self.mainframe, text="Connection was interrupted")
        self.download_message = ttk.Label(self.mainframe, text="File(s) download successful")

        # setting any radiobuttons
        self.gui_version = ttk.Radiobutton(self.mainframe, text="GUI version", variable=self.option, value="GUI")
        self.text_version = ttk.Radiobutton(self.mainframe, text="Text-based version (unavailable)",
                                            variable=self.option, value="TEXT")

        # setting up any buttons.
        self.download_button = ttk.Button(self.mainframe, text="Download")

    def dispatcher(self, event: str) -> None:
        """
        Handles all user input/ events
        :param str event: The event
        :return: None
        """
        if event == "DOWNLOAD" and self.option.get() == "GUI":
            try:
                # tries to remove the old versions of the file
                os.remove(fr"C:\Users\{os.listdir('C://Users')[-1]}\Downloads\Dnd-character-creator-main.zip")
            except FileNotFoundError:
                pass

            try:
                self.scraper.remote_web_for("https://github.com/CrypticMonkey3/Dnd-character-creator")
                self.scraper.click_button("//summary[normalize-space()='Code']")
                # clicks the 'Code' button.
                # normalize-space() trims the left and right side of the text of any whitespaces.
                # so we are finding the text: 'summary' that says 'Code', which will then be clicked.
                self.scraper.click_button("//a[normalize-space()='Download ZIP']")
                self.scraper.wait(7)
                self.scraper.close()
                self.download_message.grid(column=1, row=0, sticky=(N, E), pady=260)

            except WebDriverException:  # if the driver was never able to load, due to lack of Internet connection.
                self.scraper.close()
                self.error_message.grid(column=1, row=0, sticky=(N, E), pady=260)

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
