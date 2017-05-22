""" The run file for the Community Resilience Economic Decision Guide.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

import sys

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from Data.ClassSimulation import Simulation

from GUI.BenefitsPage import BenefitsPage
from GUI.BenefitsUncertainties import BenefitsUncertaintiesPage
from GUI.CostPage import CostPage
from GUI.DirectoryPage import DirectoryPage
from GUI.ExternalitiesPage import ExternalitiesPage
from GUI.FatalitiesPage import FatalitiesPage
from GUI.InfoPage import InfoPage
from GUI.NonDBensPage import NonDBensPage

from GUI.Constants import LARGE_FONT
from GUI.Constants import BASE_PADDING

def main():
    """ Runs the full program."""
    app = Application()
    app.mainloop()
class Application(tk.Tk):
    """ Contains the actual application."""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        tk.Tk.wm_title(self, "NIST Economic Resilience Decision Guide")

        # Adds a canvas so that the window will have a scrollbar
        vscrollbar = AutoScrollbar(self.container)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        hscrollbar = AutoScrollbar(self.container, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky="ew")

        canvas = tk.Canvas(self.container,
                           yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")

        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        self.container.grid()
        self.container.grid_rowconfigure(0, weight=1, minsize=930)
        self.container.grid_columnconfigure(0, weight=1, minsize=1500)



        self.frames = {}

        frame = StartPage(canvas, self)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        self.frames[StartPage] = frame
        canvas.create_window(0, 0, anchor="nw", window=frame)
        canvas.config(scrollregion=canvas.bbox("all"))
        frame.grid()


#    def create_widgets(self, frame):
#        """ Creates the opening page. """
#        print('Im being called')


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
        self.create_widgets(parent, controller)

    def create_widgets(self, parent, controller):
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
        self.ok_button = ttk.Button(self, text="OK", command=lambda: self.select(parent, controller)
                                   ).grid(row=3, column=0)
        self.exit_button = ttk.Button(self, text="Exit", command=sys.exit
                                     ).grid(row=4, column=0)

    def select(self, parent, controller):
        """Makes the OK button interact with the two given radio buttons"""
        if self.choice.get() == "new":
            controller.data_cont = Simulation()
            controller.cont_list = [controller.data_cont]

            for page in (DirectoryPage, InfoPage, CostPage, ExternalitiesPage,
                         BenefitsPage, BenefitsUncertaintiesPage, FatalitiesPage, NonDBensPage):
                frame = page(parent, controller, controller.cont_list)
                #parent.create_window(0, 0, anchor="nw", window=frame)
                #parent.config(scrollregion=parent.bbox("all"))
                controller.frames[page] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            # ===== transitions to InfoPage
            controller.show_frame('InfoPage')

        elif self.choice.get() == "open":
            # ======== Select a file for opening:
            filename = filedialog.askopenfilename(title='Choose a .csv file')
            if filename != None and filename[-4:] == ".csv":
                controller.data_cont = Simulation()
                controller.data_cont.file_read(filename)
                controller.cont_list = [controller.data_cont]

                for page in (DirectoryPage, InfoPage, CostPage,
                             ExternalitiesPage, BenefitsPage, BenefitsUncertaintiesPage,
                             FatalitiesPage, NonDBensPage):
                    frame = page(parent, controller, controller.cont_list)
                    #parent.create_window(0, 0, anchor="nw", window=frame)
                    #parent.config(scrollregion=parent.bbox("all"))
                    controller.frames[page] = frame
                    frame.grid()#row=0, column=0, sticky="nsew")

                # === Changes these fields so that the .trace methods are envoked
                # ===  and the respective widgets are altered
                controller.frames[InfoPage].num_plans_ent.insert(tk.END,
                                                                 controller.data_cont.num_plans)
                for i in range(len(controller.data_cont.plan_list)):
                    controller.frames[InfoPage].name_ents[i].delete(0, tk.END)
                    controller.frames[InfoPage].name_ents[i].insert(tk.END,
                                                                    controller.data_cont.plan_list[i].name)

                # ===== Global variables part of infopage
                controller.frames[InfoPage].name_ent.delete(0, tk.END)
                controller.frames[InfoPage].name_ent.insert(tk.END,
                                                            controller.data_cont.title)
                controller.frames[InfoPage].hor_ent.delete(0, tk.END)
                controller.frames[InfoPage].hor_ent.insert(tk.END,
                                                           controller.data_cont.horizon)
                controller.frames[InfoPage].dis_ent.delete(0, tk.END)
                controller.frames[InfoPage].dis_ent.insert(tk.END,
                                                           controller.data_cont.get_discount_rate())
                controller.frames[FatalitiesPage].life_ent.delete(0, tk.END)
                controller.frames[FatalitiesPage].life_ent.insert(tk.END,
                                                                  controller.data_cont.stat_life)
                controller.frames[InfoPage].haz_ent.delete(0, tk.END)
                controller.frames[InfoPage].haz_ent.insert(tk.END,
                                                           controller.data_cont.get_disaster_rate())
                controller.frames[InfoPage].mag_ent.delete(0, tk.END)
                controller.frames[InfoPage].mag_ent.insert(tk.END,
                                                           controller.data_cont.get_disaster_magnitude())
                controller.frames[InfoPage].preference.set(controller.data_cont.risk_pref)

                # ===== Transitions to DirectoryPage
                controller.show_frame('DirectoryPage')
            else:
                print("ERR: Not a .csv file")
        else:
            return

class AutoScrollbar(tk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed.
     Only works if you use the grid geometry manager!"""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
    def pack(self, **_kw):
        """ I don't know what this does. """
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **_kw):
        """ I don't know what this does. """
        raise tk.TclError("cannot use place with this widget")

# Directory Page
# Info Page
# Costs Page
# Externalities Page
# Benefits Page
# Fatalities Page
# NonDBens Page

# ===== Runs the actual program
main()
