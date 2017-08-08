"""
   File:          DirectoryPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the DirectoryPage
                  which allows the user to go to any page.
"""

import sys

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels

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
        title = ttk.Label(self, text="Menu", font=LARGE_FONT)
        title.grid(sticky="new", padx=BASE_PADDING, pady=BASE_PADDING)
        label = ttk.Label(self, text="Please select a page to continue with the project.",
                          font=SMALL_FONT)
        label.grid(sticky="w", padx=BASE_PADDING, pady=BASE_PADDING)
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        group = ttk.LabelFrame(self, text="Pages")
        group.grid(row=2, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        info_btn = ttk.Button(group, text="Project Information",
                              command=lambda: controller.show_frame('InfoPage'))
        info_btn.grid(row=0, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        cost_btn = ttk.Button(group, text="Costs",
                              command=lambda: controller.show_frame('CostPage'))
        cost_btn.grid(row=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_btn = ttk.Button(group, text="Costs Uncertainties",
                             command=lambda: controller.show_frame('CostsUncertaintiesPage'))
        ben_btn.grid(row=1, column=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ext_btn = ttk.Button(group, text="Externalities",
                             command=lambda: controller.show_frame('ExternalitiesPage'))
        ext_btn.grid(row=2, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ext_btn = ttk.Button(group, text="Externalities Uncertainties",
                             command=lambda: controller.show_frame('ExternalitiesUncertaintiesPage'))
        ext_btn.grid(row=2, column=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_btn = ttk.Button(group, text="Benefits",
                             command=lambda: controller.show_frame('BenefitsPage'))
        ben_btn.grid(row=3, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_btn = ttk.Button(group, text="Benefits Uncertainties",
                             command=lambda: controller.show_frame('BenefitsUncertaintiesPage'))
        ben_btn.grid(row=3, column=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        fat_btn = ttk.Button(group, text="Fatalities Averted",
                             command=lambda: controller.show_frame('FatalitiesPage'))
        fat_btn.grid(row=4, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        non_d_ben_btn = ttk.Button(group, text="Non-Disaster Related Benefits",
                                   command=lambda: controller.show_frame('NonDBensPage'))
        non_d_ben_btn.grid(row=5, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        non_d_ben_btn = ttk.Button(group, text="Non-Disaster Related Benefits Uncertainties",
                                   command=lambda: controller.show_frame('NonDBensUncertaintiesPage'))
        non_d_ben_btn.grid(row=5, column=1, sticky="ew", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ana_btn = ttk.Button(self, text="Analysis",
                             command=lambda: controller.show_frame('AnalysisInfo'))
        ana_btn.grid(row=3, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        exit_btn = ttk.Button(self, text="Exit", command=sys.exit)
        exit_btn.grid(row=3, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def on_trace_change(self, _name, _index, _mode):
        """ Passes to allow on_trace_change for other pages."""
        pass
