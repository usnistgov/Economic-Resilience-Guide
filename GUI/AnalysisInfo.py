"""
   File:          AnalysisInfo.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the AnalysisInfo page
                  which allows the user to select how they want to interact with their analysis.
"""

import sys
import random

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels
from tkinter import messagebox

from GUI.AnalysisPage import run_main_page
from GUI.AnalysisUncertainties import run_u_main_page

from GUI.Constants import SMALL_FONT, LARGE_FONT, ENTRY_WIDTH
from GUI.Constants import FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

class AnalysisInfo(tk.Frame):
    """
    GUI for the Directory.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        title = ttk.Label(self, text="Analysis Information", font=LARGE_FONT)
        title.grid(sticky="new", padx=BASE_PADDING, pady=BASE_PADDING)
        label = ttk.Label(self, text="Please select how you want to view your analysis.",
                          font=SMALL_FONT)
        label.grid(sticky="w", padx=BASE_PADDING, pady=BASE_PADDING)
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """

        # With or without uncertainty group
        choice_group = ttk.LabelFrame(self, text="With or without uncertainty?")
        choice_group.grid(row=2, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        self.uncert_select = tk.StringVar()
        self.uncert_select.set("1")
        point_rad = ttk.Radiobutton(choice_group, text="Point estimate calculations",
                                    variable=self.uncert_select, value="point")
        point_rad.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        uncert_rad = ttk.Radiobutton(choice_group, text="Uncertainty calculations",
                                     variable=self.uncert_select, value="uncert")
        uncert_rad.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # Analysis choices group
        button_group = ttk.LabelFrame(self, text="What would you like to do with your analysis?")
        button_group.grid(row=3, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        analysis_button = ttk.Button(button_group, text="View Analysis",
                                     command=lambda: self.view(self.uncert_select.get()))
        analysis_button.grid(row=0, columnspan=3, sticky="ew",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        docx_button = ttk.Button(button_group, text="Export as .docx",
                                 command=lambda: self.document)
        docx_button.grid(row=1, column=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        docx_button.grid_columnconfigure(0, weight=1)
        csv_button = ttk.Button(button_group, text="Export as .csv",
                                command=lambda: self.commas(self.uncert_select.get()))
        csv_button.grid(row=1, column=1, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        csv_button.grid_columnconfigure(1, weight=1)
        both_button = ttk.Button(button_group, text="Export using both formats",
                                 command=lambda: self.both(self.uncert_select.get()))
        both_button.grid(row=1, column=2, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        both_button.grid_columnconfigure(2, weight=1)

        # Uncertainty Information Group
        uncert_group = ttk.LabelFrame(self, text="Information on Monte-Carlo calculations")
        uncert_group.grid(row=4, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        ttk.Label(uncert_group, text="Seed",
                  font=SMALL_FONT).grid(row=0, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.seed_ent = tk.Entry(uncert_group, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.seed_ent.insert(tk.END, str(random.randrange(sys.maxsize)))
        self.seed_ent.grid(row=0, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Label(uncert_group, text="Confidence Interval",
                  font=SMALL_FONT).grid(row=1, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.conf_ent = tk.Entry(uncert_group, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.conf_ent.insert(tk.END, '95')
        self.conf_ent.grid(row=1, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Label(uncert_group, text="%",
                  font=SMALL_FONT).grid(row=1, column=2, sticky="w",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Label(uncert_group, text="Monte Carlo Bounds Tolerance",
                  font=SMALL_FONT).grid(row=2, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.tol_ent = tk.Entry(uncert_group, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.tol_ent.insert(tk.END, '0.1')
        self.tol_ent.grid(row=2, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Label(uncert_group, text="% of point estimate",
                  font=SMALL_FONT).grid(row=2, column=2, sticky="w",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Label(uncert_group, text="Maximum number of runs",
                  font=SMALL_FONT).grid(row=3, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.max_ent = tk.Entry(uncert_group, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.max_ent.insert(tk.END, '102400')
        self.max_ent.grid(row=3, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # Changes presence of uncertainty choices based on whether or not uncertainty is selected
        # For now deemed unnecessary since the page is fairly clean with choices
        #self.uncert_select.trace("w", self.on_trace_change)

        # Return to menu
        menu_button = ttk.Button(self, text="View Directory",
                                 command=lambda: controller.show_frame('DirectoryPage'))
        menu_button.grid(row=5, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def view(self, uncert):
        """ Views the appropriate analysis page."""
        self.data_cont.summer()
        if uncert == "point":
            run_main_page(self.data_cont)
        elif uncert == "uncert":
            try:
                seed = int(self.seed_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Input seed must be an integer value.")
            try:
                conf = float(self.conf_ent.get())
                assert 0 < conf <= 100
            except ValueError:
                messagebox.showerror("Error", "Confidence must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Confidence must be a positive number less than or equal to 100%.")
            try:
                tol = float(self.tol_ent.get())
                assert 0 < tol <= 100
            except ValueError:
                messagebox.showerror("Error", "Tolerance must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Tolerance must be a positive number less than or equal to 100%.")
            try:
                break_point = int(self.max_ent.get())
            except ValueError:
                messagebox.showerror("Error", "The maximum number of iterations must be an integer value.")            
            self.data_cont.monte(seed, conf, tol, high_iters=break_point)
            run_u_main_page(self.data_cont)
        else:
            messagebox.showerror("Error", "You must select whether to use uncertainty inputs in your analysis.")

    def document(self, uncert):
        """Calls docx export."""
        self.data_cont.summer()
        if uncert == "point":
            self.data_cont.word_export()
        elif uncert == "uncert":
            try:
                seed = int(self.seed_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Input seed must be an integer value.")
            try:
                conf = float(self.conf_ent.get())
                assert 0 < conf <= 100
            except ValueError:
                messagebox.showerror("Error", "Confidence must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Confidence must be a positive number less than or equal to 100%.")
            try:
                tol = float(self.tol_ent.get())
                assert 0 < tol <= 100
            except ValueError:
                messagebox.showerror("Error", "Tolerance must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Tolerance must be a positive number less than or equal to 100%.")
            try:
                break_point = int(self.max_ent.get())
            except ValueError:
                messagebox.showerror("Error", "The maximum number of iterations must be an integer value.")
            self.data_cont.monte(seed, conf, tol, max_iters=break_point)
            self.data_cont.word_export_uncert()
        else:
            messagebox.showerror("Error", "You must select whether to use uncertainty inputs in your analysis.")

    def commas(self, uncert):
        """Calls csv export."""
        self.data_cont.summer()
        if uncert == "point":
            self.data_cont.csv_export()
        elif uncert == "uncert":
            try:
                seed = int(self.seed_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Input seed must be an integer value.")
            try:
                conf = float(self.conf_ent.get())
                assert 0 < conf <= 100
            except ValueError:
                messagebox.showerror("Error", "Confidence must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Confidence must be a positive number less than or equal to 100%.")
            try:
                tol = float(self.tol_ent.get())
                assert 0 < tol <= 100
            except ValueError:
                messagebox.showerror("Error", "Tolerance must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Tolerance must be a positive number less than or equal to 100%.")
            try:
                break_point = int(self.max_ent.get())
            except ValueError:
                messagebox.showerror("Error", "The maximum number of iterations must be an integer value.")
            messagebox.showinfo("Please be patient", "The Monte-Carlo simulations will take some time to run. Please be patient while they compute.")
            self.data_cont.monte(seed, conf, tol, high_iters=break_point)
            self.data_cont.csv_export_uncert()
        else:
            messagebox.showerror("Error", "You must select whether to use uncertainty inputs in your analysis.")

    def both(self, uncert):
        """Calls docx and csv export."""
        self.data_cont.summer()
        if uncert == "point":
            self.data_cont.word_export()
            self.data_cont.csv_export()
        elif uncert == "uncert":
            try:
                seed = int(self.seed_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Input seed must be an integer value.")
            try:
                conf = float(self.conf_ent.get())
                assert 0 < conf <= 100
            except ValueError:
                messagebox.showerror("Error", "Confidence must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Confidence must be a positive number less than or equal to 100%.")
            try:
                tol = float(self.tol_ent.get())
                assert 0 < tol <= 100
            except ValueError:
                messagebox.showerror("Error", "Tolerance must be a number.")
            except AssertionError:
                messagebox.showerror("Error", "Tolerance must be a positive number less than or equal to 100%.")
            try:
                break_point = int(self.max_ent.get())
            except ValueError:
                messagebox.showerror("Error", "The maximum number of iterations must be an integer value.")
            self.data_cont.monte(seed, conf, tol, high_iters=break_point)
            self.data_cont.word_export_uncert()
            self.data_cont.csv_export_uncert()
        else:
            messagebox.showerror("Error", "You must select whether to use uncertainty inputs in your analysis.")


    def on_trace_change(self, _name, _index, _mode):
        """ Passes to allow on_trace_change for other pages."""
        pass