"""
   File:          InfoPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the InfoPage,
                  the first page the user will input data on.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.Constants import SMALL_FONT, ENTRY_WIDTH
from GUI.Constants import BASE_PADDING, FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING

from GUI.PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist, disc_dist

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
                                    "the planning horizon,the calculated \n"
                                    "real discount rate for discounting future costs to "
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
                                           "the planning horizon,the calculated \n"
                                           "real discount rate for discounting future costs to "
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
        group3 = ttk.LabelFrame(self, text="Discount Rate")
        group3.grid(row=4, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        dis_lbl = ttk.Label(group3, text="Real Discount Rate", font=SMALL_FONT)
        dis_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.dis_ent = tk.Entry(group3, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.dis_ent.insert(tk.END, "5.00")
        self.dis_ent.grid(row=0, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        percent_lbl = ttk.Label(group3, text="%", font=SMALL_FONT)
        percent_lbl.grid(row=0, column=2, sticky='w', pady=FIELDY_PADDING)

        def_button = ttk.Button(group3, text="Restore Default", command=self.restore)
        def_button.grid(row=2, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        group4 = ttk.LabelFrame(self, text="Hazard Recurrence")
        group4.grid(row=5, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        self.recur_choice = tk.StringVar()
        self.recur_choice.set("none")
        recur_rads = [tk.Radiobutton(group4, variable=self.recur_choice, value="none"),
                      tk.Radiobutton(group4, variable=self.recur_choice, value="gauss"),
                      tk.Radiobutton(group4, variable=self.recur_choice, value="tri"),
                      tk.Radiobutton(group4, variable=self.recur_choice, value="rect"),
                      tk.Radiobutton(group4, variable=self.recur_choice, value="discrete")]
        rad_labels = ["Exact", "Gaussian", "Triangular", "Rectangular", "Discrete"]
        figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist(), disc_dist()]
        for col in range(len(recur_rads)):
            fig_label = ttk.Label(group4)
            fig_label.grid(row=1, column=col)
            fig = figs[col]
            canvas = FigureCanvasTkAgg(fig, master=fig_label)
            canvas.get_tk_widget().grid(row=1, column=col+1)
            canvas.show()
            recur_rads[col].grid(row=3, column=col)
            rad_label = ttk.Label(group4, text=rad_labels[col], font=SMALL_FONT)
            rad_label.grid(row=2, column=col)
        self.recur_choice.trace("w", self.on_trace_change_recur)
        self.recur_label = [tk.Label(group4, text="Most Frequent (Years)"),
                            tk.Label(group4, text="Expected Recurrence (Years)"),
                            tk.Label(group4, text="Least Frequent (Years)")]
        self.recur_one_label = tk.Label(group4, text="Recurrence (Years)")
        self.recur_one_label.grid(row=4, column=0)
        self.recur_gauss_label = [tk.Label(group4, text="Expected Recurrence (Years)"),
                                  tk.Label(group4, text="Standard Deviation (Years)")]
        self.recur_discrete_label = [tk.Label(group4, text="Most Frequent (Years)"),
                                     tk.Label(group4, text="Middle Recurrence (Years)"),
                                     tk.Label(group4, text="Least Frequence (Years)"),
                                     tk.Label(group4, text="Likelihood of Most Frequent (%)"),
                                     tk.Label(group4, text="Likelihood of Middle Recurrence (%)"),
                                     tk.Label(group4, text="Likelihood of Least Frequent (%)")]
        self.recur_range = [tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                            tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                            tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                            tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                            tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                            tk.Entry(group4, width=int(ENTRY_WIDTH/2), font=SMALL_FONT)]
        self.recur_range[0].grid(row=4, column=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        group5 = ttk.LabelFrame(self, text="Hazard Magnitude")
        group5.grid(row=6, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        self.mag_choice = tk.StringVar()
        self.mag_choice.set("none")
        mag_rads = [tk.Radiobutton(group5, variable=self.mag_choice, value="none"),
                    tk.Radiobutton(group5, variable=self.mag_choice, value="gauss"),
                    tk.Radiobutton(group5, variable=self.mag_choice, value="tri"),
                    tk.Radiobutton(group5, variable=self.mag_choice, value="rect"),
                    tk.Radiobutton(group5, variable=self.mag_choice, value="discrete")]
        rad_labels = ["Exact", "Gaussian", "Triangular", "Rectangular", "Discrete"]
        figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist(), disc_dist()]
        for col in range(len(mag_rads)):
            fig_label = ttk.Label(group5)
            fig_label.grid(row=1, column=col)
            fig = figs[col]
            canvas = FigureCanvasTkAgg(fig, master=fig_label)
            canvas.get_tk_widget().grid(row=1, column=col+1)
            canvas.show()
            mag_rads[col].grid(row=3, column=col)
            rad_label = ttk.Label(group5, text=rad_labels[col], font=SMALL_FONT)
            rad_label.grid(row=2, column=col)
        self.mag_choice.trace("w", self.on_trace_change_mag)
        self.mag_label = [tk.Label(group5, text="Least Severe (%)"),
                          tk.Label(group5, text="Expected Magnitude (%)"),
                          tk.Label(group5, text="Most Severe (%)")]
        self.mag_one_label = tk.Label(group5, text="Magnitude (%)")
        self.mag_one_label.grid(row=4, column=0)
        self.mag_gauss_label = [tk.Label(group5, text="Expected Magnitude (%)"),
                                tk.Label(group5, text="Standard Deviation (%)")]
        self.mag_discrete_label = [tk.Label(group5, text="Least Severe (%)"),
                                   tk.Label(group5, text="Middle Severity (%)"),
                                   tk.Label(group5, text="Most severe (%)"),
                                   tk.Label(group5, text="Likelihood of Least Severe (%)"),
                                   tk.Label(group5, text="Likelihood of Middle Severity (%)"),
                                   tk.Label(group5, text="Likelihood of Most Severe (%)")]
        self.mag_range = [tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                          tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                          tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                          tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                          tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT),
                          tk.Entry(group5, width=int(ENTRY_WIDTH/2), font=SMALL_FONT)]
        self.mag_range[0].grid(row=4, column=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        group6 = ttk.LabelFrame(self, text="Risk Preference")
        group6.grid(row=7, stick="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        self.preference = tk.StringVar()
        self.preference.set("none")
        risk_lbl = ttk.Label(group6, text="Define Risk Preference", font=SMALL_FONT)
        risk_lbl.grid(row=14, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.neutral = ttk.Radiobutton(group6, text="Risk Neutral",
                                       variable=self.preference, value="neutral")
        self.neutral.grid(row=15, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.averse = ttk.Radiobutton(group6, text="Risk Averse",
                                      variable=self.preference, value="averse")
        self.averse.grid(row=16, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.accepting = ttk.Radiobutton(group6, text="Risk Accepting",
                                         variable=self.preference, value="accepting")
        self.accepting.grid(row=17, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Manueverability Buttons
        group7 = ttk.LabelFrame(self)
        group7.grid(row=8, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
            # === Places spacing so that buttons are on the bottom right
        space_lbl = ttk.Label(group7, text=" " * 106)
        space_lbl.grid(row=0, column=1)
        next_button = ttk.Button(group7, text="Next>>",
                                 command=lambda: self.check_page(controller, 'CostPage'))
        next_button.grid(row=0, column=7, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        menu_button = ttk.Button(group7, text="Menu",
                                 command=lambda: self.check_page(controller, 'DirectoryPage'))
        menu_button.grid(row=0, column=3, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def restore(self):
        """restores default discount value"""
        self.dis_ent.delete(0, tk.END)
        self.dis_ent.insert(tk.END, "5.00")

    def check_page(self, controller, frame):
        """Ensures that all required fields are properly filled out before continuing"""
        err_messages = ""

        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        if self.name_ent.get() == "" or self.name_ent.get() == "<enter project name>":
            err_messages += "Project name field has been left empty!\n\n"
            valid = False
        if "," in self.name_ent.get():
            err_messages += "Project name field cannot have a comma.\n\n"
            valid = False

        for i in range(int(self.num_plans_ent.get())):
            if self.name_ents[i].get() == "" or self.name_ents[i].get() == "<enter plan name>":
                err_messages += "Name for Alternative " + str(i) + " hasn't been given.\n\n"
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

        if self.recur_choice.get() == 'none':
            try:
                if float(self.recur_range[0].get()) <= 0:
                    valid = False
                    err_messages += "Hazard Recurrence must be greater than zero.\n\n"
            except ValueError:
                valid = False
                err_messages += "Hazard Recurrence must be a number.\n\n"
        elif self.recur_choice.get() == 'gauss':
            try:
                if float(self.recur_range[0].get()) <= 0:
                    valid = False
                    err_messages += "Hazard Recurrence must be greater than zero.\n\n"
                if float(self.recur_range[1].get()) <= 0:
                    valid = False
                    err_messages += "Hazard Recurrence standard deviation must be "
                    err_messages += "greater than zero.\n\n"
            except ValueError:
                valid = False
                err_messages += "All Hazard Recurrence values must be numbers.\n\n"
        elif self.recur_choice.get() == 'discrete':
            for entry in self.recur_range:
                try:
                    float(entry.get())
                except ValueError:
                    valid = False
                    err_messages += "All Hazard Recurrence inputs must be numbers.\n\n"
            try:
                assert float(self.recur_range[0].get()) <= float(self.recur_range[1].get()) <= float(self.recur_range[2].get())
                disc_sum = float(self.recur_range[3].get()) + float(self.recur_range[4].get()) + float(self.recur_range[5].get())
                if disc_sum != 100:
                    valid = False
                    err_messages += "Hazard Recurrence discrete likelihoods must add to 100%.\n\n"
            except AssertionError:
                valid = False
                err_messages += "Hazard Recurrence discrete options must be in order.\n\n"
            except ValueError:
                pass
        else:
            try:
                bound = float(self.recur_range[0].get()) <= float(self.recur_range[1].get()) <= float(self.recur_range[2].get())
                if not bound:
                    valid = False
                    err_messages += "Hazard Recurrence lower bound must be below upper bound.\n\n"
            except ValueError:
                valid = False
                err_messages += "All Hazard Recurrence inputs must be numbers.\n\n"

        if self.mag_choice.get() == 'none':
            try:
                if float(self.mag_range[0].get()) < 0:
                    valid = False
                    err_messages += "Hazard Magnitude must be greater than or equal to zero.\n\n"
            except ValueError:
                if self.mag_range[0].get() != "":
                    valid = False
                    err_messages += "Hazard Magnitude must be a number.\n\n"
        elif self.mag_choice.get() == 'gauss':
            try:
                if float(self.mag_range[0].get()) <= 0:
                    valid = False
                    err_messages += "Hazard Magnitude must be greater than zero.\n\n"
                if float(self.mag_range[1].get()) <= 0:
                    valid = False
                    err_messages += "Hazard Magnitude standard deviation must be "
                    err_messages += "greater than zero.\n\n"
            except ValueError:
                valid = False
                err_messages += "All Hazard Magnitude values must be numbers.\n\n"
        elif self.mag_choice.get() == 'discrete':
            for entry in self.mag_range:
                try:
                    float(entry.get())
                except ValueError:
                    valid = False
                    err_messages += "All Hazard Magnitude inputs must be numbers.\n\n"
            try:
                assert float(self.mag_range[0].get()) >= float(self.mag_range[1].get()) >= float(self.mag_range[2].get())
                disc_sum = float(self.mag_range[3].get()) + float(self.mag_range[4].get()) + float(self.mag_range[5].get())
                if disc_sum != 100:
                    valid = False
                    err_messages += "Hazard Magnitude discrete likelihoods must add to 100%.\n\n"
            except AssertionError:
                valid = False
                err_messages += "Hazard Magnitude discrete options must be in order.\n\n"
            except ValueError:
                pass
        else:
            try:
                bound = float(self.mag_range[0].get()) <= float(self.mag_range[1]) <= float(self.mag_range[2].get())
                if not bound:
                    valid = False
                    err_messages += "Hazard Magnitude lower bound must be below upper bound.\n\n"
            except ValueError:
                valid = False
                err_messages += "All Hazard Magnitude inputs must be numbers.\n\n"

        if self.preference.get() not in ['neutral', 'averse', 'accepting', 'none']:
            err_messages += "A risk preference has not been selected! Please select one.\n\n"
            valid = False

        if not valid:
            messagebox.showerror("ERROR", err_messages)
            return valid

        # Fills data_cont with the values entered
        data = self.controller.data_cont
        data.title = self.name_ent.get()
        data.num_plans = int(self.num_plans_ent.get()) + 1
        data.horizon = float(self.hor_ent.get())
        data.discount_rate = float(self.dis_ent.get())
        data.risk_preference = self.preference.get()

        dis_recurr = [entry.get() for entry in self.recur_range]
        dis_mag = [entry.get() for entry in self.mag_range]

        if data.plan_list == []:
            data.plan_list.append(Plan(0, "Base",
                                       [self.recur_choice.get(), dis_recurr],
                                       [self.mag_choice.get(), dis_mag],
                                       data.discount_rate, data.horizon, data.stat_life,
                                       self.data_cont.parties))
            for i in range(1, data.num_plans):
                data.plan_list.append(Plan(i, self.name_ents[i-1].get(),
                                           [self.recur_choice.get(), dis_recurr],
                                           [self.mag_choice.get(), dis_mag],
                                           data.discount_rate, data.horizon, data.stat_life,
                                           self.data_cont.parties))
        else:
            old_num_plans = len(data.plan_list)
            new_num_plans = data.num_plans
            if old_num_plans <= new_num_plans:
                data.plan_list[0].update(0, 'Base', [self.recur_choice.get(), dis_recurr],
                                         [self.mag_choice.get(), dis_mag],
                                         data.discount_rate, data.horizon, data.stat_life)
                for i in range(1, old_num_plans):
                    data.plan_list[i].update(i, self.name_ents[i-1].get(),
                                             [self.recur_choice.get(), dis_recurr],
                                             [self.mag_choice.get(), dis_mag],
                                             data.discount_rate, data.horizon, data.stat_life)
                for j in range(old_num_plans, new_num_plans):
                    data.plan_list.append(Plan(j, self.name_ents[j-1].get(),
                                               [self.recur_choice.get(), dis_recurr],
                                               [self.mag_choice.get(), dis_mag],
                                               data.discount_rate, data.horizon, data.stat_life,
                                               self.data_cont.parties))
            elif old_num_plans > new_num_plans:
                data.plan_list[0].update(0, 'Base', [self.recur_choice.get(), dis_recurr],
                                         [self.mag_choice.get(), dis_mag],
                                         data.discount_rate, data.horizon, data.stat_life)
                for i in range(1, new_num_plans):
                    data.plan_list[i].update(i, self.name_ents[i-1].get(),
                                             [self.recur_choice.get(), dis_recurr],
                                             [self.mag_choice.get(), dis_mag],
                                             data.discount_rate, data.horizon, data.stat_life)
                for j in range(old_num_plans, new_num_plans, -1):
                    data.plan_list.remove(data.plan_list[j-1])

        data.file_save()
        controller.show_frame(frame)

    def show_info(self):
        """Shows extra information for the user (for clarification)"""
        messagebox.showinfo("More Information",
                            "In the EDGeS Tool, the terms are defined in the following manner:\n"
                            "    Planning Horizon: The time span – measured in years – for which "
                            "the project’s costs and benefits will be assessed in the analysis.\n"
                            "    Base Scenario:  Often referred to as the “business as usual” case."
                            " It refers to the option against which the other identified alterative"
                            " scenarios are compared.\n"
                            "    Real Discount Rate: Often referred to as the “time value of "
                            "money.” Typically, a dollar is worth more today than it would be "
                            "worth tomorrow. This is the percent at which the value of money "
                            "decreases over time, allowing for the comparison of quantities as if "
                            "prices had not changed. 5.00% is the default value.\n"
                            "    Hazard Recurrence: The number of years expected before a specific "
                            "hazard occurs after its last occurrence. In this version of EDGeS "
                            "only a single hazard will be considered. Future versions of the EDGeS"
                            " Tool may add functionality to deal with compound hazards directly.\n"
                            "    Hazard Magnitude: The total damage the defined hazard is expected "
                            "tp inflict upon occurrence. The magnitude is measured as the fraction "
                            "of total replacement cost for a project.\n"
                            "    Risk preference: The willingness of the user/community to take on "
                            "the risk(s) associated with the consequences of potential disruptive "
                            "events.\n\n"
                            "NOTE: The ‘hazard magnitude’ and ‘risk preference’ fields have no "
                            "impact on the calculations made within this Tool. The information "
                            "will only be stored for reference.")

    def on_trace_change(self, _name, _index, _mode):
        """ Triggers all on_trace_***"""
        self.on_trace_change_mag(_name, _index, _mode)
        self.on_trace_change_recur(_name, _index, _mode)
        self.on_trace_choice(_name, _index, _mode)

    def on_trace_choice(self, _name, _index, _mode):
        """Triggers refresh when combobox changes"""

        try:
            choice = int(self.num_plans_ent.get())
            #print('try', choice)
            if 0 <= choice <= 6:
                for i in range(choice):
                    self.name_lbls[i].configure(state="active")
                    self.name_ents[i].configure(state="normal")
                for i in range(choice, 6):
                    self.name_lbls[i].configure(state="disabled")
                    self.name_ents[i].configure(text="", state="disabled")
            elif choice < 0:
                self.num_plans_ent.set(0)
                self.on_trace_choice("", "", "")
            else:
                #print('set 6', choice)
                self.num_plans_ent.set(6)
                self.on_trace_choice("", "", "")
        except ValueError:
            if self.num_plans_ent.get() == "":
                pass
            else:
                self.num_plans_ent.set(0)
                self.on_trace_choice("", "", "")

    def on_trace_change_recur(self, _name, _index, _mode):
        """Triggers refresh when the uncertainty choices change."""
        if self.recur_choice.get() == "none":
            self.recur_one_label.grid(row=4, column=0)
            for label in self.recur_label:
                label.grid_remove()
            for label in self.recur_gauss_label:
                label.grid_remove()
            for label in self.recur_discrete_label:
                label.grid_remove()
            self.recur_range[0].grid(row=4, column=1,
                                     padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(1, len(self.recur_range)):
                self.recur_range[i].grid_remove()
        elif self.recur_choice.get() == "gauss":
            self.recur_one_label.grid_remove()
            for label in self.recur_label:
                label.grid_remove()
            for label in self.recur_gauss_label:
                label.grid(row=self.recur_gauss_label.index(label)+4, column=0)
            for label in self.recur_discrete_label:
                label.grid_remove()
            self.recur_range[0].grid(row=4, column=1,
                                     padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            self.recur_range[1].grid(row=5, column=1,
                                     padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(2, len(self.recur_range)):
                self.recur_range[i].grid_remove()
        elif self.recur_choice.get() == "discrete":
            self.recur_one_label.grid_remove()
            for label in self.recur_label:
                label.grid_remove()
            for label in self.recur_gauss_label:
                label.grid_remove()
            for label in self.recur_discrete_label[0:3]:
                label.grid(row=self.recur_discrete_label.index(label)+4, column=0)
            for label in self.recur_discrete_label[3:6]:
                label.grid(row=self.recur_discrete_label.index(label)+1, column=2)
            for entry in self.recur_range[0:3]:
                entry.grid(row=self.recur_range.index(entry)+4, column=1,
                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for entry in self.recur_range[3:6]:
                entry.grid(row=self.recur_range.index(entry)+1, column=3,
                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        else:
            self.recur_one_label.grid_remove()
            for label in self.recur_label:
                label.grid(row=self.recur_label.index(label)+4, column=0)
            for label in self.recur_gauss_label:
                label.grid_remove()
            for label in self.recur_discrete_label:
                label.grid_remove()
            for i in range(3):
                self.recur_range[i].grid(row=self.recur_range.index(self.recur_range[i])+4,
                                         column=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(3, len(self.recur_range)):
                self.recur_range[i].grid_remove()

    def on_trace_change_mag(self, _name, _index, _mode):
        """Triggers refresh when the uncertainty choices change."""
        if self.mag_choice.get() == "none":
            self.mag_one_label.grid(row=4, column=0)
            for label in self.mag_label:
                label.grid_remove()
            for label in self.mag_gauss_label:
                label.grid_remove()
            for label in self.mag_discrete_label:
                label.grid_remove()
            self.mag_range[0].grid(row=4, column=1,
                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(1, len(self.mag_range)):
                self.mag_range[i].grid_remove()
        elif self.mag_choice.get() == "gauss":
            self.mag_one_label.grid_remove()
            for label in self.mag_label:
                label.grid_remove()
            for label in self.mag_gauss_label:
                label.grid(row=self.mag_gauss_label.index(label)+4, column=0)
            for label in self.mag_discrete_label:
                label.grid_remove()
            self.mag_range[0].grid(row=4, column=1,
                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            self.mag_range[1].grid(row=5, column=1,
                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(2, len(self.mag_range)):
                self.mag_range[i].grid_remove()
        elif self.mag_choice.get() == "discrete":
            self.mag_one_label.grid_remove()
            for label in self.mag_label:
                label.grid_remove()
            for label in self.mag_gauss_label:
                label.grid_remove()
            for label in self.mag_discrete_label[0:3]:
                label.grid(row=self.mag_discrete_label.index(label)+4, column=0)
            for label in self.mag_discrete_label[3:6]:
                label.grid(row=self.mag_discrete_label.index(label)+1, column=2)
            for entry in self.mag_range[0:3]:
                entry.grid(row=self.mag_range.index(entry)+4, column=1,
                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for entry in self.mag_range[3:6]:
                entry.grid(row=self.mag_range.index(entry)+1, column=3,
                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        else:
            self.mag_one_label.grid_remove()
            for label in self.mag_label:
                label.grid(row=self.mag_label.index(label)+4, column=0)
            for label in self.mag_gauss_label:
                label.grid_remove()
            for label in self.mag_discrete_label:
                label.grid_remove()
            for i in range(3):
                self.mag_range[i].grid(row=self.mag_range.index(self.mag_range[i])+4,
                                       column=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            for i in range(3, len(self.mag_range)):
                self.mag_range[i].grid_remove()
