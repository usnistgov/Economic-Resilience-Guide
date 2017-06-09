"""
   File:          CostPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the CostPage,
                  the page for the user to input Costs.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

import numpy as np

from GUI.InfoPage import InfoPage

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

from Data.ClassCosts import Cost

#
#
########################################### Costs Class ###########################################
#
#
class CostPage(tk.Frame):
    """
    GUI for the input of all Costs.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Input individual costs by including a "
                                     "title, cost, and description. "
                                     "Note: these are not \n"
                                     "externalities. To add another cost, click 'Add Cost'. "
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        cost_lbl = tk.Label(self, text="Costs", font=LARGE_FONT)
        cost_lbl.grid(row=2, sticky="w")

        self.create_widgets(controller)


    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Cost Description Widgets
        group1 = ttk.LabelFrame(self, text="Cost Description")
        group1.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        title_lbl = ttk.Label(group1, text="Title", font=SMALL_FONT)
        title_lbl.grid(row=0, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.title_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.title_ent.insert(tk.END, "<enter a title for this cost>")
        self.title_ent.grid(row=0, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        cost_lbl = ttk.Label(group1, text="Cost  $", font=SMALL_FONT)
        cost_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.cost_ent = tk.Entry(group1, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.cost_ent.insert(tk.END, "<enter an amount for this cost>")
        self.cost_ent.grid(row=1, column=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        desc_lbl = ttk.Label(group1, text="Description", font=SMALL_FONT)
        desc_lbl.grid(row=2, column=0, sticky="ne", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.desc_ent = tk.Text(group1, width=60, height=10, font=SMALL_FONT)
        self.desc_ent.insert(tk.END, "<enter a description for this cost>")
        self.desc_ent.grid(row=2, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Associated Plan(s) Widgets
        group2 = ttk.LabelFrame(self, text="Plan Affected")
        group2.grid(row=3, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        plan_lbl = ttk.Label(group2, text="Which plan(s) does this cost pertain to?",
                             font=SMALL_FONT)
        plan_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

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
        controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

        # ===== Cost type widgets
        group3 = ttk.LabelFrame(self, text="Kind of Cost")
        group3.grid(row=4, column=0, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)
#        self.scrollbar = Scrollbar(self)
#        self.scrollbar.grid_configure(group3)

        self.choice = tk.StringVar()
        self.choice.set("1")
        did_lbl = ttk.Label(group3,
                            text="Is this an Immediate Direct Cost, Immediate Indirect Cost, "
                                 "or an Operation,\nManagement, or Repairs (OMR) Cost?",
                            font=SMALL_FONT)
        did_lbl.grid(row=0, column=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        direct_rad = tk.Radiobutton(group3, text="Immediate Direct",
                                    variable=self.choice, value="direct")
        direct_rad.grid(sticky="w")
        indirect_rad = tk.Radiobutton(group3, text="Immediate Indirect",
                                      variable=self.choice, value="indirect")
        indirect_rad.grid(sticky="w")
        omr_rad = tk.Radiobutton(group3, text="Operation, Management, or Repairs Cost",
                                 variable=self.choice, value="omr")
        omr_rad.grid(sticky="w")

        self.choice.trace("w", self.on_trace_change)

        # ===== Interact with previously inputted costs
        group4 = ttk.LabelFrame(self, text="Previously Inputted Costs (optional)")
        group4.grid(row=4, column=1, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        hist_lbl = ttk.Label(group4, text="Interact with previously inputted costs",
                             font=SMALL_FONT)
        hist_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        self.choices = []
        self.variable = tk.StringVar()
        self.prev_costs = ttk.Combobox(group4, textvariable=self.variable,
                                       font=SMALL_FONT, width=ENTRY_WIDTH, values=self.choices)
        self.prev_costs.insert(tk.END, "")
        self.prev_costs.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        self.prev_costs.bind("<Enter>", self.hover)

        self.edit_button = ttk.Button(group4, text="Edit", command=self.edit_cost)
        self.edit_button.grid(row=3, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.copy_button = ttk.Button(group4, text="Copy Info", command=self.copy_cost)
        self.copy_button.grid(row=3, sticky="s", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.delete_button = ttk.Button(group4, text="Delete",
                                        command=lambda: self.delete_cost(False))
        self.delete_button.grid(row=3, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== OMR Details
        self.group5 = ttk.LabelFrame(self, text="OMR Details")
        self.group5.grid(row=5, column=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        omr_lbl = ttk.Label(self.group5,
                            text="Choose what kind of OMR cost this is and its specifics",
                            font=SMALL_FONT)
        omr_lbl.grid(row=0, sticky="ew", padx=BASE_PADDING, pady=BASE_PADDING)

        self.omr_selection = tk.StringVar()
        self.omr_selection.set("1")
        one_time_rad = ttk.Radiobutton(self.group5, text="One-Time Occurrence",
                                       variable=self.omr_selection, value="one-titme")
        one_time_rad.grid(row=1, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        recurring_rad = ttk.Radiobutton(self.group5, text="Recurring",
                                        variable=self.omr_selection, value="recurring")
        recurring_rad.grid(row=2, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # === Changes upcoming fields depending on OMR choice
        self.omr_selection.trace("w", self.on_trace_change)

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

        self.group5.grid_remove()

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'CostsUncertaintiesPage'
            moveon = self.add_cost(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'InfoPage'
            moveon = self.add_cost(moveon=True)
            if moveon:
                controller.show_frame(go_to_place)


        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis",
                                 command=lambda: self.data_cont.file_save())
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Add Cost", command=self.add_cost)
        self.add_button.grid(row=6, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=7, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=7, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.update_prev_list()

    def show_info(self):
        """ Pulls up information for the Cost page."""
        messagebox.showinfo("More Information",
                            "        To add a cost, a title and dollar value must be given. "
                            "The description is optional.\n\n"
                            "        At least one 'Plan Affected' must be selected so that "
                            "the cost will be assigned to the "
                            "respective plan(s). The type of cost must be selected "
                            "in order to determine what kind "
                            "of calculation will be made in the analysis of this plan.\n\n"
                            "        You may interact with previously inputted costs "
                            "on the right hand side by editing their "
                            "information, copying their information (for ease), "
                            "or deleting the cost altogether.\n\n"
                            "The following types of costs are defined:\n"
                            "    Immediate Direct:\n            "
                            "Costs that affect the immediate stakeholders as soon as the "
                            "corresponding plan is implemented "
                            "(such as building/construction costs).\n\n"
                            "    Immediate Indirect:\n            "
                            "Costs affecting users that have some form of dependency on "
                            "either the stakeholder(s) or the environment surrounding "
                            "the project's implementation area.\n\n"
                            "    Operation, Management, Maintenance, or Repair (OMR):\n            "
                            "Costs that take effect years after the implementation "
                            "date of the corresponding plan. These can be "
                            "one-time or recurring costs.")

    def add_cost(self, moveon=False):
        """Appends list of costs, clears page's entry widgets,
            and updates 'Previously Inputted Costs' section"""
        if moveon:
            valid = self.check_page(printout=False)
        else:
            valid = self.check_page()
        if not valid:
            if moveon:
                checker = messagebox.askyesno('Move Forward?',
                                              'Your cost was not saved. '
                                              'Select \'No\' if you wish to continue editing '
                                              'and \'Yes\' if you wish to move to the next page.')
                return checker
            return False

        plan_num = []            # === List that contains all selected plans
        for i in range(len(self.bools)):
            if self.bools[i].get():
                plan_num.append(i)

        cost_dict = {'title':self.title_ent.get(), 'cost_type':self.choice.get(),
                     'amount':self.cost_ent.get(), 'desc': self.desc_ent.get('1.0', 'end-1c')}
        if self.choice.get() == "omr":
            cost_dict['omr_type'] = self.omr_selection.get()
            try:
                cost_dict['omr_times'] = [self.year_start_ent.get(), self.year_rate_ent.get(), 0]
            except:
                cost_dict['omr_times'] = [self.year_start_ent.get(), 0, 0]
        this_cost = Cost(**cost_dict)
        for index in plan_num:
            self.data_cont.plan_list[index].costs.indiv.append(this_cost)

        if valid:
            # ===== Updates the page for the next cost
            self.clear_page()
            self.update_prev_list()
            messagebox.showinfo("Success", "Cost has been successfully added!")
            return True

    def update_prev_list(self):
        """Updates 'Previously Inputted Costs' Section"""
        del self.choices[:]

        for plan in self.data_cont.plan_list:
            i = str(plan.id_assign)
            for cost in plan.costs.indiv:
                choice_check = cost.title
                if i == "0" and ((choice_check + " - <Base Plan>") not in self.choices):
                    self.choices.append(choice_check + " - <Base Plan>")
                elif i != "0" and ((choice_check + " - <Plan " + i + ">") not in self.choices):
                    self.choices.append(choice_check + " - <Plan " + i + ">")

        self.prev_costs.delete(0, tk.END)
        self.prev_costs.insert(tk.END, "")
        self.prev_costs.configure(values=self.choices)

    def check_page(self, printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        err_messages = ""

        valid = True

        # ===== Mandatory fields cannot be left blank or left alone
        if self.title_ent.get() == "" or self.title_ent.get() == "<enter a title for this cost>":
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        if "," in self.desc_ent.get("1.0", "end-1c"):
            err_messages += ("Description cannot have a comma \',\'."
                             "Please change the decsription.\n\n")
            valid = False
        check_against = self.desc_ent.get("1.0", "end-1c")
        if check_against == "" or check_against == "<enter a description for this cost>":
            self.desc_ent.delete('1.0', tk.END)
            self.desc_ent.insert(tk.END, "N/A")
        bool_check = [self.bools[i].get() for i in range(len(self.bools))]
        if not np.any(bool_check):
            err_messages += "No affected plans have been chosen! Please choose a plan.\n\n"
            valid = False
        if self.choice.get() != "direct" and self.choice.get() != "indirect" and self.choice.get() != "omr":
            err_messages += "A 'Cost Type' has not been selected!\n\n"
            valid = False

        # ===== Cost cannot have a duplicate title
        plan_num = []  # === List that contains all selected plans

        for i in range(1, len(self.bools)):
            if self.bools[i].get():
                plan_num.append(i)

        for choice in self.choices:
            if (choice)[:len(self.title_ent.get())] == self.title_ent.get():
                if self.bools[0].get() and " - <Base Plan>" in choice:
                    err_messages += ("\"" + self.title_ent.get() +
                                     "\" is already used as a cost title for the Base Plan. "
                                     "Please input a different title.\n\n")
                    valid = False

                for index in plan_num:
                    if " - <Plan " + str(index) + ">" in choice:
                        err_messages += ("\"" + self.title_ent.get()
                                         + "\" is already used as a cost title for Plan "
                                         + str(index) + ". Please input a different title."
                                         + "\n\n")
                        valid = False

        # ===== Cost Title must not have a hyphen '-'
        if "-" in self.title_ent.get():
            err_messages += ("Title cannot have a hyphen \'-\'. Please change the title.\n\n")
            valid = False

        # ===== Cost must be a positive number
        try:
            float(self.cost_ent.get())
        except ValueError:
            err_messages += "Dollar value of the cost must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.cost_ent.get():
            err_messages += "Cost must be a positive number. Please enter a positive amount.\n\n"
            valid = False

        # ===== Omr Fields must be filled if OMR is selected
        if self.choice.get() == "omr":
            try:
                float(self.year_start_ent.get())
            except ValueError:
                err_messages += "Starting year must be number. Please enter an amount.\n\n"
                valid = False
            if "-" in self.year_start_ent.get():
                err_messages += "Starting year must be a positive number. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False

            if self.omr_selection.get() == "Recurring":
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

    def copy_cost(self):
        """Duplicates information of chosen cost and pastes it on screen"""
        if self.prev_costs.get() == "":
            messagebox.showerror("Error",
                                 "No previous cost selected! Please select a cost to continue.")
            return

        # === First index is cost title, second index is plan number of corresponding cost
        chosen_cost = (self.prev_costs.get()).split(" - ")
        # === Cleans this up so that it could be used to find the first index of the chosen cost
        chosen_cost[1] = chosen_cost[1].replace("Plan", '')
        chosen_cost[1] = chosen_cost[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_cost[1] = chosen_cost[1].replace("Base", '0')
        chosen_cost[1] = int(chosen_cost[1])

        old_plan = self.data_cont.plan_list[chosen_cost[1]]
        for cost in old_plan.costs.indiv:
            if cost.title == chosen_cost[0]:
                old_cost = cost

        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, old_cost.title)
        self.cost_ent.delete(0, tk.END)
        self.cost_ent.insert(tk.END, old_cost.amount)
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, old_cost.desc)
        self.choice.set(old_cost.cost_type)
        if old_cost.cost_type == "omr":
            self.omr_selection.set(old_cost.omr_type)
            self.year_start_ent.delete(0, tk.END)
            self.year_start_ent.insert(tk.END, old_cost.omr_times[0])
            if old_cost.omr_type == "recurring":
                self.year_rate_ent.delete(0, tk.END)
                self.year_rate_ent.insert(tk.END, old_cost.omr_times[1])


    def edit_cost(self):
        """Edits the chosen cost and disables all 'previous costs'
           functionality untill an appropriate action is taken"""
        if self.prev_costs.get() == "":
            messagebox.showerror("Error",
                                 "No previous cost selected! Please select a cost to continue.")
            return

        chosen_cost = (self.prev_costs.get()).split(" - ")
        chosen_cost[1] = chosen_cost[1].replace("Plan", '')
        chosen_cost[1] = chosen_cost[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_cost[1] = chosen_cost[1].replace("Base", '0')
        chosen_cost[1] = int(chosen_cost[1])

        # ===== Sets the check boxes to their appropriate selection/deselection
        self.clear_page()

        self.copy_cost()

        if chosen_cost[1] == 0:
            self.base.select()
        elif chosen_cost[1] == 1:
            self.plan1.select()
        elif chosen_cost[1] == 2:
            self.plan2.select()
        elif chosen_cost[1] == 3:
            self.plan3.select()
        elif chosen_cost[1] == 4:
            self.plan4.select()
        elif chosen_cost[1] == 5:
            self.plan5.select()
        elif chosen_cost[1] == 6:
            self.plan6.select()

        # ===== Alters the button layout to avoid conflicting actions
        # ===== Enables user to take additional actions
        self.prev_costs.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        self.add_button.configure(text="Edit Cost", command=self.change_cost)

        self.cancel_button = ttk.Button(self, text="Cancel Edit", command=self.cancel_edit)
        self.cancel_button.grid(row=6, column=1, sticky="sw",
                                padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def delete_cost(self, is_updating):
        """Deletes a cost entry"""
        if self.prev_costs.get() == "":
            messagebox.showerror("Error",
                                 "No previous cost selected! Please select a cost to continue.")
            return

        # === First index is cost title, second index is plan number of corresponding cost
        chosen_cost = (self.prev_costs.get()).split(" - ")
        # === Cleans this up so that it could be used to find the first index of the chosen cost
        chosen_cost[1] = chosen_cost[1].replace("Plan", '')
        chosen_cost[1] = chosen_cost[1].replace("<", '').replace(">", '').replace(" ", '')
        chosen_cost[1] = chosen_cost[1].replace("Base", '0')
        chosen_cost[1] = int(chosen_cost[1])

        def confirm():
            """Confirmation page to make sure the user really wants to delete the given cost"""
            popup = tk.Tk()

            def confirm_delete():
                """ Confirms that deleting should happen and actually deletes the data."""
                # ===== Removes the cost from the list
                chosen_plan = self.data_cont.plan_list[chosen_cost[1]]
                for cost in chosen_plan.costs.indiv:
                    if cost.title == chosen_cost[0]:
                        chosen_plan.costs.indiv.remove(cost)

                self.update_prev_list()
                popup.destroy()

            def cancel_delete():
                """ Cancels the delete process."""
                popup.destroy()

            chosen_plan = self.data_cont.plan_list[chosen_cost[1]]
            for cost in chosen_plan.costs.indiv:
                if cost.title == chosen_cost[0]:
                    cost_amount = cost.amount
                    cost_desc = cost.desc

            popup.wm_title("Confirmation")
            del_text = "Delete \'" + chosen_cost[0] + "\'?\n\nAmount: " + str(cost_amount) + "\n\nDescription: " + str(cost_desc)
            label = ttk.Label(popup, text=del_text, font=NORM_FONT)
            label.grid(padx=BASE_PADDING, pady=BASE_PADDING)

            confirm_button = ttk.Button(popup, text="OK", command=confirm_delete)
            confirm_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            cancel_button = ttk.Button(popup, text="Cancel", command=cancel_delete)
            cancel_button.grid(sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)
            popup.mainloop()
            return

        if not is_updating:
            confirm()       # === Makes sure the user meant to delete the cost
        else:
            chosen_plan = self.data_cont.plan_list[chosen_cost[1]]
            for cost in chosen_plan.costs.indiv:
                if cost.title == chosen_cost[0]:
                    chosen_plan.costs.indiv.remove(cost)

            self.update_prev_list()

    def change_cost(self):
        """Deletes old instance of cost and adds new instance"""
        self.prev_costs.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Cost", command=self.add_cost)

        self.cancel_button.grid_remove()

        self.delete_cost(True)
        self.update_prev_list()
        self.add_cost()

        return

    def cancel_edit(self):
        """Cancels 'edit mode' and returns to normal functionality"""
        self.prev_costs.configure(state="active")
        self.edit_button.configure(state="active")
        self.copy_button.configure(state="active")
        self.delete_button.configure(state="active")

        self.add_button.configure(text="Add Cost", command=self.add_cost)

        self.cancel_button.grid_remove()

        self.clear_page()

    def clear_page(self):
        """Clears the page and resets all fields"""
        self.title_ent.delete(0, tk.END)
        self.title_ent.insert(tk.END, "<enter a title for this cost>")
        self.cost_ent.delete(0, tk.END)
        self.cost_ent.insert(tk.END, "<enter an amount for this cost>")
        self.desc_ent.delete('1.0', tk.END)
        self.desc_ent.insert(tk.END, "<enter a description for this cost>")
        self.base.deselect()
        self.plan1.deselect()
        self.plan2.deselect()
        self.plan3.deselect()
        self.plan4.deselect()
        self.plan5.deselect()
        self.plan6.deselect()
        # === Temporarily sets these so that further fields can be returned to default state
        self.choice.set("omr")
        self.omr_selection.set("Recurring")
        self.year_start_ent.delete(0, tk.END)
        self.year_start_ent.insert(tk.END, "<enter # of years after build year>")
        self.year_rate_ent.delete(0, tk.END)
        self.year_rate_ent.insert(tk.END, "<enter rate of occurence in years>")

        self.choice.set("1")
        self.omr_selection.set("1")


    def on_trace_change(self, _name, _index, _mode):
        """Updates checkbox fields if names are changed in 'InfoPage'"""

        self.plan1.configure(text=self.controller.frames[InfoPage].name_ents[0].get()+" (Plan 1)")
        # ===== Hides the widget until .grid() is called again
        self.plan2.grid_remove()
        self.plan3.grid_remove()
        self.plan4.grid_remove()
        self.plan5.grid_remove()
        self.plan6.grid_remove()

        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 1:
            self.plan2.configure(text=self.controller.frames[InfoPage].name_ents[1].get()
                                 +" (Plan 2)")
            self.plan2.grid()
        if int(self.controller.frames[InfoPage].num_plans_ent.get()) > 2:
            print(self.controller.frames[InfoPage].name_ents[2].get())
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

        if self.choice.get() == "omr":
            self.group5.grid()
        else:
            self.group5.grid_remove()

        self.year_start_lbl.configure(state="disabled")
        self.year_start_ent.configure(state="disabled")
        self.year_start_lbl2.configure(state="disabled")
        self.year_rate_lbl.grid_remove()
        self.year_rate_ent.grid_remove()
        self.year_rate_lbl2.grid_remove()

        if self.omr_selection.get() == "one-time":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid_remove()
            self.year_rate_ent.grid_remove()
            self.year_rate_lbl2.grid_remove()
        elif self.omr_selection.get() == "recurring":
            self.year_start_lbl.configure(state="normal")
            self.year_start_ent.configure(state="normal")
            self.year_start_lbl2.configure(state="normal")
            self.year_rate_lbl.grid()
            self.year_rate_ent.grid()
            self.year_rate_lbl2.grid()
