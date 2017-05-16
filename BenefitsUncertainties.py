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

from BenefitsPage import BenefitsPage
from InfoPage import InfoPage

from PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist

from Constants import SMALL_FONT, LARGE_FONT
from Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from Constants import ENTRY_WIDTH

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
                                 command=lambda: self.data_cont.save_info())
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

        num_plans = int(self.controller.frames[InfoPage].num_plans_ent.get())
        for i in range(0, num_plans + 1):
            self.data_cont.ben.u_direct.append([])
            for j in range(len(self.direct_range[i])):
                self.data_cont.ben.u_direct[i].append([self.direct_range[i][j].get()])
                self.data_cont.ben.u_direct[i][j].append(self.direct_choices[i][j].get())
            self.data_cont.ben.u_indirect.append([])
            for j in range(len(self.indirect_range[i])):
                self.data_cont.ben.u_indirect[i].append([self.indirect_range[i][j].get()])
                self.data_cont.ben.u_indirect[i][j].append(self.indirect_choices[i][j].get())
            self.data_cont.ben.u_res_rec.append([])
            for j in range(len(self.res_rec_range[i])):
                self.data_cont.ben.u_res_rec[i].append([self.res_rec_range[i][j].get()])
                self.data_cont.ben.u_res_rec[i][j].append(self.indirect_choices[i][j].get())
        print(self.data_cont.ben.u_direct)
        print(self.data_cont.ben.u_indirect)
        print(self.data_cont.ben.u_res_rec)

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
        self.labels_direct = []
        labels_indirect = []
        labels_res_rec = []

        self.direct_choices = [[tk.StringVar() for x in range(len(self.data_cont.ben.direct[i]))]
                               for i in range(len(self.data_cont.plan_name))]
        for item in self.direct_choices:
            for var in item:
                var.set("1")
        self.indirect_choices = [[tk.StringVar()
                                  for x in range(len(self.data_cont.ben.indirect[i]))]
                                 for i in range(len(self.data_cont.plan_name))]
        for item in self.indirect_choices:
            for var in item:
                var.set("1")
        self.res_rec_choices = [[tk.StringVar() for x in range(len(self.data_cont.ben.res_rec[i]))]
                                for i in range(len(self.data_cont.plan_name))]
        for item in self.res_rec_choices:
            for var in item:
                var.set("1")

        for i in range(len(self.data_cont.plan_name)):
            row_index = 0
            group.append(ttk.LabelFrame(self, text=self.data_cont.plan_name[i]))
            group[-1].grid(row=3+i, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
            self.direct_range.append([])
            self.indirect_range.append([])
            self.res_rec_range.append([])
            for j in range(len(self.data_cont.ben.direct[i])):
                if self.data_cont.ben.direct[i][j][0] == "":
                    align = "w"
                    print_text = "No direct benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.ben.direct[i][j][0]
                    print_text += " - $" + self.data_cont.ben.direct[i][j][1]
                    add_rad = True
                self.labels_direct.append(ttk.Label(group[-1], text=print_text,
                                                    font=SMALL_FONT))
                self.labels_direct[-1].grid(row=row_index, column=0, sticky="w",
                                            padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1

                if add_rad:
                    rads = [tk.Radiobutton(group[-1],
                                           variable=self.direct_choices[i][j], value="None"),
                            tk.Radiobutton(group[-1],
                                           variable=self.direct_choices[i][j], value="Gauss"),
                            tk.Radiobutton(group[-1],
                                           variable=self.direct_choices[i][j], value="Tri"),
                            tk.Radiobutton(group[-1],
                                           variable=self.direct_choices[i][j], value="Rect")]
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
                    d_range_label = tk.Label(group[-1], text="Range/Standard Deviation:")
                    d_range_label.grid(row=row_index+3, column=1, sticky="e")
                    self.direct_range[i].append(tk.Entry(group[-1],
                                                         width=int(ENTRY_WIDTH/2), font=SMALL_FONT))
                    self.direct_range[i][j].grid(row=row_index+3, column=2, sticky="w",
                                                 padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4

            for j in range(len(self.data_cont.ben.indirect[i])):
                if self.data_cont.ben.indirect[i][j][0] == "":
                    align = "w"
                    print_text = "No indirect benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.ben.indirect[i][j][0] + " - $" + self.data_cont.ben.indirect[i][j][1]
                    add_rad = True

                labels_indirect.append(ttk.Label(group[-1], text=print_text,
                                                 font=SMALL_FONT))
                labels_indirect[-1].grid(row=row_index, column=0, sticky=align,
                                         padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1

                if add_rad:
                    rads = [tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j],
                                           value="None"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j],
                                           value="Gauss"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j],
                                           value="Tri"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j],
                                           value="Rect")]
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
                    i_range_label = tk.Label(group[-1], text="Range/Standard Deviation:")
                    i_range_label.grid(row=row_index+3, column=1, sticky="e")
                    self.indirect_range[i].append(tk.Entry(group[-1],
                                                           width=int(ENTRY_WIDTH/2),
                                                           font=SMALL_FONT))
                    self.indirect_range[i][j].grid(row=row_index+3, column=2, sticky="w",
                                                   padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4


            for j in range(len(self.data_cont.ben.res_rec[i])):
                if self.data_cont.ben.res_rec[i][j][0] == "":
                    align = "w"
                    print_text = "No response/recovery benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.ben.res_rec[i][j][0] + " - $" + self.data_cont.ben.res_rec[i][j][1]
                    add_rad = True

                labels_res_rec.append(ttk.Label(group[-1], text=print_text,
                                                font=SMALL_FONT))
                labels_res_rec[-1].grid(row=row_index, column=0, sticky=align,
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1

                if add_rad:
                    rads = [tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j],
                                           value="None"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j],
                                           value="Gauss"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j],
                                           value="Tri"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j],
                                           value="Rect")]
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
                    rr_range_label = tk.Label(group[-1], text="Range/Standard Deviation:")
                    rr_range_label.grid(row=row_index+3, column=1, sticky="e")
                    self.res_rec_range[i].append(tk.Entry(group[-1],
                                                          width=int(ENTRY_WIDTH/2),
                                                          font=SMALL_FONT))
                    self.res_rec_range[i][j].grid(row=row_index+3, column=2, sticky="w",
                                                  padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4
