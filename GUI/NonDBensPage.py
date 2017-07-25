"""
   File:          NonDBensPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the NonDBensPage,
                  the page for the user to input non-Disaster-Related Benefits.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.InfoPage import InfoPage
from GUI.AnalysisPage import run_main_page

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

from Data.ClassNonDBens import Benefit

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
        controller.frames[InfoPage].traces[0].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[1].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[2].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[3].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[4].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[5].trace("w", self.on_trace_change)
        #controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

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
                                       variable=self.non_d_ben_recurr_selection, value="one-time")
        one_time_rad.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        recurring_rad = ttk.Radiobutton(self.group5, text="Recurring Occurrence",
                                        variable=self.non_d_ben_recurr_selection, value="recurring")
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
            go_to_place = 'NonDBensUncertaintiesPage'
            moveon = self.add_ben(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'FatalitiesPage'
            moveon = self.add_ben(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def menu():
            """ Tries to save the input and sends the user to the Directory Page.
            If save unsuccessful, asks user for verification to move on."""
            go_to_place = 'DirectoryPage'
            moveon = self.add_ben(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=lambda: self.data_cont.file_save())
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Benefit", command=self.add_ben)
        self.add_button.grid(row=5, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=6, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Directory", command=menu).grid(row=7, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.update_prev_list()

    def show_info(self):
        """ Shows the information textbox for Non-Disaster related benefits."""
        messagebox.showinfo("More Information",
                            "To add a non-disaster related benefit, a title and associated "
                            "dollar value must be provided. The description field is optional. "
                            "At least one ‘Plan Affected’ must be selected so that the benefit "
                            "will be assigned to the respective plan(s).\n\n"
                            "You may interact with previously inputted non-disaster related "
                            "benefits on the right side by editing the associated information, "
                            "copying the associated information (for ease), or deleting the "
                            "externality all together.\n\n"
                            "Non-disaster related benefits are the inexplicit benefits of a given "
                            "project. These types of benefits may affect the project or its "
                            "stakeholders directly, but may generate benefits or conveniences "
                            "that could increase the project’s net worth to the wider community. "
                            "These benefits accrue even in the absence of a disturbance "
                            "occurrence.\n\n"
                            "Examples of such benefits include:\n"
                            "•	Reduced traffic time\n"
                            "•	Increased ‘green space’\n"
                            "•	Increased public recreational activity options,\n"
                            "•	Increased tourism, etc.\n")

    def add_ben(self, moveon=False):
        """Appends list of NonDBens, clears page's entry widgets,
           and updates 'Previously Inputted NonDBens' section"""
        if moveon:
            [valid, blank, err_messages] = self.check_page(printout=False)
            if not (valid | blank):
                checker = messagebox.askyesno('Move Forward?',
                                              'Your benefit was not saved. The following errors were found:\n'
                                              + err_messages
                                              + 'Select \'No\' if you wish to continue editing and'
                                              ' \'Yes\' if you wish to move to the next page.')
                return checker
            if blank:
                return True
        else:
            [valid, blank, err_messages] = self.check_page()
        if not valid:
            return False
        else:
            # ===== Updates the page for the next NonDBen
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success", err_messages)
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted NonDBens' Section"""
        del self.choices[:]

        for plan in self.data_cont.plan_list:
            i = str(plan.id_assign)
            for ben in plan.nond_bens.indiv:
                if i == "0" and ((ben.title + " - <Base Plan>") not in self.choices):
                    self.choices.append(ben.title + " - <Base Plan>")
                elif i != "0" and ((ben.title + " - <Plan " + i + ">") not in self.choices):
                    self.choices.append(ben.title + " - <Plan " + i + ">")

        self.prev_bens.delete(0, tk.END)
        self.prev_bens.insert(tk.END, "")
        self.prev_bens.configure(values=self.choices)

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        err_messages = ""
        valid = True

        plan_num = []
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

        new_title = self.title_ent.get()
        new_desc = self.desc_ent.get("0.0", tk.END)
        new_type = self.non_d_ben_recurr_selection.get()
        new_amount = self.ben_ent.get()
        new_times = [self.year_start_ent.get(), self.year_rate_ent.get(), 0]

        if len(plan_num) == 0:
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            plan = self.data_cont.plan_list[0]
            [valid, blank, err_messages] = plan.nond_bens.save(new_title, new_times, new_type, new_amount, new_desc, err_messages, blank=True)
        else:
            for i in plan_num:
                plan = self.data_cont.plan_list[i]
                [valid, blank, err_messages] = plan.nond_bens.save(new_title, new_times, new_type, new_amount, new_desc, err_messages)
                
        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return [valid, blank, err_messages]

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

        old_plan = self.data_cont.plan_list[chosen_ben[1]]
        for ben in old_plan.nond_bens.indiv:
            if ben.title == chosen_ben[0]:
                old_ben = ben

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, old_ben.title)
        self.ben_ent.delete(0, tk.END)
        self.ben_ent.insert(tk.END,old_ben.amount)
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END,old_ben.desc)
        self.non_d_ben_recurr_selection.set(old_ben.ben_type)
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, old_ben.times[0])
        if old_ben.ben_type == "recurring":
            self.year_rate_ent.delete(0, tk.END)
            self.year_rate_ent.insert(tk.END, old_ben.times[1])

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
                chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
                for ben in chosen_plan.nond_bens.indiv:
                    if ben.title == chosen_ben[0]:
                        chosen_plan.nond_bens.indiv.remove(ben)

                self.update_prev_list()
                popup.destroy()

            def cancel_delete():
                popup.destroy()

            chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
            for ben in chosen_plan.nond_bens.indiv:
                if ben.title == chosen_ben[0]:
                    ben_amount = ben.amount
                    ben_desc = ben.desc

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
            chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
            for ben in chosen_plan.nond_bens.indiv:
                if ben.title == chosen_ben[0]:
                    chosen_plan.nond_bens.indiv.remove(ben)

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
        self.non_d_ben_recurr_selection.set("recurring")
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, "<enter # of years after build year>")
        self.year_rate_ent.delete(0, tk.END)
        self.year_rate_ent.insert(tk.END, "<enter rate of occurence in years>")
        self.non_d_ben_recurr_selection.set("1")

    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""

        # ===== Hides the widget until .grid() is called again
        #self.plan1.configure(text=self.controller.frames[InfoPage].name_ents[0].get()+" (Plan 1)")
        self.plan1.grid_remove()
        self.plan2.grid_remove()
        self.plan3.grid_remove()
        self.plan4.grid_remove()
        self.plan5.grid_remove()
        self.plan6.grid_remove()

        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 0:
            self.plan1.configure(text=self.controller.frames[InfoPage].name_ents[0].get()
                                 +" (Plan 1)")
            self.plan1.grid()

        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 1:
            self.plan2.configure(text=self.controller.frames[InfoPage].name_ents[1].get()+" (Plan 2)")
            self.plan2.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 2:
            self.plan3.configure(text=self.controller.frames[InfoPage].name_ents[2].get()+" (Plan 3)")
            self.plan3.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 3:
            self.plan4.configure(text=self.controller.frames[InfoPage].name_ents[3].get()+" (Plan 4)")
            self.plan4.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 4:
            self.plan5.configure(text=self.controller.frames[InfoPage].name_ents[4].get()+" (Plan 5)")
            self.plan5.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 5:
            self.plan6.configure(text=self.controller.frames[InfoPage].name_ents[5].get()+" (Plan 6)")
            self.plan6.grid()

        self.year_start_lbl.configure(state="disabled")
        self.year_start_ent.configure(state="disabled")
        self.year_start_lbl2.configure(state="disabled")
        self.year_rate_lbl.grid_remove()
        self.year_rate_ent.grid_remove()
        self.year_rate_lbl2.grid_remove()

        if self.non_d_ben_recurr_selection.get() == "one-time":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid_remove()
            self.year_rate_ent.grid_remove()
            self.year_rate_lbl2.grid_remove()
        elif self.non_d_ben_recurr_selection.get() == "recurring":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid()
            self.year_rate_ent.grid()
            self.year_rate_lbl2.grid()
