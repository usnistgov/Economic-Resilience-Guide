"""
   File:          NonDBensUncertainties.py
   Author:        Shannon Grubb
   Description:   Interacts with EconGuide.py, builds the GUI for adding uncertainties to
                  non-disaster benefits, the page for the user to input Non D Benefits
                  uncertainty distributions.
"""

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist, disc_dist

from GUI.Constants import SMALL_FONT, LARGE_FONT
from GUI.Constants import FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

matplotlib.use("TkAgg")


#
#
########################### Non Disaster Related Benefits Uncertainties ###########################
#
#
class NonDBensUncertaintiesPage(tk.Frame):
    """
    GUI for the input of all Disaster-Related benefits.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="There is often uncertainty surrounding the exact benefits.\n"
                                     "The benefits associated with each alternative are listed "
                                     "below. The type of benefit and the dollar amount associated "
                                     "with the benefit is indicated.\nFor each benefit, please "
                                     "select the associated uncertainty description. Each type of "
                                     "uncertainty distribution requires key information.\n"
                                     "Please provide this information in the boxes below the "
                                     "distribution type you select.\nFurther information is "
                                     "available in the “More Information” section for this page.\n"
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ben_lbl = tk.Label(self, text="Non Disaster Related Benefits Uncertainties",
                           font=LARGE_FONT)
        ben_lbl.grid(row=2, sticky="w")
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

        #controller.frames[BenefitsPage].choice.trace("w", self.on_trace_change)


        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'AnalysisInfo'
            moveon = self.add_uncertainty(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'NonDBensPage'
            moveon = self.add_uncertainty(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def menu():
            """ Tries to save the input and sends the user to the Directory Page.
            If save unsuccessful, asks user for verification to move on."""
            go_to_place = 'DirectoryPage'
            moveon = self.add_uncertainty(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)



        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis", command=self.data_cont.file_save)
        save_button.grid(row=1, column=0, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Update Uncertainties",
                                     command=self.add_uncertainty)
        self.add_button.grid(row=3, column=0, sticky="w",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=13, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=13, column=0, sticky="se",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Menu", command=menu).grid(row=13, column=0,
                                                         padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def show_info(self):
        """ Pulls up information for the NonDBenefits page."""
        messagebox.showinfo("More Information",
                            "Uncertainty may surround exact point estimates for user defined "
                            "non-disaster related benefits. On this screen the values associated "
                            "with all defined non-disaster related benefits are summarized. "
                            "The non-disaster related benefits are listed by alterative. The "
                            "title for each non-disaster related benefit and the point value "
                            "dollar estimate previously defined are provided.\n\n"
                            "For each non-disaster related benefit please define the type of "
                            "uncertainty distribution (below the cost description). If there is "
                            "no uncertainty associated with a given non-disaster related benefit "
                            "or you prefer not to include this information, you may choose the "
                            "‘none’ option.\n\n"
                            "Each type of uncertainty distribution requires specific user inputs. "
                            "The uncertainty distributions and their associated required "
                            "information are as follows:\n"
                            "•	‘Gaussian’ is a common continuous probability distribution. The "
                            "assumption is that the Gaussian distribution is symmetric in this "
                            "Tool. The user needs to define the ‘standard deviation ($)’ from the "
                            "point estimate defined by the user for the non-disaster related "
                            "benefit.\n"
                            "•	‘Triangle’ is a continuous probability distribution. This "
                            "distribution can be defined to be symmetric or asymmetric around the "
                            "cost point estimate. The user needs to provide a ‘Lower bound ($)’ "
                            "and ‘Upper bound ($).’Be sure that the lower bound is indeed less "
                            "than the point estimate and that the point estimate is less than the "
                            "upper bound value.\n"
                            "•	‘Rectangle’ is a continuous probability distribution for which "
                            "all intervals of the same length are equally probable. The "
                            "rectangular distribution is sometimes referred to as a uniform "
                            "distribution. The user needs to provide a ‘Lower bound ($)’ and "
                            "‘Upper bound ($).’ Be sure that the lower bound is indeed less than "
                            "the point estimate and that the point estimate is less than the "
                            "upper bound value.\n"
                            "•	‘Discrete’ is a distribution that is not continuous around the "
                            "point estimate value for the non-disaster related benefit. One of "
                            "the three values must be the point estimate. Be sure that the lower "
                            "bound is indeed less than the point estimate and that the point "
                            "estimate is less than the upper bound value. The user needs to "
                            "assign a probability of occurrence to each of the ‘Lower bound ($),’ "
                            "‘Middle bound ($),’ and ‘Upper bound ($)’. The sum of these "
                            "probability values must be 100%.\n")


    def add_uncertainty(self, moveon=False):
        """Adds the uncertainty and updates the page."""
        if moveon:
            valid = self.check_page()
        else:
            valid = self.check_page(printout=False)

        for plan in self.data_cont.plan_list:
            for ben in plan.nond_bens.indiv:
                ben_idx = plan.nond_bens.indiv.index(ben)
                new_values = []
                for entry in self.ranges[plan.num][ben_idx]:
                    new_values.append(entry.get())
                ben.add_uncertainty(new_values,
                                    self.choices[plan.num][ben_idx].get())
        self.on_trace_change('_name', '_index', '_mode')

        return valid

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool """
        err_messages = ""
        valid = True
        for plan in self.data_cont.plan_list:
            for ben in plan.nond_bens.indiv:
                dist = self.choices[plan.num][plan.nond_bens.indiv.index(ben)].get()
                nums = self.ranges[plan.num][plan.nond_bens.indiv.index(ben)]
                try:
                    assert dist in ['none', 'gauss', 'rect', 'tri', 'discrete']
                except AssertionError:
                    valid = False

                choices = [nums[i].get().replace(',', '').replace(' ', '') for i in range(6)]

                if dist == 'none':
                    for entry in nums:
                        entry.delete(0, tk.END)
                        entry.insert(tk.END, '<insert uncertainty>')
                elif dist == 'gauss':
                    try:
                        if float(choices[0]) <= 0:
                            err_messages += "Standard deviation must be greater than zero."
                            err_messages += " (" + ben.title + ").\n\n"
                    except ValueError:
                        valid = False
                        err_messages += "All inputs must be numbers (" + ben.title +").\n\n"
                    for entry in nums[1:]:
                        entry.delete(0, tk.END)
                        entry.insert(tk.END, '<insert uncertainty>')
                elif dist == 'discrete':
                    for entry in choices:
                        try:
                            float(entry)
                        except ValueError:
                            valid = False
                            err_messages += "All inputs must be numbers (" + ben.title + ").\n\n"
                    try:
                        assert float(choices[0]) <= float(choices[1]) <= float(choices[2])
                        disc_sum = float(choices[3]) + float(choices[4]) + float(choices[5])
                        if disc_sum != 100:
                            valid = False
                            err_messages += "Discrete likelihoods must add to 100% ("
                            err_messages += ben.title + ").\n\n"
                    except AssertionError:
                        valid = False
                        err_messages += "Discrete options must be in order ("
                        err_messages += ben.title + ").\n\n"
                    except ValueError:
                        pass
                    try:
                        assert float(ben.amount) in [float(choices[0]),
                                                     float(choices[1]),
                                                     float(choices[2])]
                    except AssertionError:
                        valid = False
                        err_messages += "One of the discrete options must be your point estimate "
                        err_messages += "(" + ben.title + ").\n\n"
                    except ValueError:
                        pass
                else:
                    try:
                        bound = float(choices[0]) <= float(ben.amount) <= float(choices[1])
                        if not bound:
                            valid = False
                            err_messages += "Lower bound must be below Upper bound "
                            err_messages += "(" + ben.title + ").\n\n"
                    except ValueError:
                        valid = False
                        err_messages += "All inputs must be numbers (" + ben.title + ").\n\n"
                    for entry in nums[2:]:
                        entry.delete(0, tk.END)
                        entry.insert(tk.END, '<insert uncertainty>')


        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return valid


    def on_trace_change(self, _name, _index, _mode):
        """Updates the number of plans with options dependent on number of benefits input."""
        for group in self.groups:
            group.grid_forget()
            group.destroy()
        self.groups = []
        rad_labels = ["Exact", "Gaussian", "Triangular", "Rectangular", "Discrete"]
        figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist(), disc_dist()]
        self.choices = [[tk.StringVar() for ben in plan.nond_bens.indiv]
                        for plan in self.data_cont.plan_list]
        rads = []
        self.ranges = []
        self.labels = []
        for plan in self.data_cont.plan_list:
            row_index = 0
            self.groups.append(ttk.LabelFrame(self, text=plan.name))
            self.groups[-1].grid(row=4+plan.num, sticky="ew",
                                 padx=FIELDX_PADDING, pady=FIELDY_PADDING)
            rads.append([])
            self.ranges.append([])
            self.labels.append([])
            for ben in plan.nond_bens.indiv:
                choice = plan.nond_bens.indiv.index(ben)
                self.choices[plan.num][choice].set(ben.dist)
                titles = ttk.Label(self.groups[-1],
                                   text=ben.title + " - $" + '{:,.2f}'.format(ben.amount),
                                   font=SMALL_FONT)
                titles.grid(row=row_index, column=0, sticky="w",
                            padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                rads[plan.num].append([tk.Radiobutton(self.groups[-1],
                                                      variable=self.choices[plan.num][choice],
                                                      value="none"),
                                       tk.Radiobutton(self.groups[-1],
                                                      variable=self.choices[plan.num][choice],
                                                      value="gauss"),
                                       tk.Radiobutton(self.groups[-1],
                                                      variable=self.choices[plan.num][choice],
                                                      value="tri"),
                                       tk.Radiobutton(self.groups[-1],
                                                      variable=self.choices[plan.num][choice],
                                                      value="rect"),
                                       tk.Radiobutton(self.groups[-1],
                                                      variable=self.choices[plan.num][choice],
                                                      value="discrete")])
                self.ranges[plan.num].append([tk.Entry(self.groups[-1], width=int(ENTRY_WIDTH/2),
                                                       font=SMALL_FONT) for i in range(6)])
                self.labels[plan.num].append([])
                for col in range(5):
                    fig_label = ttk.Label(self.groups[-1])
                    fig_label.grid(row=row_index + 1, column=col)
                    fig = figs[col]
                    canvas = FigureCanvasTkAgg(fig, master=fig_label)
                    canvas.get_tk_widget().grid(row=1, column=col+1)
                    canvas.show()
                    rads[plan.num][choice][col].grid(row=row_index + 3, column=col)
                    rad_label = ttk.Label(self.groups[-1], text=rad_labels[col], font=SMALL_FONT)
                    rad_label.grid(row=row_index + 2, column=col)

                if self.choices[plan.num][choice].get() == "none":
                    row_index += 4
                    for entry in self.ranges[plan.num][choice]:
                        entry.grid_remove()
                elif self.choices[plan.num][choice].get() == "gauss":
                    self.labels[plan.num][choice] = [tk.Label(self.groups[-1],
                                                              text="Standard Deviation ($)")]
                    self.labels[plan.num][choice][0].grid(row=row_index + 4, column=0)
                    for entry in self.ranges[plan.num][choice]:
                        entry.grid_remove()
                    self.ranges[plan.num][choice][0].grid(row=row_index + 4, column=1)
                    row_index += 5
                elif self.choices[plan.num][choice].get() == "discrete":
                    self.labels[plan.num][choice] = [tk.Label(self.groups[-1],
                                                              text="Lowest Amount ($)"),
                                                     tk.Label(self.groups[-1],
                                                              text="Middle Amount ($)"),
                                                     tk.Label(self.groups[-1],
                                                              text="Highest Amount ($)"),
                                                     tk.Label(self.groups[-1], text="Likelihood of Lowest Amount (%)"),
                                                     tk.Label(self.groups[-1], text="Likelihood of Middle Amount (%)"),
                                                     tk.Label(self.groups[-1], text="Likelihood of Highest Amount (%)")]
                    for label in self.labels[plan.num][choice][0:3]:
                        label.grid(row=row_index+self.labels[plan.num][choice].index(label)+5,
                                   column=0)
                    for label in self.labels[plan.num][choice][3:6]:
                        label.grid(row=row_index+self.labels[plan.num][choice].index(label)+2,
                                   column=2)
                    for entry in self.ranges[plan.num][choice][0:3]:
                        entry.grid(row=row_index+self.ranges[plan.num][choice].index(entry)+5,
                                   column=1,
                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    for entry in self.ranges[plan.num][choice][3:6]:
                        entry.grid(row=row_index+self.ranges[plan.num][choice].index(entry)+2,
                                   column=3,
                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 8
                else:
                    self.labels[plan.num][choice] = [tk.Label(self.groups[-1],
                                                              text="Lower Bound ($)"),
                                                     tk.Label(self.groups[-1],
                                                              text="Upper Bound ($)")]
                    self.labels[plan.num][choice][0].grid(row=row_index+4, column=0)
                    self.labels[plan.num][choice][1].grid(row=row_index+4, column=2)
                    for entry in self.ranges[plan.num][choice]:
                        entry.grid_remove()
                    self.ranges[plan.num][choice][0].grid(row=row_index+4, column=1)
                    self.ranges[plan.num][choice][1].grid(row=row_index+4, column=3)
                    row_index += 5
                for entry in self.ranges[plan.num][choice]:
                    try:
                        text = ben.range[self.ranges[plan.num][choice].index(entry)]
                        text = '{:,.2f}'.format(float(text))
                    except ValueError:
                        text = ben.range[self.ranges[plan.num][choice].index(entry)]
                    entry.insert(tk.END, text)
