"""
   File:          InfoPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the InfoPage,
                  the first page the user will input data on.
"""

import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.Constants import SMALL_FONT, ENTRY_WIDTH
from GUI.Constants import BASE_PADDING, FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING

from GUI.PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist

from Data.ClassSimulation import Plan

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

matplotlib.use("TkAgg")

#
#
###################################### Base Information Class ######################################
############################################# InfoPage #############################################
#
#

class InfoPage(tk.Frame):
    """ Allows the user to input the basic information about their options."""
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Input the project name, the list of alternatives, "
                                    "the planning horizon,the calculated\n"
                                    "nominal discount rate for discounting future costs to "
                                    "present values, and hazard specifics.", font=SMALL_FONT)

        label.grid(pady=BASE_PADDING, padx=BASE_PADDING)

        self.traces = [tk.StringVar() for i in range(6)]
        #self.p1_trace = tk.StringVar()
        #self.p2_trace = tk.StringVar()
        #self.p3_trace = tk.StringVar()
        #self.p4_trace = tk.StringVar()
        #self.p5_trace = tk.StringVar()
        #self.p6_trace = tk.StringVar()

        self.choice_var = tk.StringVar()

        self.create_widgets(controller)

    def create_widgets(self, controller):
        """Widgets include: buttons, text boxes, and labels"""

        group0 = ttk.LabelFrame(self)
        group0.grid(row=0, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        new_label = ttk.Label(group0, text="Input the project name, the list of alternatives, "
                                           "the planning horizon,the calculated\n"
                                           "nominal discount rate for discounting future costs to "
                                           "present values, and hazard specifics.", font=SMALL_FONT)
        new_label.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        info_button = ttk.Button(group0, text="More Information", command=self.show_info)
        info_button.grid(row=1, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Project Description Specifics
        group1 = ttk.LabelFrame(self, text="Project Description")
        group1.grid(row=2, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        name_lbl = ttk.Label(group1, text="Name", font=SMALL_FONT)
        name_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.name_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.name_ent.insert(tk.END, "<enter project name>")
        self.name_ent.grid(row=0, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        hor_lbl = ttk.Label(group1, text="Planning Horizon", font=SMALL_FONT)
        hor_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.hor_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.hor_ent.insert(tk.END, "<enter number of years for analysis>")
        self.hor_ent.grid(row=1, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Project Alternatives Names
        group2 = ttk.LabelFrame(self, text="Project Alternatives")
        group2.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        self.choices = [1, 2, 3, 4, 5, 6]
        num_plans_lbl = ttk.Label(group2, text="Number of Alternative Plans", font=SMALL_FONT)
        num_plans_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.num_plans_ent = ttk.Combobox(group2, textvariable=self.choice_var, font=SMALL_FONT,
                                          width=ENTRY_WIDTH, values=self.choices)
        self.num_plans_ent.insert(tk.END, 0)
        self.num_plans_ent.grid(row=0, column=1, sticky="e",
                                padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.choice_var.trace("w", self.on_trace_choice)
        # ^ Updates other widgets when this field is updated

        base_lbl = ttk.Label(group2, text="Base scenario", font=SMALL_FONT)
        base_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        base_2_lbl = ttk.Label(group2, text="---------------------------------------------------",
                               font=SMALL_FONT)
        base_2_lbl.grid(row=1, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.name_lbls = [ttk.Label(group2, text="Alternative 1", font=SMALL_FONT),
                          ttk.Label(group2, text="Alternative 2", font=SMALL_FONT),
                          ttk.Label(group2, text="Alternative 3", font=SMALL_FONT),
                          ttk.Label(group2, text="Alternative 4", font=SMALL_FONT),
                          ttk.Label(group2, text="Alternative 5", font=SMALL_FONT),
                          ttk.Label(group2, text="Alternative 6", font=SMALL_FONT)]
        for lbl in self.name_lbls:
            my_row = self.name_lbls.index(lbl) + 2
            lbl.grid(row=my_row, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            lbl.configure(state="disabled")
        self.name_ents = [tk.Entry(group2, textvariable=self.traces[i],
                                   width=ENTRY_WIDTH, font=SMALL_FONT) for i in range(6)]
        for ent in self.name_ents:
            my_row = self.name_ents.index(ent) + 2
            ent.insert(tk.END, "<enter plan name>")
            ent.grid(row=my_row, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            ent.configure(state="disabled")

        # ===== Discount Rate and Hazard Specifics
        group3 = ttk.LabelFrame(self, text="Discount Rate/Hazard Specifics")
        group3.grid(row=4, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        dis_lbl = ttk.Label(group3, text="Nominal Discount Rate", font=SMALL_FONT)
        dis_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.dis_ent = tk.Entry(group3, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.dis_ent.insert(tk.END, "5.00")
        self.dis_ent.grid(row=0, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        percent_lbl = ttk.Label(group3, text="%", font=SMALL_FONT)
        percent_lbl.grid(row=0, column=2, sticky='w', pady=FIELDY_PADDING)

        def_button = ttk.Button(group3, text="Restore Default", command=self.restore)
        def_button.grid(row=2, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        sep1 = ttk.Separator(group3, orient=tk.HORIZONTAL)
        sep1.grid(row=3, sticky="ew", columnspan=90, padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        haz_lbl = ttk.Label(group3, text="Hazard Recurrence", font=SMALL_FONT)
        haz_lbl.grid(row=4, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.haz_ent = tk.Entry(group3, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.haz_ent.insert(tk.END, "<expected # of years between each incident>")
        self.haz_ent.grid(row=4, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        yrs_lbl = ttk.Label(group3, text="Year(s)", font=SMALL_FONT)
        yrs_lbl.grid(row=4, column=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.recur_choice = tk.StringVar()
        self.recur_choice.set("1")
        recur_rads = [tk.Radiobutton(group3, variable=self.recur_choice, value="none"),
                      tk.Radiobutton(group3, variable=self.recur_choice, value="gauss"),
                      tk.Radiobutton(group3, variable=self.recur_choice, value="tri"),
                      tk.Radiobutton(group3, variable=self.recur_choice, value="rect")]
        rad_labels = ["-none-", "-gaussian-", "-triangle-", "-rectangle-"]
        figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist()]
        for col in range(len(recur_rads)):
            fig_label = ttk.Label(group3)
            fig_label.grid(row=5, column=col+2)
            fig = figs[col]
            canvas = FigureCanvasTkAgg(fig, master=fig_label)
            canvas.get_tk_widget().grid(row=5, column=col+1)
            canvas.show()
            recur_rads[col].grid(row=6, column=col+2)
            rad_label = ttk.Label(group3, text=rad_labels[col], font=SMALL_FONT)
            rad_label.grid(row=7, column=col+2)
        recur_range_label = tk.Label(group3, text="Range/Standard Deviation:")
        recur_range_label.grid(row=5, column=0, sticky="e")
        self.recur_range = tk.Entry(group3, width=int(ENTRY_WIDTH/2), font=SMALL_FONT)
        self.recur_range.grid(row=5, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        mag_lbl = ttk.Label(group3, text="Hazard Magnitude", font=SMALL_FONT)
        mag_lbl.grid(row=9, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.mag_ent = tk.Entry(group3, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.mag_ent.insert(tk.END, "<enter % of replacement cost>")
        self.mag_ent.grid(row=9, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        percent_lbl2 = ttk.Label(group3, text="% of replacement cost", font=SMALL_FONT)
        percent_lbl2.grid(row=9, column=2, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.mag_choice = tk.StringVar()
        self.mag_choice.set("1")
        mag_rads = [tk.Radiobutton(group3, variable=self.mag_choice, value="none"),
                    tk.Radiobutton(group3, variable=self.mag_choice, value="gauss"),
                    tk.Radiobutton(group3, variable=self.mag_choice, value="tri"),
                    tk.Radiobutton(group3, variable=self.mag_choice, value="rect")]
        rad_labels = ["-none-", "-gaussian-", "-triangle-", "-rectangle-"]
        figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist()]
        for col in range(len(mag_rads)):
            fig_label = ttk.Label(group3)
            fig_label.grid(row=10, column=col+2)
            fig = figs[col]
            canvas = FigureCanvasTkAgg(fig, master=fig_label)
            canvas.get_tk_widget().grid(row=5, column=col+1)
            canvas.show()
            mag_rads[col].grid(row=11, column=col+2)
            rad_label = ttk.Label(group3, text=rad_labels[col], font=SMALL_FONT)
            rad_label.grid(row=12, column=col+2)
        mag_range_label = tk.Label(group3, text="Range/Standard Deviation:")
        mag_range_label.grid(row=10, column=0, sticky="e")
        self.mag_range = tk.Entry(group3, width=int(ENTRY_WIDTH/2), font=SMALL_FONT)
        self.mag_range.grid(row=10, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        sep2 = ttk.Separator(group3, orient=tk.HORIZONTAL)
        sep2.grid(row=13, sticky="ew", columnspan=90, padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.preference = tk.StringVar()
        self.preference.set("Risk Neutral")
        risk_lbl = ttk.Label(group3, text="Define Risk Preference", font=SMALL_FONT)
        risk_lbl.grid(row=14, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.neutral = ttk.Radiobutton(group3, text="Risk Neutral",
                                       variable=self.preference, value="neutral")
        self.neutral.grid(row=15, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.averse = ttk.Radiobutton(group3, text="Risk Averse",
                                      variable=self.preference, value="averse")
        self.averse.grid(row=16, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.accepting = ttk.Radiobutton(group3, text="Risk Accepting",
                                         variable=self.preference, value="accepting")
        self.accepting.grid(row=17, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Manueverability Buttons
        group4 = ttk.LabelFrame(self)
        group4.grid(row=5, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
            # === Places spacing so that buttons are on the bottom right
        space_lbl = ttk.Label(group4, text=" " * 106)
        space_lbl.grid(row=0, column=1)
        next_button = ttk.Button(group4, text="Next>>", command=lambda: self.check_page(controller))
        next_button.grid(row=0, column=4, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        exit_button = ttk.Button(group4, text="Exit", command=sys.exit)
        exit_button.grid(row=0, column=3, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def restore(self):
        """restores default discount value"""
        self.dis_ent.delete(0, tk.END)
        self.dis_ent.insert(tk.END, "5.00")

    def check_page(self, controller):
        """Ensures that all required fields are properly filled out before continuing"""
        err_messages = ""

        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        if self.name_ent.get() == "" or self.name_ent.get() == "<enter project name>":
            err_messages += "Project name field has been left empty!\n\n"
            valid = False

        for i in range(int(self.num_plans_ent.get())):
            if self.name_ents[i].get() == "" or self.name_ents[i].get() == "<enter plan name>":
                err_messages += "Name for Alternative " + str(i) + " hasn't been given \n\n"
                valid = False

        not_neutral = self.preference.get() != "neutral"
        not_averse = self.preference.get() != "averse"
        not_accepting = self.preference.get() != "accepting"
        if not_neutral and not_averse and not_accepting:
            err_messages += "A risk preference has not been selected! Please select one\n\n"
            valid = False

        # ===== Number fields must be positive numbers
        try:
            float(self.hor_ent.get())
            if float(self.hor_ent.get()) == 0:
                err_messages += "Planning Horizon must be greater than zero.\n"
                err_messages += "Please enter a positive amount. \n\n"
                valid = False
        except ValueError:
            err_messages += "Planning Horizon must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.hor_ent.get():
            err_messages += "Planning Horizon must be a positive number.\n"
            err_messages += " Please enter a positive amount.\n\n"
            valid = False

        try:
            float(self.dis_ent.get())
        except ValueError:
            err_messages += "Discount Rate must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.dis_ent.get():
            err_messages += "Discount Rate must be a positive number.\n"
            err_messages += "Please enter a positive amount.\n\n"
            valid = False


        try:
            float(self.haz_ent.get())
        except ValueError:
            err_messages += "Hazard Recurrence must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.haz_ent.get():
            err_messages += "Hazard Recurrence must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False

        try:
            float(self.recur_range.get())
        except ValueError:
            err_messages += "Hazard Recurrence must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.recur_range.get():
            err_messages += "Hazard Recurrence must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False

        try:
            float(self.mag_ent.get())
        except ValueError:
            err_messages += "Hazard Magnitude must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.mag_ent.get():
            err_messages += "Hazard Magnitude must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False

        try:
            float(self.mag_range.get())
        except ValueError:
            err_messages += "Hazard Magnitude must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.mag_range.get():
            err_messages += "Hazard Magnitude must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False

        if not valid:
            messagebox.showerror("ERROR", err_messages)
            return


        # Fills data_cont with the values entered
        data = self.controller.data_cont
        data.title = self.name_ent.get()
        data.num_plans = int(self.num_plans_ent.get())
        data.horizon = float(self.hor_ent.get())
        data.discount_rate = float(self.dis_ent.get())
        data.risk_preference = self.preference.get()

        data.plan_list = []
        data.plan_list.append(Plan(0, "Base",
                                   [float(self.haz_ent.get()), float(self.recur_range.get()), self.recur_choice.get()],
                                   [float(self.mag_ent.get()), float(self.mag_range.get()), self.mag_choice.get()]))
        for i in range(data.num_plans):
            data.plan_list.append(Plan(i+1, self.name_ents[i].get(),
                                       [float(self.haz_ent.get()), float(self.recur_range.get()), self.recur_choice.get()],
                                       [float(self.mag_ent.get()), float(self.mag_range.get()), self.mag_choice.get()]))

        # TODO: Make file save possible
        #data.save_info()
        controller.show_frame('CostPage')

    def show_info(self):
        """Shows extra information for the user (for clarification)"""
        messagebox.showinfo("More Information",
                            "For the case of this application, the following terms are defined:\n\n"
                            "Planning Horizon:\n        "
                            "The time span - measured in years - for which the project's costs "
                            "and benefits will be measured.\n\n"
                            "Base Scenario:\n        "
                            "Usually referred to as the \"Business as Usual\" case. Refers to the "
                            "costs and benefits when no alternative plan is implemented. Yet, this"
                            " does not have to be the case. The case scenario is the option "
                            "against which the other identified alternatives are compared.\n\n"
                            "Nominal Discount Rate:\n        "
                            "The calculated percentage at which the value of money decreases "
                            "over time. This may take inflation into account. 5.00% is the default."
                            "\n\n"
                            "Hazard Recurrence:\n        "
                            "The number of years expected before a specific hazard occurs "
                            "after its last occurrence. For the purpose of this analysis, only "
                            "one given hazard will be taken into consideration. Future versions"
                            " of the tool may add functionality for compound hazards.\n\n"
                            "Hazard Magnitude:\n        "
                            "The total damage the specific hazard is expected to inflict upon "
                            "occurring. Measured in the fraction of total replacement cost of "
                            "a project.\n\n"
                            "Risk Preference:\n        "
                            "How willing the user/community is to take on risk associated with the "
                            "consequences of potential disruptive events.\n\n\n"
                            "WARNING: \n        "
                            "If this is a previously loaded analysis, "
                            "the number of plans cannot decrease. "
                            "You may, however, add more plans if wanted.\n"
                            "        Also, as of right now, the "
                            "Hazard Magnitude and Risk Preference Fields have no impact on any "
                            "calculations made with this tool. "
                            "The information will merely be stored.")

    def on_trace_choice(self, _name, _index, _mode):
        """Triggers refresh when combobox changes"""

        choice = int(self.num_plans_ent.get())
        for i in range(choice):
            self.name_lbls[i].configure(state="active")
            self.name_ents[i].configure(state="normal")
        for i in range(choice, 6):
            self.name_lbls[i].configure(state="disabled")
            self.name_ents[i].configure(text="", state="disabled")
