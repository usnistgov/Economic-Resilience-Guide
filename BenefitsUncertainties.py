"""
   File:          BenefitsUncertainties.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for adding uncertainties to benefits,
                  the page for the user to input Benefits uncertainty distributions.
    * NOTE: This page is a prototype uncertainties page.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from BenefitsPage import BenefitsPage

from PlotsAndImages import none_dist, gauss_dist, tri_dist, rect_dist

from Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from Constants import ENTRY_WIDTH

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


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
        label = ttk.Label(self, text="The prototype uncertainties page.\n "
                                     "Need to add text here to explain uncertainties.\n"
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        # TODO: Update Label text
        label.grid(padx=10, pady=10, sticky="new")

        ben_lbl = tk.Label(self, text="Benefits Uncertainties", font=LARGE_FONT)
        ben_lbl.grid(row=2, sticky="w")
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
        self.add_button = ttk.Button(self, text="Update Uncertainties", command=self.add_uncertainty)
        self.add_button.grid(row=12, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=13, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=13, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

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

        plan_num = []            # === List that contains all selected plans
        #if self.b_bool.get():
        #    plan_num.append(0)
        #if self.p1_bool.get():
        #    plan_num.append(1)
        #if self.p2_bool.get():
        #    plan_num.append(2)
        #if self.p3_bool.get():
        #    plan_num.append(3)
        #if self.p4_bool.get():
        #    plan_num.append(4)
        #if self.p5_bool.get():
        #    plan_num.append(5)
        #if self.p6_bool.get():
        #    plan_num.append(6)

        # TODO: Save data

        if valid:
            # ===== Updates the page for the next cost
            self.update_prev_list()
            #messagebox.showinfo("Success", "Benefit has been successfully added!")
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted Benefits' Section"""
        pass
        #del self.choices[:]

        # === Prevents field duplication
        # TODO: Make this function
        #for i in range(len(self.data_cont.DirectBen)):
        #    for j in range(len(self.data_cont.DirectBen[i])):
        #        if self.data_cont.DirectBen[i][j][0] != "":
        #            if i == 0:
        #                plan_text = self.data_cont.DirectBen[i][j][0] + " - <Base Plan>"
        #            else:
        #                plan_text = self.data_cont.DirectBen[i][j][0] + " - <Plan " + str(i) + ">"
        #            if plan_text not in self.choices:
        #                self.choices.append(plan_text)

        #for i in range(len(self.data_cont.IndirectBen)):
        #    for j in range(len(self.data_cont.IndirectBen[i])):
        #        if self.data_cont.IndirectBen[i][j][0] != "":
        #            if i == 0:
        #                plan_text = self.data_cont.IndirectBen[i][j][0] + " - <Base Plan>"
        #            else:
        #                plan_text = self.data_cont.IndirectBen[i][j][0] + " - <Plan " + str(i) + ">"
        #            if plan_text not in self.choices:
        #                self.choices.append(plan_text)

        #for i in range(len(self.data_cont.ResRec)):
        #    for j in range(len(self.data_cont.ResRec[i])):
        #        if self.data_cont.ResRec[i][j][0] != "":
        #            if i == 0:
        #                plan_text = self.data_cont.ResRec[i][j][0] + " - <Base Plan>"
        #            else:
        #                plan_text = self.data_cont.ResRec[i][j][0] + " - <Plan " + str(i) + ">"
        #            if plan_text not in self.choices:
        #                self.choices.append(plan_text)

        #self.prev_bens.delete(0, tk.END)
        #self.prev_bens.insert(tk.END, "")
        #self.prev_bens.configure(values=self.choices)

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        #TODO: Fix this function
        err_messages = ""

        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        #if self.title_ent.get() == "" or self.title_ent.get() == "<enter a title for this benefit>":
        #    err_messages += "Title field has been left empty!\n\n"
        #    valid = False
        #d_text = "<enter a description for this benefit>"
        #if self.desc_ent.get("1.0", "end-1c") == "" or self.desc_ent.get("1.0", "end-1c") == d_text:
        #    self.desc_ent.delete('1.0', tk.END)
        #    self.desc_ent.insert(tk.END, "N/A")
        #any_plan_1 = self.p1_bool.get() or self.p2_bool.get() or self.p3_bool.get()
        #any_plan_2 = self.p4_bool.get() or self.p5_bool.get() or self.p6_bool.get()
        #if not (self.b_bool.get() or any_plan_1 or any_plan_2):
        #    err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
        #    valid = False
        #if self.choice.get() not in ["Direct", "Indirect", "ResRec"]:
        #    err_messages += "A 'Benefit Type' has not been selected!\n\n"
        #    valid = False

        # ===== Benefit cannot have a duplicate title
        #plan_num = []  # === List that contains all selected plans
        #if self.p1_bool.get():
        #    plan_num.append(1)
        #if self.p2_bool.get():
        #    plan_num.append(2)
        #if self.p3_bool.get():
        #    plan_num.append(3)
        #if self.p4_bool.get():
        #    plan_num.append(4)
        #if self.p5_bool.get():
        #    plan_num.append(5)
        #if self.p6_bool.get():
        #    plan_num.append(6)

        #for choice in self.choices:
        #    if (choice)[:len(self.title_ent.get())] == self.title_ent.get():
        #        if self.b_bool.get() and (choice)[len(self.title_ent.get()):] == " - <Base Plan>":
        #            err_messages += ("\"" + self.title_ent.get())
        #            err_messages += "\" is already used as a benefit title for the Base Plan. "
        #            err_messages += "Please input a different title.\n\n"
        #            valid = False

        #        for index in plan_num:
        #            if (choice)[len(self.title_ent.get()):] == " - <Plan " + str(index) + ">":
        #                err_messages += ("\"" + self.title_ent.get() + "\" is already ")
        #                err_messages += "used as a benefit title for Plan " + str(index)
        #                err_messages += ". Please input a different title.\n\n"
        #                valid = False

        # ===== Benefit Title must not have a hyphen '-'
        #if "-" in self.title_ent.get():
        #    err_messages += ("Title cannot have a hyphen \'-\'. Please change the title.\n\n")
        #    valid = False

        # ===== Dollar Amount must be a positive number
        #try:
        #    float(self.ben_ent.get())
        #except ValueError:
        #    err_messages += "Dollar value of the benefit must be a number. "
        #    err_messages += "Please enter an amount.\n\n"
        #    valid = False
        #if "-" in self.ben_ent.get():
        #    err_messages += "Dollar value must be a positive number. "
        #    err_messages += "Please enter a positive amount.\n\n"
        #    valid = False


        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return valid


    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""
        # TODO: Ensure that this works as expected/desired.

        group = []
        labels_direct = []
        labels_indirect = []
        labels_res_rec = []

        self.direct_choices = [[tk.StringVar() for x in range(len(self.data_cont.DirectBen[i]))] for i in range(len(self.data_cont.plan_name))]
        for item in self.direct_choices:
            for var in item:
                var.set("1")
        self.indirect_choices = [[tk.StringVar() for x in range(len(self.data_cont.IndirectBen[i]))] for i in range(len(self.data_cont.plan_name))]
        for item in self.indirect_choices:
            for var in item:
                var.set("1")
        self.res_rec_choices = [[tk.StringVar() for x in range(len(self.data_cont.ResRec[i]))] for i in range(len(self.data_cont.plan_name))]
        for item in self.res_rec_choices:
            for var in item:
                var.set("1")

        for i in range(len(self.data_cont.plan_name)):
            row_index = 0
            group.append(ttk.LabelFrame(self, text=self.data_cont.plan_name[i]))
            group[-1].grid(row=3+i, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
            for j in range(len(self.data_cont.DirectBen[i])):
                if self.data_cont.DirectBen[i][j][0] == "":
                    align = "w"
                    print_text = "No direct benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.DirectBen[i][j][0]
                    print_text += " - $" + self.data_cont.DirectBen[i][j][1]
                    add_rad = True
                labels_direct.append(ttk.Label(group[-1], text=print_text,
                                               font=SMALL_FONT))
                labels_direct[-1].grid(row=row_index, column=0, sticky="w",
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
                    self.direct_range = tk.Entry(group[-1], width=int(ENTRY_WIDTH/2), font=SMALL_FONT)
                    self.direct_range.grid(row=row_index+3, column=2, sticky="w",
                                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4

            for j in range(len(self.data_cont.IndirectBen[i])):
                if self.data_cont.IndirectBen[i][j][0] == "":
                    align = "w"
                    print_text = "No indirect benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.IndirectBen[i][j][0] + " - $" + self.data_cont.IndirectBen[i][j][1]
                    add_rad = True

                labels_indirect.append(ttk.Label(group[-1], text=print_text,
                                                 font=SMALL_FONT))
                labels_indirect[-1].grid(row=row_index, column=0, sticky=align,
                                         padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1

                if add_rad:
                    rads = [tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j], value="None"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j], value="Gauss"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j], value="Tri"),
                            tk.Radiobutton(group[-1], variable=self.indirect_choices[i][j], value="Rect")]
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
                    self.indirect_range = tk.Entry(group[-1], width=int(ENTRY_WIDTH/2), font=SMALL_FONT)
                    self.indirect_range.grid(row=row_index+3, column=2, sticky="w",
                                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4


            for j in range(len(self.data_cont.ResRec[i])):
                if self.data_cont.ResRec[i][j][0] == "":
                    align = "w"
                    print_text = "No response/recovery benefits associated with this plan."
                    add_rad = False
                else:
                    align = "w"
                    print_text = self.data_cont.ResRec[i][j][0] + " - $" + self.data_cont.ResRec[i][j][1]
                    add_rad = True

                labels_res_rec.append(ttk.Label(group[-1], text=print_text,
                                               font=SMALL_FONT))
                labels_res_rec[-1].grid(row=row_index, column=0, sticky=align,
                                       padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                row_index += 1

                if add_rad:
                    rads = [tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j], value="None"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j], value="Gauss"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j], value="Tri"),
                            tk.Radiobutton(group[-1], variable=self.res_rec_choices[i][j], value="Rect")]
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
                    self.res_rec_range = tk.Entry(group[-1], width=int(ENTRY_WIDTH/2), font=SMALL_FONT)
                    self.res_rec_range.grid(row=row_index+3, column=2, sticky="w",
                                           padx=FIELDX_PADDING, pady=FIELDY_PADDING)
                    row_index += 4

