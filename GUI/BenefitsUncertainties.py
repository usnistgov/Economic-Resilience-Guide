"""
   File:          BenefitsUncertainties.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for adding uncertainties to benefits,
                  the page for the user to input Benefits uncertainty distributions.
    * NOTE: This page is a prototype uncertainties page.
"""

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.BenefitsPage import BenefitsPage
from GUI.InfoPage import InfoPage

from GUI.PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist

from GUI.Constants import SMALL_FONT, LARGE_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

matplotlib.use("TkAgg")


#
#
###################################### Benefits Uncertainties ######################################
#
#
class BenefitsUncertaintiesPage(tk.Frame):
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
                                     "uncertainty distribution requires key information. \n"
                                     "Please provide this information in the boxes below the "
                                     "distribution type you select. Further information is "
                                     "available in the “more information” section for this page.\n"
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ben_lbl = tk.Label(self, text="Benefits Uncertainties", font=LARGE_FONT)
        ben_lbl.grid(row=2, sticky="w")
        self.direct_range = []
        self.indirect_range = []
        self.res_rec_range = []
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Uncertainty selection Widgets

        self.on_trace_change("name", "index", "mode")

        controller.frames[BenefitsPage].choice.trace("w", self.on_trace_change)


        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'FatalitiesPage'
            moveon = self.add_uncertainty(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'BenefitsPage'
            moveon = self.add_uncertainty(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)


        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=lambda: self.data_cont.file_save())
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Update Uncertainties",
                                     command=self.add_uncertainty)
        self.add_button.grid(row=12, column=1, sticky="se",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=13, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=13, column=1, sticky="se",
                             padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        # NOTE: the _ before event designates it as an intentionally unused input
        self.update_prev_list()

    def show_info(self):
        """ Pulls up information for the Benefits page."""
        messagebox.showinfo("More Information",
                            "Some benefit information text.")
        # TODO: Update Information Text

    def add_uncertainty(self, moveon=False):
        """Appends list of benefits, clears page's entry widgets,
           and updates 'Previously Inputted Benefits' section"""
        if moveon:
            valid = self.check_page(printout=False)
        else:
            valid = self.check_page()
        if not valid:
            if moveon:
                checker = messagebox.askyesno('Move Forward?',
                                              'Your benefit was not saved. '
                                              'Select \'No\' if you wish to continue editing'
                                              ' and \'Yes\' if you wish to move to the next page.')
                return checker
            return False

        for plan in self.data_cont.plan_list:
            for ben in plan.bens.indiv:
                ben.add_uncertainty(self.range[plan.id_assign][plan.bens.indiv.index(ben)].get(),
                                    self.choices[plan.id_assign][plan.bens.indiv.index(ben)].get())

        if valid:
            # ===== Updates the page for the next cost
            self.update_prev_list()
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted Benefits' Section"""
        pass

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        #TODO: Fix this function
        err_messages = ""

        valid = True


        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return valid


    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""
        # TODO: Ensure that this works as expected/desired.

        group = []
        self.labels = []
        self.range = []

        self.choices = [[tk.StringVar() for ben in plan.bens.indiv]
                        for plan in self.data_cont.plan_list]
        for i in range(self.data_cont.num_plans):
            for j in range(len(self.choices[i])):
                self.choices[i][j].set(self.data_cont.plan_list[i].bens.indiv[j].dist)

        for plan in self.data_cont.plan_list:
            row_index = 0
            group.append(ttk.LabelFrame(self, text=plan.name))
            for ben in plan.bens.indiv:
                print_text = ben.title + " - $" + str(ben.amount)
                self.labels.append(ttk.Label(group[-1], text=print_text, font=SMALL_FONT))
                self.labels[-1].grid(row=row_index, column=0, sticky="w",
                                     padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1


        for plan in self.data_cont.plan_list:
            row_index = 0
            i = self.data_cont.plan_list.index(plan)
            group.append(ttk.LabelFrame(self, text=plan.name))
            group[-1].grid(row=3+i, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
            self.range.append([])
            for benefit in plan.bens.indiv:
                print_text = benefit.title + " - $" + str(benefit.amount)
                self.labels.append(ttk.Label(group[-1], text=print_text,
                                             font=SMALL_FONT))
                self.labels[-1].grid(row=row_index, column=0, sticky="w",
                                     padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1
                j = plan.bens.indiv.index(benefit)
                rads = [tk.Radiobutton(group[-1], variable=self.choices[i][j], value="none"),
                        tk.Radiobutton(group[-1], variable=self.choices[i][j], value="gauss"),
                        tk.Radiobutton(group[-1], variable=self.choices[i][j], value="tri"),
                        tk.Radiobutton(group[-1], variable=self.choices[i][j], value="rect")]
                rad_labels = ["-none-", "-gaussian-", "-triangle-", "-rectangle-"]
                figs = [none_dist(), gauss_dist(), tri_dist(), rect_dist()]
                for col in range(len(rads)):
                    fig_label = ttk.Label(group[-1])
                    fig_label.grid(row=row_index, column=col+1)
                    fig = figs[col]
                    canvas = FigureCanvasTkAgg(fig, master=fig_label)
                    canvas.get_tk_widget().grid(row=row_index, column=col+1)
                    canvas.show()
                    rads[col].grid(row=row_index+1, column=col+1)
                    rad_label = ttk.Label(group[-1], text=rad_labels[col], font=SMALL_FONT)
                    rad_label.grid(row=row_index+2, column=col+1)
                range_label = tk.Label(group[-1], text="Range/Standard Deviation:")
                range_label.grid(row=row_index+3, column=1, sticky="e")
                self.range[i].append(tk.Entry(group[-1], width=int(ENTRY_WIDTH/2), font=SMALL_FONT))
                self.range[i][j].grid(row=row_index+3, column=2, sticky="w",
                                      padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                self.range[i][j].insert(tk.END, benefit.range)
                row_index += 4

