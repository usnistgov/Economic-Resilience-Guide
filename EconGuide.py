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


#from Calculations import Data
from Data.ClassSimulation import Simulation

from GUI.InfoPage import InfoPage
from GUI.DirectoryPage import DirectoryPage
from GUI.CostPage import CostPage
from GUI.ExternalitiesPage import ExternalitiesPage
from GUI.BenefitsPage import BenefitsPage
from GUI.BenefitsUncertainties import BenefitsUncertaintiesPage
from GUI.FatalitiesPage import FatalitiesPage
from GUI.NonDBensPage import NonDBensPage

from VertScroll import VerticalScrolledFrame

from GUI.Constants import LARGE_FONT
from GUI.Constants import BASE_PADDING

class Application(tk.Tk):
    """ Contains the actual application."""
    def __init__(self, *args, **kwargs):
        #args = arguments, kwargs = key word args

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = VerticalScrolledFrame(self)

        self.container.grid(sticky="nsew")

        tk.Tk.wm_title(self, "NIST Economic Decision Guide")

        self.container.grid_rowconfigure(0, weight=1, minsize=700)
        self.container.grid_columnconfigure(0, weight=1, minsize=1000)

        self.frames = {}

        # ====== A list of all pages (classes) used in this program.
        # ====== Makes it possible to transition between each
        frame = StartPage(self.container.interior, self)
        self.frames[StartPage] = frame
        frame.grid()

        # ====== Has any text boxes select all when clicked on for ease of entering new information
        self.bind_class("Text", "<FocusIn>", self.selectall)

        self.show_frame('StartPage')

    def show_frame(self, cont_string):
        """ Brings to the forefront the frame described by cont_string."""
        frame_dict = {'StartPage': StartPage, 'DirectoryPage': DirectoryPage, 'InfoPage': InfoPage,
                      'CostPage': CostPage, 'ExternalitiesPage': ExternalitiesPage,
                      'BenefitsPage': BenefitsPage,
                      'BenefitsUncertaintiesPage': BenefitsUncertaintiesPage,
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
            controller.data_cont = Simulation()
            controller.cont_list = [controller.data_cont]

            for page in (DirectoryPage, InfoPage, CostPage, ExternalitiesPage,
                         BenefitsPage, BenefitsUncertaintiesPage,
                         FatalitiesPage, NonDBensPage):
                frame = page(controller.container.interior, controller, controller.cont_list)
                controller.frames[page] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            # ===== transitions to InfoPage
            controller.show_frame('InfoPage')
        elif self.choice.get() == "open":
            # ======== Select a file for opening:
            filename = filedialog.askopenfilename(title='Choose a .csv file')
            if filename != None and filename[-4:] == ".csv":
                controller.data_cont = Simulation()
                controller.data_cont.file_read(file_name=filename)
                controller.cont_list = [controller.data_cont]
                for page in (DirectoryPage, InfoPage, CostPage,
                             ExternalitiesPage, BenefitsPage, BenefitsUncertaintiesPage,
                             FatalitiesPage, NonDBensPage):
                    frame = page(controller.container.interior, controller, controller.cont_list)
                    controller.frames[page] = frame
                    frame.grid(row=0, column=0, sticky="nsew")

                # === Changes these fields so that the .trace methods are envoked
                # ===  and the respective widgets are altered
                controller.frames[InfoPage].num_plans_ent.insert(tk.END,
                                                                 controller.data_cont.num_plans-1)
                for i in range(1, controller.data_cont.num_plans):
                    controller.frames[InfoPage].name_ents[i-1].delete(0, tk.END)
                    controller.frames[InfoPage].name_ents[i-1].insert(tk.END,
                                                                      controller.data_cont.plan_list[i].name)

                # ===== Global variables part of infopage
                page = controller.frames[InfoPage]
                page.name_ent.delete(0, tk.END)
                page.name_ent.insert(tk.END, controller.data_cont.title)
                page.hor_ent.delete(0, tk.END)
                page.hor_ent.insert(tk.END, controller.data_cont.horizon)
                page.dis_ent.delete(0, tk.END)
                page.dis_ent.insert(tk.END, controller.data_cont.discount_rate)
                controller.frames[FatalitiesPage].life_ent.delete(0, tk.END)
                controller.frames[FatalitiesPage].life_ent.insert(tk.END,
                                                                  controller.data_cont.stat_life)
                page.haz_ent.delete(0, tk.END)
                page.haz_ent.insert(tk.END, controller.data_cont.get_disaster_rate()[0])

                page.recur_range.delete(0, tk.END)
                page.recur_range.insert(tk.END, controller.data_cont.get_disaster_rate()[1])

                page.recur_choice.set(controller.data_cont.get_disaster_rate()[2])

                page.mag_ent.delete(0, tk.END)
                page.mag_ent.insert(tk.END, controller.data_cont.get_disaster_magnitude()[0])

                page.mag_range.delete(0, tk.END)
                page.mag_range.insert(tk.END, controller.data_cont.get_disaster_magnitude()[1])

                page.mag_choice.set(controller.data_cont.get_disaster_magnitude()[2])

                page.preference.set(controller.data_cont.risk_pref)

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
