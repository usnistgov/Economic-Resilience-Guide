"""
   File:          EconGuide.py
   Author:        Shannon Grubb (shannon.grubb@nist.gov),
                  Edward Hanson (ehanson1@umbc.edu)
   Description:   Starts up the application
"""

import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from Data.ClassSimulation import Simulation

from GUI.InfoPage import InfoPage
from GUI.DirectoryPage import DirectoryPage
from GUI.CostPage import CostPage
from GUI.CostsUncertainties import CostsUncertaintiesPage
from GUI.ExternalitiesPage import ExternalitiesPage
from GUI.ExternalitiesUncertainties import ExternalitiesUncertaintiesPage
from GUI.BenefitsPage import BenefitsPage
from GUI.BenefitsUncertainties import BenefitsUncertaintiesPage
from GUI.FatalitiesPage import FatalitiesPage
from GUI.NonDBensPage import NonDBensPage
from GUI.NonDBensUncertainties import NonDBensUncertaintiesPage
from GUI.AnalysisInfo import AnalysisInfo

from GUI.Constants import LARGE_FONT
from GUI.Constants import BASE_PADDING

from VertScroll import VerticalScrolledFrame

class Application(tk.Tk):
    """ Contains the actual application."""
    def __init__(self, *args, **kwargs):
        #args = arguments, kwargs = key word args
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = VerticalScrolledFrame(self)

        self.container.grid(sticky="nsew")

        tk.Tk.wm_title(self, "NIST Economic Decision Guide")

        self.container.grid_rowconfigure(0, weight=1, minsize=50)
        self.container.grid_columnconfigure(0, weight=1, minsize=50)

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
                      'CostPage': CostPage,
                      'CostsUncertaintiesPage': CostsUncertaintiesPage,
                      'ExternalitiesPage': ExternalitiesPage,
                      'ExternalitiesUncertaintiesPage': ExternalitiesUncertaintiesPage,
                      'BenefitsPage': BenefitsPage,
                      'BenefitsUncertaintiesPage': BenefitsUncertaintiesPage,
                      'FatalitiesPage': FatalitiesPage,
                      'NonDBensPage': NonDBensPage,
                      'NonDBensUncertaintiesPage': NonDBensUncertaintiesPage,
                      'AnalysisInfo': AnalysisInfo}
        cont = frame_dict[cont_string]
        frame = self.frames[cont]
        frame.on_trace_change("", "","")
        self.container.canvas.xview_moveto(0)
        self.container.canvas.yview_moveto(0)
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

        photo = tk.PhotoImage(file="CR_Logo.png")
        photo = photo.subsample(4, 4)
        #photo = tk.PhotoImage(file="el_logo_small.gif")
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

        tk.Label(self, text="").grid(row=5)

        photo = tk.PhotoImage(file="nistident_fleft_300ppi.png")
        photo = photo.subsample(3, 3)
        pic = ttk.Label(self, image=photo)
        pic.image = photo
        pic.grid(row=6, sticky="sw")

    def select(self, controller):
        """Makes the OK button interact with the two given radio buttons"""
        if self.choice.get() == "new":
            controller.data_cont = Simulation()
            controller.cont_list = [controller.data_cont]

            for page in (DirectoryPage, InfoPage, CostPage, CostsUncertaintiesPage,
                         ExternalitiesPage, ExternalitiesUncertaintiesPage,
                         BenefitsPage, BenefitsUncertaintiesPage,
                         FatalitiesPage, NonDBensPage,
                         NonDBensUncertaintiesPage, AnalysisInfo):
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
                for page in (DirectoryPage, InfoPage, CostPage, CostsUncertaintiesPage,
                             ExternalitiesPage, ExternalitiesUncertaintiesPage,
                             BenefitsPage, BenefitsUncertaintiesPage,
                             FatalitiesPage, NonDBensPage,
                             NonDBensUncertaintiesPage, AnalysisInfo):
                    frame = page(controller.container.interior, controller, controller.cont_list)
                    controller.frames[page] = frame
                    frame.grid(row=0, column=0, sticky="nsew")

                # === Changes these fields so that the .trace methods are envoked
                # ===  and the respective widgets are altered
                controller.frames[InfoPage].num_plans_ent.insert(tk.END,
                                                                 controller.data_cont.num_plans-1)
                for i in range(1, controller.data_cont.num_plans):
                    controller.frames[InfoPage].name_ents[i-1].delete(0, tk.END)
                    name = controller.data_cont.plan_list[i].name
                    controller.frames[InfoPage].name_ents[i-1].insert(tk.END, name)

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
                for entry in page.recur_range:
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, controller.data_cont.plan_list[0].recurr_range[page.recur_range.index(entry)])
                for entry in page.mag_range:
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, controller.data_cont.plan_list[0].mag_range[page.mag_range.index(entry)])

                page.recur_choice.set(controller.data_cont.plan_list[0].recurr_dist)

                page.mag_choice.set(controller.data_cont.plan_list[0].mag_dist)

                page.preference.set(controller.data_cont.risk_pref)

                # ===== Transitions to DirectoryPage
                controller.show_frame('DirectoryPage')
            else:
                print("ERR: Not a .csv file")
        else:
            return
    
    def on_trace_change(self, _name, _index, _mode):
        """ Passes to allow on_trace_change of other pages."""
        pass


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
