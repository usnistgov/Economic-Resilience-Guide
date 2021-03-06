"""
   File:          BenefitsPage.py
   Author:        Shannon Grubb
   Description:   Interacts with EconGuide.py, builds the GUI for the BenefitsPage,
                  the page for the user to input Disaster-Related Benefits.
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
########################################## Benefits Class ##########################################
#
#
class BenefitsPage(tk.Frame):
    """
    GUI for the input of all Disaster-Related benefits.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="To add a benefit, input a "
                                     "title, amount, and description, the click"
                                     "'Add Benefit.' \n"
                                     "Note: these are only disaster-related benefits "
                                     "and do not consider fatalities averted.\n"
                                     "Fatalities averted will be recorded in a later page. "
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        ben_lbl = tk.Label(self, text="Add Benefits", font=LARGE_FONT)
        ben_lbl.grid(row=2, sticky="w")
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Cost Description Widgets
        group1 = ttk.LabelFrame(self, text="Benefit Description")
        group1.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        ttk.Label(group1, text="Title",
                  font=SMALL_FONT).grid(row=0, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.title_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.title_ent.insert(tk.END, "<enter a title for this benefit>")
        self.title_ent.grid(row=0, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ttk.Label(group1, text="Amount  $",
                  font=SMALL_FONT).grid(row=1, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.ben_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.ben_ent.insert(tk.END, "<enter dollar value for this benefit>")
        self.ben_ent.grid(row=1, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ttk.Label(group1, text="Description",
                  font=SMALL_FONT).grid(row=2, column=0, sticky="ne",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.desc_ent = tk.Text(group1, width=60, height=10, font=SMALL_FONT)
        self.desc_ent.insert(tk.END, "<enter a description for this benefit>")
        self.desc_ent.grid(row=2, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Associated Plan(s) Widgets
        group2 = ttk.LabelFrame(self, text="Plan Affected")
        group2.grid(row=3, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        ttk.Label(group2, text="Which plan(s) does this benefit pertain to?",
                  font=SMALL_FONT).grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)
        self.bools = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(),
                      tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]


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

        # ===== Benefit type widgets
        group3 = ttk.LabelFrame(self, text="Benefit Type")
        group3.grid(row=4, column=0, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        self.choice = tk.StringVar()
        self.choice.set("1")
        ttk.Label(group3,
                  text="Is this a Direct Loss Reduction, Indirect Loss Reduction, or\n"
                       "Response/Recovery Cost Reduction?",
                  font=SMALL_FONT).grid(row=0, column=0, sticky="ew",
                                        padx=BASE_PADDING, pady=BASE_PADDING)

        tk.Radiobutton(group3, text="Direct Reduction",
                       variable=self.choice, value="direct").grid(sticky="w")
        tk.Radiobutton(group3, text="Indirect Reduction",
                       variable=self.choice, value="indirect").grid(sticky="w")
        tk.Radiobutton(group3, text="Response/Recovery Reduction",
                       variable=self.choice, value="res-rec").grid(sticky="w")

        #self.choice.trace("w", self.on_trace_change)

        # ===== Interact with already-saved costs
        group4 = ttk.LabelFrame(self, text="Access Saved Benefits")
        group4.grid(row=4, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        ttk.Label(group4, text="Edit, copy, or delete saved benefits.",
                  font=SMALL_FONT).grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

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
            go_to_place = 'BenefitsUncertaintiesPage'
            moveon = self.add_ben(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'ExternalitiesUncertaintiesPage'
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
        save_button = ttk.Button(self, text="Save Analysis", command=self.data_cont.file_save)
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Benefit", command=self.add_ben)
        self.add_button.grid(row=5, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=6, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Menu", command=menu).grid(row=7, column=0, sticky="se",
                                                         padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        # NOTE: the _ before event designates it as an intentionally unused input
        self.update_prev_list()

    def show_info(self):
        """ Pulls up information for the Benefits page."""
        messagebox.showinfo("More Information",
                            "To add a benefit, a title and associated dollar value must be "
                            "provided. The description field is optional. "
                            "At least one ‘Plan Affected’ must be selected so that the benefit "
                            "will be assigned to the respective plan(s). The benefit ‘type’ must "
                            "be selected to determine the type of calculation to be made in the "
                            "analysis stage.\n\n"
                            "You may interact with saved benefits on the right side "
                            "by editing the associated information, copying the associated "
                            "information (for ease), or deleting the benefit all together.\n\n"
                            "The following benefit types are defined:\n"
                            "    Direct Reduction: The additional dollar amount of a cost that "
                            "would have directly affected the plan’s associated stakeholder(s) "
                            "had this plan NOT been implemented. Direct costs avoided.\n"
                            "    Indirect Reduction: The additional dollar amount of a cost that "
                            "would have affected individuals in the surrounding area or involved "
                            "with the stakeholder(s) had this plan NOT been implemented. Indirect "
                            "costs avoided.\n"
                            "    Response/recovery Reduction: The additional dollar amount of "
                            "disturbance-related responses/recoveries that are expected to have "
                            "applied had this plan NOT been implemented.\n")

    def add_ben(self, moveon=False):
        """Appends list of benefits, clears page's entry widgets,
           and updates 'Saved Benefits' section"""
        if moveon:
            [valid, blank, err_messages] = self.check_page(printout=False)
            if not valid | blank:
                checker = messagebox.askyesno('Move Forward?',
                                              'Your benefit was not saved. The following errors '
                                              + "were found:\n" + err_messages
                                              + 'Select \'No\' if you wish to continue editing'
                                              + ' and \'Yes\' if you wish to move to the '
                                              + 'next page.')
                return checker
            if blank:
                return True
        else:
            [valid, blank, err_messages] = self.check_page()
        if not valid:
            return False
        else:
            # ===== Updates the page for the next cost
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success", "Benefit has been successfully added!")
            return True

    def update_prev_list(self):
        """Updates ' Benefits' Section"""
        del self.choices[:]

        for plan in self.data_cont.plan_list:
            i = str(plan.num)
            for ben in plan.bens.indiv:
                choice_check = ben.title
                if i == "0" and ((choice_check + " - <Base Plan>") not in self.choices):
                    self.choices.append(choice_check + " - <Base Plan>")
                elif i != "0" and ((choice_check + " - <Plan " + i + ">") not in self.choices):
                    self.choices.append(choice_check + " - <Plan " + i + ">")

        self.prev_bens.delete(0, tk.END)
        self.prev_bens.insert(tk.END, "")
        self.prev_bens.configure(values=self.choices)

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
        new_amount = self.ben_ent.get()
        new_type = self.choice.get()
        if len(plan_num) == 0:
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            plan = self.data_cont.plan_list[0]
            [valid, blank, err_messages] = plan.bens.save(new_title, new_type, new_amount,
                                                          new_desc, err_messages, blank=True)
        else:
            for i in plan_num:
                plan = self.data_cont.plan_list[i]
                [valid, blank, err_messages] = plan.bens.save(new_title, new_type, new_amount,
                                                              new_desc, err_messages)

        if (not valid) & (not blank) & printout:
            messagebox.showerror("ERROR", err_messages)
        return [valid, blank, err_messages]

    def copy_ben(self):
        """Duplicates information of chosen cost and pastes it on screen"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select a benefit to continue.")
            return

        # === First index is benefit title, second index is plan number of corresponding benefit
        # === Cleans this up so that it could be used to find the first index of the chosen benefit
        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = chosen_ben[1].replace("Plan", '')
        chosen_ben[1] = chosen_ben[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_ben[1] = int(chosen_ben[1].replace("Base", '0'))

        old_plan = self.data_cont.plan_list[chosen_ben[1]]
        for ben in old_plan.bens.indiv:
            if ben.title == chosen_ben[0]:
                old_ben = ben

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, old_ben.title)
        self.ben_ent.delete(0, tk.END)
        self.ben_ent.insert(tk.END, '{:,.2f}'.format(old_ben.amount))
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, old_ben.desc)
        self.choice.set(old_ben.ben_type)



    def edit_ben(self):
        """Edits the chosen benefit and disables all 'previous benefits'
           functionality untill an appropriate action is taken"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select a benefit to continue.")
            return

        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = chosen_ben[1].replace("Plan", '')
        chosen_ben[1] = chosen_ben[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_ben[1] = int(chosen_ben[1].replace("Base", '0'))

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

        # ===== Alters the button layout to avoid conflicting actions.
        # ===== Enable user to take additional actions.
        self.prev_bens.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        self.add_button.configure(text="Edit Benefit", command=self.change_ben)

        self.cancel_button = ttk.Button(self, text="Cancel Edit", command=self.cancel_edit)
        self.cancel_button.grid(row=6, column=1, sticky="sw",
                                padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def delete_ben(self, is_updating):
        """Deletes a benefit entry"""
        if self.prev_bens.get() == "":
            messagebox.showerror("Error",
                                 "No previous benefit selected! "
                                 "Please select a benefit to continue.")
            return

        # === First index is benefit title, second index is plan number of corresponding benefit
        # === Cleans this up so that it could be used to find the first index of the chosen cost
        chosen_ben = (self.prev_bens.get()).split(" - ")
        chosen_ben[1] = chosen_ben[1].replace("Plan", '')
        chosen_ben[1] = chosen_ben[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_ben[1] = int(chosen_ben[1].replace("Base", '0'))

        def confirm():
            """Confirmation page to make sure the user really wants to delete the given benefit"""
            #popup = tk.Tk()

            def confirm_delete():
                """ Checks delete is confirmed and performs the deletion. """
                # ===== Removes the benefit from the list
                chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
                for ben in chosen_plan.bens.indiv:
                    if ben.title == chosen_ben[0]:
                        chosen_plan.bens.indiv.remove(ben)

                self.update_prev_list()

            chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
            for ben in chosen_plan.bens.indiv:
                if ben.title == chosen_ben[0]:
                    ben_amount = ben.amount
                    ben_desc = ben.desc
            del_text = ("Delete \'" + chosen_ben[0] + "\' from "
                        + self.data_cont.plan_list[chosen_ben[1]].name + " Plan ?\n\n"
                        + "Amount: $" + '{:,.2f}'.format(ben_amount)
                        + "\n\nDescription: " + str(ben_desc))
            confirm = messagebox.askokcancel("Confirmation", del_text)
            if confirm:
                confirm_delete()

        if not is_updating:
            # === Makes sure the user meant to delete the benefit
            confirm()
        else:
            # ===== Removes the cost from the list
            chosen_plan = self.data_cont.plan_list[chosen_ben[1]]
            for ben in chosen_plan.bens.indiv:
                if ben.title == chosen_ben[0]:
                    chosen_plan.bens.indiv.remove(ben)
            self.update_prev_list()

    def change_ben(self):
        """Deletes old instance of benefit and adds new instance"""
        self.prev_bens.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Benefit", command=self.add_ben)

        self.cancel_button.grid_remove()

        self.delete_ben(True)
        self.update_prev_list()
        self.add_ben()

        return

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
        self.ben_ent.insert(tk.END, "<enter dollar value for this benefit>")
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, "<enter a description for this benefit>")
        self.base.deselect()
        self.plan1.deselect()
        self.plan2.deselect()
        self.plan3.deselect()
        self.plan4.deselect()
        self.plan5.deselect()
        self.plan6.deselect()
        self.choice.set("1")


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
