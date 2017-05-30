"""
   File:          DirectoryPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the DirectoryPage
                  which allows the user to go to any page.
"""

import sys

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels

from GUI.AnalysisPage import run_main_page

from GUI.Constants import SMALL_FONT, LARGE_FONT
from GUI.Constants import FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

class DirectoryPage(tk.Frame):
    """
    GUI for the Directory.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        title = ttk.Label(self, text="Directory", font=LARGE_FONT)
        title.grid(sticky="new", padx=BASE_PADDING, pady=BASE_PADDING)
        label = ttk.Label(self, text="Please select a page to continue with the analysis.",
                          font=SMALL_FONT)
        label.grid(sticky="w", padx=BASE_PADDING, pady=BASE_PADDING)
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        group = ttk.LabelFrame(self, text="Pages")
        group.grid(row=2, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        info_button = ttk.Button(group, text="Analysis Information",
                                 command=lambda: controller.show_frame('InfoPage'))
        info_button.grid(row=0, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        cost_button = ttk.Button(group, text="Costs",
                                 command=lambda: controller.show_frame('CostPage'))
        cost_button.grid(row=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ext_button = ttk.Button(group, text="Externalities",
                                command=lambda: controller.show_frame('ExternalitiesPage'))
        ext_button.grid(row=2, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_button = ttk.Button(group, text="Benefits",
                                command=lambda: controller.show_frame('BenefitsPage'))
        ben_button.grid(row=3, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_button = ttk.Button(group, text="Benefits Uncertainties",
                                command=lambda: controller.show_frame('BenefitsUncertaintiesPage'))
        ben_button.grid(row=3, column=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        fat_button = ttk.Button(group, text="Fatalities Averted",
                                command=lambda: controller.show_frame('FatalitiesPage'))
        fat_button.grid(row=4, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        non_d_ben_button = ttk.Button(group, text="Non-Disaster Related Benefits",
                                      command=lambda: controller.show_frame('NonDBensPage'))
        non_d_ben_button.grid(row=5, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        ana_button = ttk.Button(self, text="Show Analysis",
                                command=lambda: run_main_page(self.data_cont))
        ana_button.grid(row=3, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        exit_button = ttk.Button(self, text="Exit", command=sys.exit)
        exit_button.grid(row=3, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
