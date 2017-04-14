"""
   File:          NonDBensPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the NonDBensPage,
                  the page for the user to input non-Disaster-Related Benefits.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from InfoPage import InfoPage
from AnalysisPage import run_main_page

from Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from Constants import ENTRY_WIDTH

#
#
############################### Non-disaster Related Benefits Class ###############################
#
#

class NonDBensPage(tk.Frame):
    """
    GUI for the input of all Non-Disaster-Related benefits.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Input individual Non-Disaster Related Benefits"
                                     " by including a title, cost,\n"
                                     "and description. When finished, click 'Next>>'",
                          font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ext_lbl = tk.Label(self, text="Non-disaster Related Benefits (Resilience Dividend)",
                           font=LARGE_FONT)
        ext_lbl.grid(row=2, sticky="w")
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== NonDBens Description Widgets
        group1 = ttk.LabelFrame(self, text="Benefit Description")
        group1.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        title_lbl = ttk.Label(group1, text="Title", font=SMALL_FONT)
        title_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.title_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.title_ent.insert(tk.END, "<enter a title for this benefit>")
        self.title_ent.grid(row=0, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ben_lbl = ttk.Label(group1, text="Amount  $", font=SMALL_FONT)
        ben_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.ben_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.ben_ent.insert(tk.END, "<enter an amount for this benefit>")
        self.ben_ent.grid(row=1, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        desc_lbl = ttk.Label(group1, text="Description", font=SMALL_FONT)
        desc_lbl.grid(row=2, column=0, sticky="ne", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.desc_ent = tk.Text(group1, width=60, height=10, font=SMALL_FONT)
        self.desc_ent.insert(tk.END, "<enter a description for this benefit>")
        self.desc_ent.grid(row=2, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Associated Plan(s) Widgets
        group2 = ttk.LabelFrame(self, text="Plan Affected")
        group2.grid(row=3, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        plan_lbl = ttk.Label(group2, text="Which plan(s) does this benefit pertain to?",
                             font=SMALL_FONT)
        plan_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        self.b_bool = tk.BooleanVar()
        self.p1_bool = tk.BooleanVar()
        self.p2_bool = tk.BooleanVar()
        self.p3_bool = tk.BooleanVar()
        self.p4_bool = tk.BooleanVar()
        self.p5_bool = tk.BooleanVar()
        self.p6_bool = tk.BooleanVar()


        self.base = tk.Checkbutton(group2, text="Base scenario",
                                   variable=self.b_bool, font=SMALL_FONT)
        self.base.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan1 = tk.Checkbutton(group2, text="Plan 1", variable=self.p1_bool, font=SMALL_FONT)
        self.plan1.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan2 = tk.Checkbutton(group2, text="Plan 2", variable=self.p2_bool, font=SMALL_FONT)
        self.plan2.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan3 = tk.Checkbutton(group2, text="Plan 3", variable=self.p3_bool, font=SMALL_FONT)
        self.plan3.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan4 = tk.Checkbutton(group2, text="Plan 4", variable=self.p4_bool, font=SMALL_FONT)
        self.plan4.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan5 = tk.Checkbutton(group2, text="Plan 5", variable=self.p5_bool, font=SMALL_FONT)
        self.plan5.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan6 = tk.Checkbutton(group2, text="Plan 6", variable=self.p6_bool, font=SMALL_FONT)
        self.plan6.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")

        # ===== Detects if a change occurs in the name fields on 'InfoPage'
        controller.frames[InfoPage].p1_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p2_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p3_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p4_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p5_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p6_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

        # ===== Allows for recurrence
        self.group5 = ttk.LabelFrame(self, text="Recurring Non-Disaster Related Benefits")
        self.group5.grid(row=4, column=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        non_d_ben_recurr_lbl = ttk.Label(self.group5,
                                         text="Choose how often this benefit will occur.",
                                         font=SMALL_FONT)
        non_d_ben_recurr_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        self.non_d_ben_recurr_selection = tk.StringVar()
        self.non_d_ben_recurr_selection.set("1")
        one_time_rad = ttk.Radiobutton(self.group5, text="One-Time Occurrence",
                                       variable=self.non_d_ben_recurr_selection, value="OneTime")
        one_time_rad.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        recurring_rad = ttk.Radiobutton(self.group5, text="Recurring",
                                        variable=self.non_d_ben_recurr_selection, value="Recurring")
        recurring_rad.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # === Changes upcoming fields depending on NDBR choice
        self.non_d_ben_recurr_selection.trace("w", self.on_trace_change)

        pad_opts = {'sticky':"w", 'padx':FIELDX_PADDING, 'pady':FIELDY_PADDING}
        self.year_start_lbl = ttk.Label(self.group5, text="Year of occurrence", font=SMALL_FONT)
        self.year_start_lbl.grid(row=4, column=0, **pad_opts)
        self.year_start_ent = tk.Entry(self.group5, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.year_start_ent.insert(tk.END, "<enter # of years after build year>")
        self.year_start_ent.grid(row=5, column=0, **pad_opts)
        self.year_start_lbl2 = ttk.Label(self.group5, text="Year(s)", font=SMALL_FONT)
        self.year_start_lbl2.grid(row=5, column=1, **pad_opts)

        self.year_rate_lbl = ttk.Label(self.group5, text="Rate of occurrence")
        self.year_rate_lbl.grid(row=6, column=0, **pad_opts)
        self.year_rate_ent = tk.Entry(self.group5, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.year_rate_ent.insert(tk.END, "<enter rate of occurence in years>")
        self.year_rate_ent.grid(row=7, column=0, **pad_opts)
        self.year_rate_lbl2 = ttk.Label(self.group5, text="Year(s)", font=SMALL_FONT)
        self.year_rate_lbl2.grid(row=7, column=1, **pad_opts)


        # ===== Interact with previously inputted externalities
        group4 = ttk.LabelFrame(self, text="Previously Inputted Benefits (optional)")
        group4.grid(row=4, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        hist_lbl = ttk.Label(group4, text="Interact with previously inputted Non-disaster\n"
                                          "related benefits", font=SMALL_FONT)
        hist_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        self.choices = []
        self.variable = tk.StringVar()
        self.prev_bens = ttk.Combobox(group4, textvariable=self.variable,
                                      font=SMALL_FONT, width=ENTRY_WIDTH, values=self.choices)
        self.prev_bens.insert(tk.END, "")
        self.prev_bens.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # === Updates the combobox whenever user hovers over it
        self.prev_bens.bind("<Enter>", self.hover)

        self.edit_button = ttk.Button(group4, text="Edit", command=self.edit_ben)
        self.edit_button.grid(row=3, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.copy_button = ttk.Button(group4, text="Copy Info", command=self.copy_ben)
        self.copy_button.grid(row=3, sticky="s", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.delete_button = ttk.Button(group4, text="Delete",
                                        command=lambda: self.delete_ben(False))
        self.delete_button.grid(row=3, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            moveon = self.add_ben(moveon=True)
            if moveon:
                run_main_page(self.data_cont)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'FatalitiesPage'
            moveon = self.add_ben(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=lambda: self.data_cont.save_info())
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Benefit", command=self.add_ben)
        self.add_button.grid(row=5, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=6, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Finish Calculations", command=save_and_next)
        finished_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        # ===== GOES TO MAIN PAGE

    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.update_prev_list()

    def show_info(self):
        """ Shows the information textbox for Non-Disaster related benefits."""
        messagebox.showinfo("More Information",
                            "        Non-disaster related benefits are the inexplicit"
                            " benefits of a particular project. They "
                            "may affect the project or its "
                            "stakeholders directly, but may generate benefits or "
                            "conveniences that could increase the project's"
                            " net worth to the wider community.\n\n"
                            "Examples of such benefits "
                            "include:\n    reduced traffic time,"
                            "\n    increased 'green space',\n"
                            "    increased public recreational activity "
                            "options,\n    increased tourism, and so on.\n\n"
                            "        This field is optional but is highly recommended"
                            " as these benefits indeed generate "
                            "notable advantages capable of increasing the overall"
                            " worth of a project, especially to "
                            "the environment and surrounding population.")

    def add_ben(self, moveon=False):
        """Appends list of NonDBens, clears page's entry widgets,
           and updates 'Previously Inputted NonDBens' section"""
        if moveon:
            valid = self.check_page(printout=False)
        else:
            valid = self.check_page()
        if not valid:
            if moveon:
                checker = messagebox.askyesno('Move Forward?',
                                              'Your benefit was not saved. '
                                              'Select \'No\' if you wish to continue editing and'
                                              ' \'Yes\' if you wish to move to the next page.')
                return checker
            return False

        # === List that contains all selected plans
        plan_num = []
        if self.b_bool.get():
            plan_num.append(0)
        if self.p1_bool.get():
            plan_num.append(1)
        if self.p2_bool.get():
            plan_num.append(2)
        if self.p3_bool.get():
            plan_num.append(3)
        if self.p4_bool.get():
            plan_num.append(4)
        if self.p5_bool.get():
            plan_num.append(5)
        if self.p6_bool.get():
            plan_num.append(6)

        for i in range(len(plan_num)):
            # ===== Removes the filler spaces previously placed
            if self.data_cont.NonDBen[plan_num[i]][0] == ["", "", "", "", "", ""]:
                self.data_cont.NonDBen[plan_num[i]].remove(["", "", "", "", "", ""])
            if self.non_d_ben_recurr_selection.get() == "OneTime":
                extend_by = [[self.title_ent.get(), self.ben_ent.get(), self.desc_ent.get("1.0", "end-1c"), "OneTime", self.year_start_ent.get(), ""]]
            elif self.non_d_ben_recurr_selection.get() == "Recurring":
                extend_by = [[self.title_ent.get(), self.ben_ent.get(), self.desc_ent.get("1.0", "end-1c"), "Recurring", self.year_start_ent.get(), self.year_rate_ent.get()]]
            self.data_cont.NonDBen[plan_num[i]].extend(extend_by)

        if valid:
            # ===== Updates the page for the next NonDBen
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success",
                                "Non-disaster Related Benefit has been successfully added!")
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted NonDBens' Section"""
        del self.choices[:]

        for i in range(len(self.data_cont.NonDBen)):
            # === Prevents field duplication
            for j in range(len(self.data_cont.NonDBen[i])):
                if self.data_cont.NonDBen[i][j][0] != "":
                    ben = self.data_cont.NonDBen[i][j][0]
                    base_in = (ben + " - <Base Plan>") not in self.choices
                    plan_in = (ben + " - <Plan " + str(i) + ">") not in self.choices
                    if i == 0 and base_in:
                        self.choices.append(self.data_cont.NonDBen[i][j][0] + " - <Base Plan>")
                    elif i != 0 and plan_in:
                        self.choices.append(self.data_cont.NonDBen[i][j][0] + " - <Plan " + str(i) + ">")

        self.prev_bens.delete(0, tk.END)
        self.prev_bens.insert(tk.END, "")
        self.prev_bens.configure(values=self.choices)

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        err_messages = ""
        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        if self.title_ent.get() == "" or self.title_ent.get() == "<enter a title for this benefit>":
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        end = "end-1c"
        if "," in self.desc_ent.get("1.0", "end-1c"):
            err_messages += ("Description cannot have a comma \',\'. Please change the decsription.\n\n")
            valid = False
        ben_desc = "<enter a description for this benefit>"
        if self.desc_ent.get("1.0", end) == "" or self.desc_ent.get("1.0", end) == ben_desc:
            self.desc_ent.delete('1.0', tk.END)
            self.desc_ent.insert(tk.END, "N/A")
        any_plan_1 = self.p1_bool.get() or self.p2_bool.get() or self.p3_bool.get()
        any_plan_2 = self.p4_bool.get() or self.p5_bool.get() or self.p6_bool.get()
        if not (self.b_bool.get() or any_plan_1 or any_plan_2):
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            valid = False

        # ===== NonDBen cannot have a duplicate title
        # === List that contains all selected plans
        plan_num = []
        if self.p1_bool.get():
            plan_num.append(1)
        if self.p2_bool.get():
            plan_num.append(2)
        if self.p3_bool.get():
            plan_num.append(3)
        if self.p4_bool.get():
            plan_num.append(4)
        if self.p5_bool.get():
            plan_num.append(5)
        if self.p6_bool.get():
            plan_num.append(6)

        for i in range(len(self.choices)):
            if (self.choices[i])[:len(self.title_ent.get())] == self.title_ent.get():
                base_in = (self.choices[i])[len(self.title_ent.get()):] == " - <Base Plan>"
                if self.b_bool.get() and base_in:
                    err_messages += ("\"" + self.title_ent.get() + "\"")
                    err_messages += "is already used as a benefit title for the Base Plan."
                    err_messages += " Please input a different title.\n\n"
                    valid = False

                for j in range(len(plan_num)):
                    plan_end = (self.choices[i])[len(self.title_ent.get()):]
                    if plan_end == " - <Plan " + str(plan_num[j]) + ">":
                        err_messages += ("\"" + self.title_ent.get() + "\"")
                        err_messages += " is already used as a benefit title for Plan "
                        err_messages += str(plan_num[j]) + ". Please input a different title.\n\n"
                        valid = False

        # ===== NonDBen Title must not have a hyphen '-'
        if "-" in self.title_ent.get():
            err_messages += ("Title cannot have a hyphen \'-\'. Please change the title.\n\n")
            valid = False

        # ===== Cost must be a positive number
        try:
            float(self.ben_ent.get())
        except ValueError:
            err_messages += "Dollar value of the benefit must be a number. "
            err_messages += "Please enter an amount.\n\n"
            valid = False
        if "-" in self.ben_ent.get():
            err_messages += "Benefit must be a positive number. Please enter a positive amount.\n\n"
            valid = False

        try:
            float(self.year_start_ent.get())
        except ValueError:
            err_messages += "Starting year must be number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.year_start_ent.get():
            err_messages += "Starting year must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False

        if self.non_d_ben_recurr_selection.get() == "Recurring":
            try:
                float(self.year_rate_ent.get())
            except ValueError:
                err_messages += "Recurring rate must be a number. Please enter an amount.\n\n"
                valid = False
            if "-" in self.year_start_ent.get():
                err_messages += "Recurring rate must be a positive number. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False

        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return valid

    def copy_ben(self):
        """Duplicates information of chosen benefit and pastes it on screen"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select an benefit to continue.")
            return

        # === First index is benefit title, second index is plan number of corresponding benefit
        # === Cleans this up so that it could be used to find the first index of the chosen benefit
        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = chosen_ben[1].replace("Plan", '')
        chosen_ben[1] = chosen_ben[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_ben[1] = chosen_ben[1].replace("Base", '0')
        chosen_ben[1] = int(chosen_ben[1])

        for i in range(len(self.data_cont.NonDBen[chosen_ben[1]])):
            if self.data_cont.NonDBen[chosen_ben[1]][i][0] == chosen_ben[0]:
                ben_amount = self.data_cont.NonDBen[chosen_ben[1]][i][1]
                ben_desc = self.data_cont.NonDBen[chosen_ben[1]][i][2]
                ben_type = self.data_cont.NonDBen[chosen_ben[1]][i][3]
                start_year = self.data_cont.NonDBen[chosen_ben[1]][i][4]
                if ben_type == "Recurring":
                    recur_freq = self.data_cont.NonDBen[chosen_ben[1]][i][5]

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, chosen_ben[0])
        self.ben_ent.delete(0, tk.END)
        self.ben_ent.insert(tk.END, ben_amount)
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, ben_desc)
        self.non_d_ben_recurr_selection.set(ben_type)
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, start_year)
        if ben_type == "Recurring":
            self.year_rate_ent.delete(0, tk.END)
            self.year_rate_ent.insert(tk.END, recur_freq)

    def edit_ben(self):
        """Edits the chosen benefit and disables all 'previous benefits'
           functionality untill an appropriate action is taken"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select an benefit to continue.")
            return

        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = chosen_ben[1].replace("Plan", '')
        chosen_ben[1] = chosen_ben[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_ben[1] = chosen_ben[1].replace("Base", '0')
        chosen_ben[1] = int(chosen_ben[1])

        # ===== Sets the check boxes to their appropriate selection/deselection
        self.clear_page()

        self.copy_ben()

        if chosen_ben[1] == 0:
            self.base.select()
        elif chosen_ben[1] == 1:
            self.plan1.select()
        elif chosen_ben[1] == 2:
            self.plan2.select()
        elif chosen_ben[1] == 3:
            self.plan3.select()
        elif chosen_ben[1] == 4:
            self.plan4.select()
        elif chosen_ben[1] == 5:
            self.plan5.select()
        elif chosen_ben[1] == 6:
            self.plan6.select()

        # ===== Alters the button layout to avoid conflicting actions
        # ===== Enable user to take additional actions
        self.prev_bens.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        self.add_button.configure(text="Edit Benefit", command=self.change_ben)

        self.cancel_button = ttk.Button(self, text="Cancel Edit", command=self.cancel_edit)
        self.cancel_button.grid(row=6, column=1, sticky="sw",
                                padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def delete_ben(self, is_updating):
        """Deletes a externality entry"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select a benefit to continue.")
            return

        # === First index is benefit title
        # === Second index is plan number of corresponding benefit
        # === Cleans this up so that it could be used to find the first index of the chosen benefit
        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = int(chosen_ben[1].replace("Plan", '').replace("<", '').replace(">", '').replace(" ", '').replace("Base", '0'))

        def confirm():
            """Confirmation page to make sure the user really wants to delete the given benefit"""
            popup = tk.Tk()

            def confirm_delete():
                # ===== Removes the externality from the list
                # === Places filler fields so that code operates properly (saving/opening)
                for i in range(len(self.data_cont.NonDBen[chosen_ben[1]])):
                    if self.data_cont.NonDBen[chosen_ben[1]][i][0] == chosen_ben[0]:
                        del self.data_cont.NonDBen[chosen_ben[1]][i]
                        if len(self.data_cont.NonDBen[chosen_ben[1]]) == 0:
                            self.data_cont.NonDBen[chosen_ben[1]].extend([["", "", "", "", "", ""]])

                self.update_prev_list()
                popup.destroy()

            def cancel_delete():
                popup.destroy()

            for i in range(len(self.data_cont.NonDBen[chosen_ben[1]])):
                if self.data_cont.NonDBen[chosen_ben[1]][i][0] == chosen_ben[0]:
                    ben_amount = self.data_cont.NonDBen[chosen_ben[1]][i][1]
                    ben_desc = self.data_cont.NonDBen[chosen_ben[1]][i][2]

            popup.wm_title("Confirmation")
            label_text = "Delete \'" + chosen_ben[0] + "\'?\n\nAmount: " + str(ben_amount) + "\n\nDescription: " + str(ben_desc)
            label = ttk.Label(popup, text=label_text, font=NORM_FONT)
            label.grid(padx=BASE_PADDING, pady=BASE_PADDING)

            confirm_button = ttk.Button(popup, text="OK", command=confirm_delete)
            confirm_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            cancel_button = ttk.Button(popup, text="Cancel", command=cancel_delete)
            cancel_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            popup.mainloop()


        if not is_updating:
            # === Makes sure the user meant to delete the benefit
            confirm()
        else:
            # ===== Removes the benefit from the list
            # ===== REPEATED CODE => find a way that won't require repetition
            # === Places filler fields so that code operates properly (saving/opening)
            for i in range(len(self.data_cont.NonDBen[chosen_ben[1]])):
                if self.data_cont.NonDBen[chosen_ben[1]][i][0] == chosen_ben[0]:
                    del self.data_cont.NonDBen[chosen_ben[1]][i]
                    if len(self.data_cont.NonDBen[chosen_ben[1]]) == 0:
                        self.data_cont.NonDBen[chosen_ben[1]].extend([["", "", "", "", "", ""]])

            self.update_prev_list()


    def change_ben(self):
        """Deletes old instance of externality and adds new instance"""
        self.prev_bens.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Benefit", command=self.add_ben)

        self.cancel_button.grid_remove()

        self.delete_ben(True)
        self.update_prev_list()
        self.add_ben()


    def cancel_edit(self):
        """Cancels 'edit mode' and returns to normal functionality"""
        self.prev_bens.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Benefit", command=self.add_ben)

        self.cancel_button.grid_remove()

        self.clear_page()


    def clear_page(self):
        """Clears the page and resets all fields"""
        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, "<enter a title for this benefit>")
        self.ben_ent.delete(0, tk.END)
        self.ben_ent.insert(tk.END, "<enter an amount for this benefit>")
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, "<enter a description for this benefit>")
        self.base.deselect()
        self.plan1.deselect()
        self.plan2.deselect()
        self.plan3.deselect()
        self.plan4.deselect()
        self.plan5.deselect()
        self.plan6.deselect()
        self.non_d_ben_recurr_selection.set("Recurring")
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, "<enter # of years after build year>")
        self.year_rate_ent.delete(0, tk.END)
        self.year_rate_ent.insert(tk.END, "<enter rate of occurence in years>")
        self.non_d_ben_recurr_selection.set("1")

    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""

        self.plan1.configure(text=self.controller.frames[InfoPage].name_1_ent.get() + " (Plan 1)")
        # ===== Hides the widget until .grid() is called again
        self.plan2.grid_remove()
        self.plan3.grid_remove()
        self.plan4.grid_remove()
        self.plan5.grid_remove()
        self.plan6.grid_remove()

        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 1:
            self.plan2.configure(text=self.controller.frames[InfoPage].name_2_ent.get()+" (Plan 2)")
            self.plan2.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 2:
            self.plan3.configure(text=self.controller.frames[InfoPage].name_3_ent.get()+" (Plan 3)")
            self.plan3.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 3:
            self.plan4.configure(text=self.controller.frames[InfoPage].name_4_ent.get()+" (Plan 4)")
            self.plan4.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 4:
            self.plan5.configure(text=self.controller.frames[InfoPage].name_5_ent.get()+" (Plan 5)")
            self.plan5.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 5:
            self.plan6.configure(text=self.controller.frames[InfoPage].name_6_ent.get()+" (Plan 6)")
            self.plan6.grid()

        self.year_start_lbl.configure(state="disabled")
        self.year_start_ent.configure(state="disabled")
        self.year_start_lbl2.configure(state="disabled")
        self.year_rate_lbl.grid_remove()
        self.year_rate_ent.grid_remove()
        self.year_rate_lbl2.grid_remove()

        if self.non_d_ben_recurr_selection.get() == "OneTime":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid_remove()
            self.year_rate_ent.grid_remove()
            self.year_rate_lbl2.grid_remove()
        elif self.non_d_ben_recurr_selection.get() == "Recurring":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid()
            self.year_rate_ent.grid()
            self.year_rate_lbl2.grid()
