"""
   File:          EconGuide.py
   Author:        Shannon Craig,
                  Edward Hanson (ehanson1@umbc.edu)
   Description:   Interacts with Calculations.py,
                  Focusing on the GUI for user-friendly resilience calculations.
"""

import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk     #for pretty buttons/labels


from Calculations import Data

from InfoPage import InfoPage
from DirectoryPage import DirectoryPage
from CostPage import CostPage
from ExternalitiesPage import ExternalitiesPage
from BenefitsPage import BenefitsPage
from BenefitsUncertainties import BenefitsUncertaintiesPage
from FatalitiesPage import FatalitiesPage
from NonDBensPage import NonDBensPage

from VertScroll import VerticalScrolledFrame

from Constants import LARGE_FONT
from Constants import BASE_PADDING

class Application(tk.Tk):
    """ Contains the actual application."""
    def __init__(self, *args, **kwargs):
        #args = arguments, kwargs = key word args

        tk.Tk.__init__(self, *args, **kwargs)
        #self.container = tk.Frame(self)
        #self.container = ScrolledWindow(self)
        #self.container.master.maxsize(height=600)
        self.container = VerticalScrolledFrame(self)#.interior

        self.container.grid(sticky="nsew")

        tk.Tk.wm_title(self, "NIST Economic Decision Guide")

        #self.container.grid()

        #self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1, minsize=700)
        #self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1, minsize=1000)

        self.frames = {}

        # ====== A list of all pages (classes) used in this program.
        # ====== Makes it possible to transition between each
        frame = StartPage(self.container.interior, self)
        self.frames[StartPage] = frame
        frame.grid()
#        frame.grid(row=0, column=0, stick="nsew")

        # ====== Has any text boxes select all when clicked on for ease of entering new information
        self.bind_class("Text", "<FocusIn>", self.selectall)
        #self.bind_class("Entry", "<FocusIn>", self.selectall)

        self.show_frame('StartPage')

    def show_frame(self, cont_string):
        """ Brings to the forefront the frame described by cont_string."""
        frame_dict = {'StartPage': StartPage, 'DirectoryPage': DirectoryPage, 'InfoPage': InfoPage,
                      'CostPage': CostPage, 'ExternalitiesPage': ExternalitiesPage,
                      'BenefitsPage': BenefitsPage, 'BenefitsUncertaintiesPage': BenefitsUncertaintiesPage,
                      'FatalitiesPage': FatalitiesPage,
                      'NonDBensPage': NonDBensPage}
        cont = frame_dict[cont_string]
        frame = self.frames[cont]
        frame.tkraise()

    def selectall(self, event):
        """ Selects all items in the widget."""
        event.widget.tag_add(tk.SEL, "1.0", tk.END)

class StartPage(tk.Frame):
    """Prompts the user to either open a file or start a new analysis"""
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Welcome to the NIST Economic Decision Guide Tool",
                          font=LARGE_FONT)
        label.grid(pady=BASE_PADDING, padx=BASE_PADDING)  # places padding for neatness
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """Widgets include: radio buttons, confirmation buttons, and Labels"""

        photo = tk.PhotoImage(file="el_logo_small.gif")
        pic = ttk.Label(self, image=photo)
        pic.image = photo
        pic.grid(row=2, sticky="w")

        self.choice = tk.StringVar()
        self.choice.set("1")  # makes so that radio buttons aren't chosen yet
        tk.Radiobutton(self, text="Start new analysis", variable=self.choice, value="new"
                      ).grid(row=3, column=0, sticky='W')
        tk.Radiobutton(self, text="Open existing analysis", variable=self.choice, value="open"
                      ).grid(row=4, column=0, sticky='W')
        self.ok_button = ttk.Button(self, text="OK", command=lambda: self.select(controller)
                                   ).grid(row=3, column=0)
        self.exit_button = ttk.Button(self, text="Exit", command=sys.exit
                                     ).grid(row=4, column=0)

    def select(self, controller):
        """Makes the OK button interact with the two given radio buttons"""
        if self.choice.get() == "new":
            controller.data_cont = Data()
            controller.cont_list = [controller.data_cont]

            for page in (DirectoryPage, InfoPage, CostPage, ExternalitiesPage,
                         BenefitsPage, BenefitsUncertaintiesPage, FatalitiesPage, NonDBensPage):
                frame = page(controller.container.interior, controller, controller.cont_list)
                controller.frames[page] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            # ===== transitions to InfoPage
            controller.show_frame('InfoPage')
        elif self.choice.get() == "open":
            # ======== Select a file for opening:
            filename = filedialog.askopenfilename(title='Choose a .csv file')
            if filename != None and filename[-4:] == ".csv":
                controller.data_cont = Data(file_name=filename)
                controller.cont_list = [controller.data_cont]
                for page in (DirectoryPage, InfoPage, CostPage,
                             ExternalitiesPage, BenefitsPage, FatalitiesPage, NonDBensPage):
                    frame = page(controller.container.interior, controller, controller.cont_list)
                    controller.frames[page] = frame
                    frame.grid(row=0, column=0, sticky="nsew")

                # === Changes these fields so that the .trace methods are envoked
                # ===  and the respective widgets are altered
                controller.frames[InfoPage].num_plans_ent.insert(tk.END,
                                                                 controller.data_cont.num_plans)
                if controller.data_cont.num_plans > 0:
                    controller.frames[InfoPage].name_1_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_1_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[1])
                if controller.data_cont.num_plans > 1:
                    controller.frames[InfoPage].name_2_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_2_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[2])
                if controller.data_cont.num_plans > 2:
                    controller.frames[InfoPage].name_3_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_3_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[3])
                if controller.data_cont.num_plans > 3:
                    controller.frames[InfoPage].name_4_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_4_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[4])
                if controller.data_cont.num_plans > 4:
                    controller.frames[InfoPage].name_5_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_5_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[5])
                if controller.data_cont.num_plans > 5:
                    controller.frames[InfoPage].name_6_ent.delete(0, tk.END)
                    controller.frames[InfoPage].name_6_ent.insert(tk.END,
                                                                  controller.data_cont.plan_name[6])

                # ===== Global variables part of infopage
                controller.frames[InfoPage].name_ent.delete(0, tk.END)
                controller.frames[InfoPage].name_ent.insert(tk.END,
                                                            controller.data_cont.analysis_title)
                controller.frames[InfoPage].hor_ent.delete(0, tk.END)
                controller.frames[InfoPage].hor_ent.insert(tk.END,
                                                           controller.data_cont.horizon)
                controller.frames[InfoPage].dis_ent.delete(0, tk.END)
                controller.frames[InfoPage].dis_ent.insert(tk.END,
                                                           controller.data_cont.discount_rate)
                controller.frames[FatalitiesPage].life_ent.delete(0, tk.END)
                controller.frames[FatalitiesPage].life_ent.insert(tk.END,
                                                                  controller.data_cont.stat_life)
                controller.frames[InfoPage].haz_ent.delete(0, tk.END)
                controller.frames[InfoPage].haz_ent.insert(tk.END,
                                                           controller.data_cont.disaster_rate)
                controller.frames[InfoPage].mag_ent.delete(0, tk.END)
                controller.frames[InfoPage].mag_ent.insert(tk.END,
                                                           controller.data_cont.dis_magnitude)
                controller.frames[InfoPage].preference.set(controller.data_cont.risk_preference)

                # ===== Transitions to DirectoryPage
                controller.show_frame('DirectoryPage')
            else:
                print("ERR: Not a .csv file")
        else:
            return


# Directory Page
# Info Page
# Costs Page
# Externalities Page
# Benefits Page
# Fatalities Page
# NonDBens Page

# ===== Runs the actual program
APP = Application()
APP.mainloop()
