"""
   File:          ExternalitiesPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the ExternalitiesPage,
                  the page for the user to input externalities.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from InfoPage import InfoPage

from Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from Constants import ENTRY_WIDTH

#
#
####################################### Externalities Class #######################################
#
#
class ExternalitiesPage(tk.Frame):
    """
    GUI for the input of all externalities.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Input individual externalities by including a "
                                     "title, cost, and description.\n"
                                     "To add another externality, click 'Add Externality'. "
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ext_lbl = tk.Label(self, text="Externalities", font=LARGE_FONT)
        ext_lbl.grid(row=2, sticky="w")
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Externality Description Widgets
        group1 = ttk.LabelFrame(self, text="Externality Description")
        group1.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        title_lbl = ttk.Label(group1, text="Title", font=SMALL_FONT)
        title_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.title_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.title_ent.insert(tk.END, "<enter a title for this externality>")
        self.title_ent.grid(row=0, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ext_lbl = ttk.Label(group1, text="Cost  $", font=SMALL_FONT)
        ext_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.ext_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.ext_ent.insert(tk.END, "<enter an amount for this externality>")
        self.ext_ent.grid(row=1, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        desc_lbl = ttk.Label(group1, text="Description", font=SMALL_FONT)
        desc_lbl.grid(row=2, column=0, sticky="ne", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.desc_ent = tk.Text(group1, width=60, height=10, font=SMALL_FONT)
        self.desc_ent.insert(tk.END, "<enter a description for this externality>")
        self.desc_ent.grid(row=2, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Associated Plan(s) Widgets
        group2 = ttk.LabelFrame(self, text="Plan Affected")
        group2.grid(row=3, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        plan_lbl = ttk.Label(group2, text="Which plan(s) does this externality pertain to?",
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

        # ===== Interact with previously inputted externalities
        group4 = ttk.LabelFrame(self, text="Previously Inputted Externalities (optional)")
        group4.grid(row=4, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        hist_lbl = ttk.Label(group4, text="Interact with previously inputted externalities",
                             font=SMALL_FONT)
        hist_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        self.choices = []
        self.variable = tk.StringVar()
        self.prev_exts = ttk.Combobox(group4, textvariable=self.variable,
                                      font=SMALL_FONT, width=ENTRY_WIDTH, values=self.choices)
        self.prev_exts.insert(tk.END, "")
        self.prev_exts.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # === Updates the combobox whenever user hovers over it
        self.prev_exts.bind("<Enter>", self.hover)

        self.edit_button = ttk.Button(group4, text="Edit", command=self.edit_ext)
        self.edit_button.grid(row=3, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.copy_button = ttk.Button(group4, text="Copy Info", command=self.copy_ext)
        self.copy_button.grid(row=3, sticky="s", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.delete_button = ttk.Button(group4, text="Delete",
                                        command=lambda: self.delete_ext(False))
        self.delete_button.grid(row=3, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'BenefitsPage'
            moveon = self.add_ext(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'CostPage'
            moveon = self.add_ext(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)


        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=lambda: self.data_cont.save_info())
        save_button.grid(row=0, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Externality", command=self.add_ext)
        self.add_button.grid(row=5, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=6, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.update_prev_list()

    def show_info(self):
        """ Pulls up information for the Externalities page."""
        messagebox.showinfo("More Information",
                            "        Externalities are the inexplicit costs of a "
                            "particular project. They do not generally "
                            "affect the project or its stakeholders directly, "
                            "but may pose inconveniences or "
                            "disturbances that could diminish the project's net worth to the wider community.\n\n"
                            "Examples of externalities "
                            "include:\n    noise-disturbances,\n    landscape disturbances,\n"
                            "    removal of 'green space',\n    slower "
                            "traffic patterns, and so on.\n\n"
                            "        This field is optional but is highly recommended as "
                            "externalities indeed generate "
                            "obstacles capable of diminishing the overall worth of a project,"
                            " especially to "
                            "the environment and surrounding population.")

    def add_ext(self, moveon=False):
        """Appends list of externalities, clears page's entry widgets,
           and updates 'Previously Inputted Externalities' section"""
        if moveon:
            valid = self.check_page(printout=False)
        else:
            valid = self.check_page()
        if not valid:
            if moveon:
                checker = messagebox.askyesno('Move Forward?',
                                              "Your externality was not saved. "
                                              "Select \'No\' if you wish to continue editing and "
                                              "\'Yes\' if you wish to move to the next page.")
                return checker
            return False

        plan_num = []            # === List that contains all selected plans
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

        for plan in plan_num:
            # ===== Removes the filler spaces previously placed
            if self.data_cont.Externalities[plan][0] == ["", "", ""]:
                self.data_cont.Externalities[plan].remove(["", "", ""])
            extend_by = [[self.title_ent.get(), self.ext_ent.get(),
                          self.desc_ent.get("1.0", "end-1c")]]
            self.data_cont.Externalities[plan].extend(extend_by)


        if valid:
            # ===== Updates the page for the next externality
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success", "Externality has been successfully added!")
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted Externalities' Section"""
        del self.choices[:]

        for i in range(len(self.data_cont.Externalities)):
            for j in range(len(self.data_cont.Externalities[i])):
                if self.data_cont.Externalities[i][j][0] != "":
                    # === Prevents field duplication
                    if i == 0:
                        to_add = self.data_cont.Externalities[i][j][0] + " - <Base Plan>"
                    else:
                        to_add = self.data_cont.Externalities[i][j][0] + " - <Plan " + str(i) + ">"
                    if to_add not in self.choices:
                        self.choices.append(to_add)

        self.prev_exts.delete(0, tk.END)
        self.prev_exts.insert(tk.END, "")
        self.prev_exts.configure(values=self.choices)

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        err_messages = ""

        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        if self.title_ent.get() == "" or self.title_ent.get() == "<enter a title for this externality>":
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        if "," in self.desc_ent.get("1.0", "end-1c"):
            err_messages += ("Description cannot have a comma \',\'. Please change the decsription.\n\n")
            valid = False
        if self.desc_ent.get("1.0", "end-1c") == "" or self.desc_ent.get("1.0", "end-1c") == "<enter a description for this externality>":
            self.desc_ent.delete('1.0', tk.END)
            self.desc_ent.insert(tk.END, "N/A")
        if not (self.b_bool.get() or self.p1_bool.get() or self.p2_bool.get() or self.p3_bool.get() or self.p4_bool.get() or self.p5_bool.get() or self.p6_bool.get()):
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            valid = False

        # ===== Externality cannot have a duplicate title
        plan_num = []  # === List that contains all selected plans
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

        for choice in self.choices:
            if (choice)[:len(self.title_ent.get())] == self.title_ent.get():
                if self.b_bool.get() and (choice)[len(self.title_ent.get()):] == " - <Base Plan>":
                    err_messages += ("\"" + self.title_ent.get() + "\" is already ")
                    err_messages += "used as a externality title for the Base Plan. "
                    err_messages += "Please input a different title.\n\n"
                    valid = False

                for plan in plan_num:
                    if (choice)[len(self.title_ent.get()):] == " - <Plan " + str(plan) + ">":
                        err_messages += ("\"" + self.title_ent.get() + "\" is already ")
                        err_messages += ("used as a externality title for Plan " + str(plan))
                        err_messages += ". Please input a different title.\n\n"
                        valid = False

        # ===== Externality Title must not have a hyphen '-'
        if "-" in self.title_ent.get():
            err_messages += "Title cannot have a hyphen \'-\'. Please change the title.\n\n"
            valid = False

        # ===== Cost must be a positive number
        try:
            float(self.ext_ent.get())
        except ValueError:
            err_messages += "Dollar value of the externality must be a number. "
            err_messages += "Please enter an amount.\n\n"
            valid = False
        if "-" in self.ext_ent.get():
            err_messages += "Externality must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False


        if (not valid) & printout:
            messagebox.showerror("ERROR", err_messages)
        return valid

    def copy_ext(self):
        """Duplicates information of chosen externality and pastes it on screen"""
        if self.prev_exts.get() == "":
            messagebox.showerror("Error",
                                 "No previous externality selected! "
                                 "Please select an externality to continue.")
            return

        # === First index is externality title
        # === Second index is plan number of corresponding externality
        chosen_ext = (self.prev_exts.get()).split(" - ")
        # === Cleans this up so that it can be used to find the
        #     first index of the chosen externality
        chosen_ext[1] = int(chosen_ext[1].replace("Plan", '').replace("<", '').replace(">", '').replace(" ", '').replace("Base", '0'))

        for i in range(len(self.data_cont.Externalities[chosen_ext[1]])):
            if self.data_cont.Externalities[chosen_ext[1]][i][0] == chosen_ext[0]:
                ext_amount = self.data_cont.Externalities[chosen_ext[1]][i][1]
                ext_desc = self.data_cont.Externalities[chosen_ext[1]][i][2]

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, chosen_ext[0])
        self.ext_ent.delete(0, tk.END)
        self.ext_ent.insert(tk.END, ext_amount)
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, ext_desc)


    def edit_ext(self):
        """Edits the chosen externality and disables all 'previous externalities'
           functionality untill an appropriate action is taken"""
        if self.prev_exts.get() == "":
            messagebox.showerror("Error",
                                 "No previous externality selected! "
                                 "Please select an externality to continue.")
            return

        chosen_ext = (self.prev_exts.get()).split(" - ")
        chosen_ext[1] = int(chosen_ext[1].replace("Plan", '').replace("<", '').replace(">", '').replace(" ", '').replace("Base", '0'))

        # ===== Sets the check boxes to their appropriate selection/deselection
        self.clear_page()

        self.copy_ext()

        if chosen_ext[1] == 0:
            self.base.select()
        elif chosen_ext[1] == 1:
            self.plan1.select()
        elif chosen_ext[1] == 2:
            self.plan2.select()
        elif chosen_ext[1] == 3:
            self.plan3.select()
        elif chosen_ext[1] == 4:
            self.plan4.select()
        elif chosen_ext[1] == 5:
            self.plan5.select()
        elif chosen_ext[1] == 6:
            self.plan6.select()

        # ===== Alters the button layout to avoid conflicting actions
        # ===== Enables user to take additional actions
        self.prev_exts.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        self.add_button.configure(text="Edit Externality", command=self.change_ext)

        self.cancel_button = ttk.Button(self, text="Cancel Edit", command=self.cancel_edit)
        self.cancel_button.grid(row=6, column=1, sticky="sw",
                                padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def delete_ext(self, is_updating):
        """Deletes a externality entry"""
        if self.prev_exts.get() == "":
            messagebox.showerror("Error",
                                 "No previous externality selected! "
                                 "Please select an externality to continue.")
            return

        # === First index is externality title
        # === Second index is plan number of corresponding externality
        chosen_ext = (self.prev_exts.get()).split(" - ")
        # === Cleans this up so that it could be used to find the first index of the chosen cost
        chosen_ext[1] = int(chosen_ext[1].replace("Plan", '').replace("<", '').replace(">", '').replace(" ", '').replace("Base", '0'))

        def confirm():
            """Confirmation page to make sure the user wants to delete the given externality"""
            popup = tk.Tk()

            def confirm_delete():
                """ Confirms that the user wishes to delete and then performs delete operation."""
                # ===== Removes the externality from the list
                for i in range(len(self.data_cont.Externalities[chosen_ext[1]])):
                    if self.data_cont.Externalities[chosen_ext[1]][i][0] == chosen_ext[0]:
                        del self.data_cont.Externalities[chosen_ext[1]][i]
                        # === Places filler fields so that code operates properly (saving/opening)
                        if len(self.data_cont.Externalities[chosen_ext[1]]) == 0:
                            self.data_cont.Externalities[chosen_ext[1]].extend([["", "", ""]])

                self.update_prev_list()
                popup.destroy()

            def cancel_delete():
                """ Cancels the delete operation."""
                popup.destroy()

            for i in range(len(self.data_cont.Externalities[chosen_ext[1]])):
                if self.data_cont.Externalities[chosen_ext[1]][i][0] == chosen_ext[0]:
                    ext_amount = self.data_cont.Externalities[chosen_ext[1]][i][1]
                    ext_desc = self.data_cont.Externalities[chosen_ext[1]][i][2]

            popup.wm_title("Confirmation")
            label = ttk.Label(popup, text="Delete \'" + chosen_ext[0] + "\'?\n\nAmount: " + str(ext_amount) + "\n\nDescription: " + str(ext_desc), font=NORM_FONT)
            label.grid(padx=BASE_PADDING, pady=BASE_PADDING)

            confirm_button = ttk.Button(popup, text="OK", command=confirm_delete)
            confirm_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            cancel_button = ttk.Button(popup, text="Cancel", command=cancel_delete)
            cancel_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            popup.mainloop()


        if not is_updating:
            confirm()       # === Makes sure the user meant to delete the externality
        else:
            # ===== Removes the externality from the list
            #===== REPEATED CODE => find a way that won't require repetition
            for i in range(len(self.data_cont.Externalities[chosen_ext[1]])):
                if self.data_cont.Externalities[chosen_ext[1]][i][0] == chosen_ext[0]:
                    del self.data_cont.Externalities[chosen_ext[1]][i]
                    # === Places filler fields so that code operates properly
                    if len(self.data_cont.Externalities[chosen_ext[1]]) == 0:
                        self.data_cont.Externalities[chosen_ext[1]].extend([["", "", ""]])

            self.update_prev_list()


    def change_ext(self):
        """Deletes old instance of externality and adds new instance"""
        self.prev_exts.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Externality", command=self.add_ext)

        self.cancel_button.grid_remove()

        self.delete_ext(True)
        self.update_prev_list()
        self.add_ext()


    def cancel_edit(self):
        """Cancels 'edit mode' and returns to normal functionality"""
        self.prev_exts.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Externality", command=self.add_ext)

        self.cancel_button.grid_remove()

        self.clear_page()


    def clear_page(self):
        """Clears the page and resets all fields"""
        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, "<enter a title for this externality>")
        self.ext_ent.delete(0, tk.END)
        self.ext_ent.insert(tk.END, "<enter an amount for this externality>")
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, "<enter a description for this externality>")
        self.base.deselect()
        self.plan1.deselect()
        self.plan2.deselect()
        self.plan3.deselect()
        self.plan4.deselect()
        self.plan5.deselect()
        self.plan6.deselect()

    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""

        self.plan1.configure(text=self.controller.frames[InfoPage].name_1_ent.get()+" (Plan 1)")
        self.plan2.grid_remove()  # ===== Hides the widget until .grid() is called again
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
