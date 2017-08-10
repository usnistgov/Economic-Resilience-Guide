"""
   File:          Histograms.py
   Author:        Shannon Grubb
   Description:   Interacts with EconGuide.py, builds the GUI for adding uncertainties
                  to externalities, the page for the user to input Externalities
                  uncertainty distributions.
"""

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.PlotsAndImages import histogram

from GUI.Constants import SMALL_FONT, LARGE_FONT
from GUI.Constants import FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

matplotlib.use("TkAgg")


#
#
################################### Externalities Uncertainties ###################################
#
#
class HistogramPage(tk.Frame):
    """
    GUI for the input of all Externalities Uncertainties.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="There is often uncertainty surrounding the exact "
                                     "externalities.\nThe externalities associated with each "
                                     "alternative are listed below. The type of externality and "
                                     "the dollar amount associated with the externality is "
                                     "indicated.\nFor each externality, please select the "
                                     "associated uncertainty description. Each type of "
                                     "uncertainty distribution requires key information.\n"
                                     "Please provide this information in the boxes below the "
                                     "distribution type you select.\nFurther information is "
                                     "available in the “More Information” section for this page.\n"
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ext_lbl = tk.Label(self, text="Externalities Uncertainties", font=LARGE_FONT)
        ext_lbl.grid(row=2, sticky="w")
        self.direct_range = []
        self.indirect_range = []
        self.res_rec_range = []
        self.groups = []
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Uncertainty selection Widgets

        self.on_trace_change("name", "index", "mode")

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'BenefitsPage'
            moveon = True
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'ExternalitiesPage'
            moveon = True
            if moveon:
                controller.show_frame(go_to_place)

        def menu():
            """ Tries to save the input and sends the user to the Directory Page.
            If save unsuccessful, asks user for verification to move on."""
            go_to_place = 'DirectoryPage'
            moveon = True
            if moveon:
                controller.show_frame(go_to_place)



        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=self.data_cont.file_save)
        save_button.grid(row=1, column=0, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=13, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=13, column=0, sticky="se",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Menu",
                   command=menu).grid(row=13, column=0, padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def show_info(self):
        """ Pulls up information for the Externalities page."""
        messagebox.showinfo("More Information",
                            "Page under construction")

    def on_trace_change(self, _name, _index, _mode):
        """Updates the number of plans with options dependent on number of externalities input."""
        for group in self.groups:
            group.grid_forget()
            group.destroy()
        self.groups = []
        for plan in self.data_cont.plan_list:
            self.groups.append(ttk.LabelFrame(self, text=plan.name))
            self.groups[-1].grid(row=4+plan.num, sticky="ew",
                                 padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            fig_label = ttk.Label(self.groups[-1])
            fig_label.grid(row=1, column=plan.num+1)
            try:
                fig = histogram(plan.net_ext_totals)
            except AttributeError:
                fig = histogram([0])
            canvas = FigureCanvasTkAgg(fig, master=fig_label)
            canvas.get_tk_widget().grid(row=1, column=plan.num+1)
            canvas.show()
