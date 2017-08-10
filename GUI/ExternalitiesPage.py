"""
   File:          ExternalitiesPage.py
   Author:        Shannon Grubb
   Description:   Interacts with EconGuide.py, builds the GUI for the ExternalitiesPage,
                  the page for the user to input externalities.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.InfoPage import InfoPage

from GUI.Constants import SMALL_FONT, LARGE_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

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
        label = ttk.Label(self, text="To add an externality, input a "
                                     "title, amount and description, then"
                                     "click 'Add Externality.'\n"
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ext_lbl = tk.Label(self, text="Add Externalities", font=LARGE_FONT)
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

        ext_lbl = ttk.Label(group1, text="Amount  $", font=SMALL_FONT)
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

        self.bools = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(),
                      tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
        #self.b_bool = tk.BooleanVar()
        #self.p1_bool = tk.BooleanVar()
        #self.p2_bool = tk.BooleanVar()
        #self.p3_bool = tk.BooleanVar()
        #self.p4_bool = tk.BooleanVar()
        #self.p5_bool = tk.BooleanVar()
        #self.p6_bool = tk.BooleanVar()

        self.base = tk.Checkbutton(group2, text="Base scenario",
                                   variable=self.bools[0], font=SMALL_FONT)
        self.base.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan1 = tk.Checkbutton(group2, text="Plan 1", variable=self.bools[1], font=SMALL_FONT)
        self.plan1.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan2 = tk.Checkbutton(group2, text="Plan 2", variable=self.bools[2], font=SMALL_FONT)
        self.plan2.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan3 = tk.Checkbutton(group2, text="Plan 3", variable=self.bools[3], font=SMALL_FONT)
        self.plan3.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan4 = tk.Checkbutton(group2, text="Plan 4", variable=self.bools[4], font=SMALL_FONT)
        self.plan4.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan5 = tk.Checkbutton(group2, text="Plan 5", variable=self.bools[5], font=SMALL_FONT)
        self.plan5.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")
        self.plan6 = tk.Checkbutton(group2, text="Plan 6", variable=self.bools[6], font=SMALL_FONT)
        self.plan6.grid(padx=FIELDX_PADDING, pady=FIELDY_PADDING, sticky="w")

        # ===== Detects if a change occurs in the name fields on 'InfoPage'
        controller.frames[InfoPage].traces[0].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[1].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[2].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[3].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[4].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[5].trace("w", self.on_trace_change)
        #controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

        # ===== Sets third party affected
        def new_party_ext():
            """ Adds a new party to the list."""
            self.data_cont.plan_list[0].exts.parties.append(self.party_ent.get())

            self.third_parties.configure(values=self.data_cont.parties)


        group3 = ttk.LabelFrame(self, text="Third Party Affected")
        group3.grid(row=4, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        ttk.Label(group3, text="Add a party affected by the externality",
                  font=SMALL_FONT).grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        self.party_ent = tk.Entry(group3, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.party_ent.insert(tk.END, "<new third party option>")
        self.party_ent.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.new_party_button = ttk.Button(group3, text="Add Option", command=new_party_ext)
        self.new_party_button.grid(row=2, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.new_party = tk.StringVar()
        self.third_parties = ttk.Combobox(group3, textvariable=self.new_party, font=SMALL_FONT,
                                          width=ENTRY_WIDTH,
                                          values=self.data_cont.parties)
        self.third_parties.grid(row=3, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Interact with Saved externalities
        group4 = ttk.LabelFrame(self, text="Access Saved Externalities")
        group4.grid(row=5, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        hist_lbl = ttk.Label(group4, text="Edit, copy, or delete saved externalities",
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

        self.group_sign = ttk.LabelFrame(self, text="Positive or negative externality?")
        self.group_sign.grid(row=4, column=0, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        self.sign_select = tk.StringVar()
        self.sign_select.set("1")
        positive_rad = ttk.Radiobutton(self.group_sign, text="Positive", variable=self.sign_select, value="+")
        positive_rad.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        negative_rad = ttk.Radiobutton(self.group_sign, text="Negative", variable=self.sign_select, value="-")
        negative_rad.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.group5 = ttk.LabelFrame(self, text="One time or recurring externality?")
        self.group5.grid(row=5, column=0, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
        self.recur_selection = tk.StringVar()
        self.recur_selection.set("1")
        one_time_rad = ttk.Radiobutton(self.group5, text="One-Time Occurrence",
                                       variable=self.recur_selection, value="one-time")
        one_time_rad.grid(row = 1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        recurring_rad = ttk.Radiobutton(self.group5, text="Recurring Externality",
                                        variable = self.recur_selection, value="recurring")
        recurring_rad.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.recur_selection.trace("w", self.recur_trace_change)

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
        self.year_rate_ent.insert(tk.END, "<enter rate of occurrence in years>")
        self.year_rate_ent.grid(row=7, column=0, **pad_opts)
        self.year_rate_lbl2 = ttk.Label(self.group5, text="Year(s)", font=SMALL_FONT)
        self.year_rate_lbl2.grid(row=7, column=1, **pad_opts)

        self.year_rate_lbl.grid_remove()
        self.year_rate_ent.grid_remove()
        self.year_rate_lbl2.grid_remove()

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'ExternalitiesUncertaintiesPage'
            moveon = self.add_ext(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'CostsUncertaintiesPage'
            moveon = self.add_ext(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def menu():
            """ Tries to save the input and sends the user to the Directory Page.
            If save unsuccessful, asks user for verification to move on."""
            go_to_place = 'DirectoryPage'
            moveon = self.add_ext(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)


        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=self.data_cont.file_save)
        save_button.grid(row=0, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Externality", command=self.add_ext)
        self.add_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=7, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=7, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Menu", command=menu).grid(row=7, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.update_prev_list()

    def show_info(self):
        """ Pulls up information for the Externalities page."""
        messagebox.showinfo("More Information",
                            "To add an externality, a title and associated dollar value must be "
                            "provided. The description field is optional. "
                            "At least one ‘Plan Affected’ must be selected so that the "
                            "externality will be assigned to the respective plan(s). Whether or "
                            "not the externality is positive or negative must be assigned to "
                            "determine the sign on the calculations in the analysis stage. You "
                            "must also assign a party affected. There are predefined (common) "
                            "categories available for selection or you may write-in a party category.\n\n"
                            "You may interact with saved externalities on the right "
                            "side by editing the associated information, copying the associated "
                            "information (for ease), or deleting the externality all together.\n\n"
                            "Externalities are the inexplicit costs associated with a project. "
                            "Externalities do not affect the project or its stakeholders "
                            "directly, but affect the net worth of the project to the wider "
                            "community or others, such as members of a neighboring community. "
                            "Externalities may be positive or negative.\n\n"
                            "Examples of negative externalities include:\n"
                            "•	Noise disturbances\n"
                            "•	Landscape disturbances\n"
                            "•	Removal of ‘green spaces’\n"
                            "•	Slower traffic patterns\n\n"
                            "Examples of positive externalities include:\n"
                            "•	A neighborhood community center that can be used by members of "
                            "a neighboring community\n"
                            "•	In an area that does not have a public fire department, a "
                            "neighborhood that requires homeowners purchase private fire "
                            "protection services provide a positive externality to the "
                            "neighboring community, which is at reduced risk of the protected "
                            "neighborhood's fire spreading to their (unprotected) houses.")

    def add_ext(self, moveon=False):
        """Appends list of externalities, clears page's entry widgets,
           and updates 'Saved Externalities' section"""
        if moveon:
            [valid, blank, err_messages] = self.check_page(printout=False)
            if not (valid | blank):
                checker = messagebox.askyesno('Move Forward?',
                                              "Your externality was not saved. The following errors were found:\n"
                                              + err_messages
                                              + "Select \'No\' if you wish to continue editing and "
                                              "\'Yes\' if you wish to move to the next page.")
                return checker
            if blank:
                return True
        else:
            [valid, blank, err_messages] = self.check_page()
        if not valid:
            return False
        else:
            # ===== Updates the page for the next externality
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success", err_messages)
            return True

    def update_prev_list(self):
        """Updates 'Saved Externalities' Section"""
        del self.choices[:]

        for plan in self.data_cont.plan_list:
            for ext in plan.exts.indiv:
                if plan.num == 0:
                    to_add = ext.title + " - <Base Plan>"
                else:
                    to_add = ext.title + " - <Plan " + str(plan.num) + ">"
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

        # ===== Check which plan/plans to add to
        plan_num = []            # === List that contains all selected plans
        for boolean in self.bools:
            if boolean.get():
                plan_num.append(self.bools.index(boolean))

        new_title = self.title_ent.get()
        new_desc = self.desc_ent.get("0.0", tk.END)
        new_amount = self.ext_ent.get()
        new_type = self.recur_selection.get()
        new_times = [self.year_start_ent.get(), self.year_rate_ent.get(), 0]
        plus_minus = self.sign_select.get()
        party = self.new_party.get()
        if len(plan_num) == 0:
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            plan = self.data_cont.plan_list[0]
            [valid, blank, err_messages] = plan.exts.save(new_title, new_desc, new_amount,
                                                          new_type, new_times,
                                                          err_messages, plus_minus, party, blank=True)
        else:
            for i in plan_num:
                plan = self.data_cont.plan_list[i]
                [valid, blank, err_messages] = plan.exts.save(new_title, new_desc, new_amount,
                                                              new_type, new_times,
                                                              err_messages, plus_minus, party)

        if (not valid) & (not blank) & printout:
            messagebox.showerror("ERROR", err_messages)
        return [valid, blank, err_messages]

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

        chosen_plan = self.data_cont.plan_list[chosen_ext[1]]
        for ext in chosen_plan.exts.indiv:
            if ext.title == chosen_ext[0]:
                old_ext = ext

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, chosen_ext[0])
        self.ext_ent.delete(0, tk.END)
        self.ext_ent.insert(tk.END, '{:,.2f}'.format(old_ext.amount))
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, old_ext.desc)

        self.sign_select.set(old_ext.plus_minus)
        self.recur_selection.set(old_ext.ext_type)
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, old_ext.times[0])
        self.year_rate_ent.delete(0, tk.END)
        self.year_rate_ent.insert(tk.END, old_ext.times[1])

        self.new_party.set(old_ext.third_party)


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
            #popup = tk.Tk()

            def confirm_delete():
                """ Confirms that the user wishes to delete and then performs delete operation."""
                # ===== Removes the externality from the list
                chosen_plan = self.data_cont.plan_list[chosen_ext[1]]
                for ext in chosen_plan.exts.indiv:
                    if ext.title == chosen_ext[0]:
                        chosen_plan.exts.indiv.remove(ext)

                self.update_prev_list()

            chosen_plan = self.data_cont.plan_list[chosen_ext[1]]
            for ext in chosen_plan.exts.indiv:
                if ext.title == chosen_ext[0]:
                    ext_amount = ext.amount
                    ext_desc = ext.desc
            del_text = ("Delete \'" + chosen_ext[0] + "\' from " + self.data_cont.plan_list[chosen_ext[1]].name + " Plan?\n\n"
                        + "Amount: $" + '{:,.2f}'.format(ext_amount) + "\n\nDescription: " + str(ext_desc))
            confirm = messagebox.askokcancel("Confirmation", del_text)
            if confirm:
                confirm_delete()


        if not is_updating:
            confirm()       # === Makes sure the user meant to delete the externality
        else:
            chosen_plan = self.data_cont.plan_list[chosen_ext[1]]
            for ext in chosen_plan.exts.indiv:
                if ext.title == chosen_ext[0]:
                    chosen_plan.exts.indiv.remove(ext)

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
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, "<enter # of years after build year>")
        self.year_rate_ent.delete(0, tk.END)
        self.year_rate_ent.insert(tk.END, "<enter rate of occurrence in years>")
        self.recur_selection.set(1)
        self.sign_select.set(1)
        self.new_party.set('')
        self.base.deselect()
        self.plan1.deselect()
        self.plan2.deselect()
        self.plan3.deselect()
        self.plan4.deselect()
        self.plan5.deselect()
        self.plan6.deselect()

    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""

        # ===== Hides the widget until .grid() is called again
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
            self.plan2.configure(text=self.controller.frames[InfoPage].name_ents[1].get()
                                 +" (Plan 2)")
            self.plan2.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 2:
            self.plan3.configure(text=self.controller.frames[InfoPage].name_ents[2].get()
                                 +" (Plan 3)")
            self.plan3.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 3:
            self.plan4.configure(text=self.controller.frames[InfoPage].name_ents[3].get()
                                 +" (Plan 4)")
            self.plan4.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 4:
            self.plan5.configure(text=self.controller.frames[InfoPage].name_ents[4].get()
                                 +" (Plan 5)")
            self.plan5.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 5:
            self.plan6.configure(text=self.controller.frames[InfoPage].name_ents[5].get()
                                 +" (Plan 6)")
            self.plan6.grid()
        self.clear_page()

    def recur_trace_change(self, _name, _index, _mode):
        """Updates recurrence if things are changed."""
        if self.recur_selection.get() == "one-time":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid_remove()
            self.year_rate_ent.grid_remove()
            self.year_rate_lbl2.grid_remove()
        elif self.recur_selection.get() == "recurring":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid()
            self.year_rate_ent.grid()
            self.year_rate_lbl2.grid()
