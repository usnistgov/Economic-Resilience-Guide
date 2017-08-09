"""
   File:          FatalitiesPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the FatalitiesPage,
                  the page for the user to input Fatalities.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk     #for pretty buttons/labels

from GUI.InfoPage import InfoPage

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING
from GUI.Constants import ENTRY_WIDTH

#
#
##################################### Fatalities Averted Class #####################################
#
#
class FatalitiesPage(tk.Frame):
    """
    GUI for the input of all Fatalities.
    """
    def __init__(self, parent, controller, data_cont_list):
        [self.data_cont] = data_cont_list
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Input number of fatalities averted in the "
                                     "event that a disaster occurs. \n"
                                     "Only one input can be made per plan. "
                                     "When finished, click 'Next>>'", font=SMALL_FONT)
        label.grid(padx=10, pady=10, sticky="new")

        fat_lbl = tk.Label(self, text="Fatalities Averted", font=LARGE_FONT)
        fat_lbl.grid(row=2, sticky="w")
        self.create_widgets(controller)

    def create_widgets(self, controller):
        """
            Creates the widgets for the GUI.
        """
        # ===== Statistical Life value
        group0 = ttk.LabelFrame(self)
        group0.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        ttk.Label(group0, text="Value of a Statistical Life $",
                  font=SMALL_FONT).grid(row=1, column=0, sticky="e",
                                        padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.life_ent = tk.Entry(group0, width=ENTRY_WIDTH, font=SMALL_FONT)
        # TODO: Why no commas?!?
        text = '{:,.2f}'.format(float(controller.data_cont.stat_life))
        #print(text) # Here, text has commas
        self.life_ent.insert(tk.END, text) # But here it doesn't. Arg.
        #print(text) # Here, text has commas
        self.life_ent.grid(row=1, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        ttk.Button(group0, text="Restore Default",
                   command=self.restore).grid(row=2, column=0, sticky="w",
                                              padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Fatality Description Widgets
        group1 = ttk.LabelFrame(self, text="Fatality Description")
        group1.grid(row=4, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        pad_opts = {'padx':FIELDX_PADDING, 'pady':FIELDY_PADDING}
        ttk.Label(group1, text="Amount",
                  font=NORM_FONT).grid(row=0, column=1, sticky="we", **pad_opts)
        tk.Label(group1, text="Description", font=NORM_FONT).grid(row=0, column=2, **pad_opts)

        self.fat_plan_lbls = [ttk.Label(group1, text="Base:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 1:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 2:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 3:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 4:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 5:", font=NORM_FONT),
                              ttk.Label(group1, text="Plan 6:", font=NORM_FONT)]
        for label in self.fat_plan_lbls:
            my_row = self.fat_plan_lbls.index(label) + 1
            label.grid(row=my_row, column=0, sticky="ne", **pad_opts)

        self.fat_plan_ents = [tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT),
                              tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)]
        for entry in self.fat_plan_ents:
            entry.insert(tk.END, "")
            my_row = self.fat_plan_ents.index(entry) + 1
            entry.grid(row=my_row, column=1, sticky="new", **pad_opts)

        self.desc_plan_ents = [tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT),
                               tk.Text(group1, width=40, height=3, font=SMALL_FONT)]
        for text in self.desc_plan_ents:
            text.insert(tk.END, "<enter a description for this fatality aversion>")
            my_row = self.desc_plan_ents.index(text) + 1
            text.grid(row=my_row, column=2, sticky="ews", **pad_opts)

        for i in range(1, 7):
            self.fat_plan_lbls[i].grid_remove()
            self.fat_plan_ents[i].grid_remove()
            self.desc_plan_ents[i].grid_remove()

        # ===== Detects if a change occurs in the name fields on 'InfoPage'
        controller.frames[InfoPage].traces[0].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[1].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[2].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[3].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[4].trace("w", self.on_trace_change)
        controller.frames[InfoPage].traces[5].trace("w", self.on_trace_change)
        #controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

        def save_and_next():
            """ Tries to save the input and sends the user to the next screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'NonDBensPage'
            moveon = self.add_fat()
            if moveon:
                controller.show_frame(go_to_place)

        def save_and_back():
            """ Tries to save the input and sends the user to the previous screen.
            If save unsuccessful asks user for verification to move on."""
            go_to_place = 'BenefitsUncertaintiesPage'
            moveon = self.add_fat()
            if moveon:
                controller.show_frame(go_to_place)

        def menu():
            """ Tries to save the input and sends the user to the Directory Page.
            If save unsuccessful, asks user for verification to move on."""
            go_to_place = 'DirectoryPage'
            moveon = self.add_fat()
            if moveon:
                controller.show_frame(go_to_place)


        # ===== Manueverability/Information buttons
        save_button = ttk.Button(self, text="Save Analysis", command=self.save)
        save_button.grid(row=1, column=1, sticky="se", padx=BASE_PADDING, pady=BASE_PADDING)
        self.add_button = ttk.Button(self, text="Update Data", command=self.add_fat)
        self.add_button.grid(row=5, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        did_info = ttk.Button(self, text="More Information", command=self.show_info)
        did_info.grid(row=2, column=1, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        back_button = ttk.Button(self, text="<<Back", command=save_and_back)
        back_button.grid(row=6, column=0, sticky="sw", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        finished_button = ttk.Button(self, text="Next>>", command=save_and_next)
        finished_button.grid(row=6, column=0, sticky="se", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        ttk.Button(self, text="Menu", command=menu).grid(row=7, column=0, sticky="se",
                                                         padx=FIELDX_PADDING, pady=FIELDY_PADDING)


    def restore(self):
        """Restores the number of the statistical life value to its default state"""
        self.life_ent.delete(0, tk.END)
        self.life_ent.insert(tk.END, '{:,.0f}'.format(7500000))
        return

    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.on_trace_change('mode', 'index', 'name')

    def save(self):
        """Updates global variables with whats on the page
           in case user forgets to click 'Update Fatalities'"""
        self.add_fat()
        self.data_cont.file_save()

    def show_info(self):
        """ Pulls up information for the Fatalities page."""
        messagebox.showinfo("More Information",
                            "‘Fatalities Averted’ refers to the average expected number of deaths "
                            "avoided per disturbance occurrence as a result of implementing a "
                            "corresponding plan. This value can be defined as decimal, "
                            "representing injuries inflicted that cost a portion of the expected "
                            "cost of a (complete) fatality.\n\n"
                            "Statistical Life: The calculated average expected value of a life. "
                            "This value is subject to change, but exists merely to assist in the "
                            "cost/benefit analysis. It is noted that lives saved should be taken "
                            "into consideration in any BCA project, if possible. A default value "
                            "of $7.5 M has been assigned for the statistical value of life in "
                            "this Tool; the user may adjust this value as appropriate.\n")

    def add_fat(self):
        """Appends list of fatality aversions, clears page's entry widgets,
           and updates 'Saved Fatality Aversions' section"""
        num_plans = int(self.controller.frames[InfoPage].num_plans_ent.get())
        valid = self.check_page()
        if not valid:
            return False

        self.data_cont.stat_life = self.life_ent.get().replace(',', '')

        for i in range(0, num_plans + 1):
            self.data_cont.plan_list[i].fat.update(self.fat_plan_ents[i].get(),
                                                   [self.desc_plan_ents[i].get("1.0", "end-1c")],
                                                   self.data_cont.stat_life)

        if valid:
            messagebox.showinfo("Success",
                                "Fatality Aversion Statistics has been successfully updated!")
            return True

    def check_page(self, _printout=True):
        """Ensures that all required fields are properly filled out before continuing.
           Returns a bool"""
        # Keeping printout for consistency with other page classes
        err_messages = ""

        valid = True

        # ===== Check for empty entries
        for entry in self.fat_plan_ents:
            if entry.get() == "":
                entry.insert(tk.END, "0")

        # ===== Fatalities Averted must be a positive number
        for entry in self.fat_plan_ents:
            try:
                float(entry.get())
            except ValueError:
                err_messages += "Fatalaties Averted must be a number (can by a decimal). "
                err_messages += "Please enter an amount.\n\n"
                valid = False
            if "-" in entry.get():
                err_messages += "Fatalities Averted must be a positive number. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False

        try:
            amount = self.life_ent.get().replace(',', '')
            self.data_cont.stat_life = float(amount)
        except ValueError:
            err_messages += "Statistical Life Value must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in self.life_ent.get():
            err_messages += "Statistical Life Value must be a positive number. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False


        if not valid:
            messagebox.showerror("ERROR", err_messages)
        return valid

    def on_trace_change(self, _name, _index, _mode):
        """Updates description fields if numbers of plans are changed in 'InfoPage'"""

        for i in range(1, 7):
            self.fat_plan_ents[i].grid_remove()
            self.fat_plan_lbls[i].grid_remove()
            self.desc_plan_ents[i].grid_remove()

        # === Try is used here in case of a new analaysis being started
        num_plans = int(self.controller.frames[InfoPage].num_plans_ent.get())
        for i in range(0, num_plans+1):
            self.fat_plan_lbls[i].grid()
            self.fat_plan_ents[i].grid()
            self.desc_plan_ents[i].grid()
            try:
                self.fat_plan_ents[i].delete(0, tk.END)
                self.fat_plan_ents[i].insert(tk.END, self.data_cont.plan_list[i].fat.averted)
                self.desc_plan_ents[i].delete('1.0', tk.END)
                self.desc_plan_ents[i].insert(tk.END, self.data_cont.plan_list[i].fat.desc)
            except IndexError:
                pass
