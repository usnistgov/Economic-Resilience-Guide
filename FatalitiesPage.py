"""
   File:          FatalitiesPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the GUI for the FatalitiesPage,
                  the page for the user to input Fatalities.
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

        life_lbl = ttk.Label(group0, text="Value of a Statistical Life $", font=SMALL_FONT)
        life_lbl.grid(row=1, column=0, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)
        self.life_ent = tk.Entry(group0, width=ENTRY_WIDTH, font=SMALL_FONT)
        self.life_ent.insert(tk.END, "7500000")
        self.life_ent.grid(row=1, column=1, sticky="e", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        def_button = ttk.Button(group0, text="Restore Default", command=self.restore)
        def_button.grid(row=2, column=0, sticky="w", padx=FIELDX_PADDING, pady=FIELDY_PADDING)

        # ===== Fatality Description Widgets
        group1 = ttk.LabelFrame(self, text="Fatality Description")
        group1.grid(row=4, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

        pad_opts = {'padx':FIELDX_PADDING, 'pady':FIELDY_PADDING}
        fat_lbl = ttk.Label(group1, text="Amount", font=NORM_FONT)
        fat_lbl.grid(row=0, column=1, sticky="we", **pad_opts)
        desc_lbl = ttk.Label(group1, text="Description", font=NORM_FONT)
        desc_lbl.grid(row=0, column=2, **pad_opts)

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
            text.grid(row=my_row, column=2, sticky = "ews", **pad_opts)

        for i in range(1, 7):
            self.fat_plan_lbls[i].grid_remove()
            self.fat_plan_ents[i].grid_remove()
            self.desc_plan_ents[i].grid_remove()

        #fat_b_lbl = ttk.Label(group1, text="Base:", font=NORM_FONT)
        #fat_b_lbl.grid(row=1, column=0, sticky="ne", **pad_opts)
        #self.fat_b_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_b_ent.insert(tk.END, "")
        #self.fat_b_ent.grid(row=1, column=1, sticky="nw", **pad_opts)
        #self.desc_b_ent = tk.Text(group1, width=40, height=3, font=SMALL_FONT)
        #self.desc_b_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_b_ent.grid(row=1, column=2, sticky="ews", **pad_opts)

        #self.fat_1_lbl = ttk.Label(group1, text="Plan 1:", font=NORM_FONT)
        #self.fat_1_lbl.grid(row=2, column=0, sticky="ne", **pad_opts)
        #self.fat_1_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_1_ent.insert(tk.END, "")
        #self.fat_1_ent.grid(row=2, column=1, sticky="nw", **pad_opts)
        #self.desc_1_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_1_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_1_ent.grid(row=2, column=2, sticky="ews", **pad_opts)

        #self.fat_1_lbl.grid_remove()
        #self.fat_1_ent.grid_remove()
        #self.desc_1_ent.grid_remove()

        #self.fat_2_lbl = ttk.Label(group1, text="Plan 2:", font=NORM_FONT)
        #self.fat_2_lbl.grid(row=3, column=0, sticky="ne", **pad_opts)
        #self.fat_2_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_2_ent.insert(tk.END, "")
        #self.fat_2_ent.grid(row=3, column=1, sticky="nw", **pad_opts)
        #self.desc_2_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_2_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_2_ent.grid(row=3, column=2, sticky="ews", **pad_opts)

        #self.fat_2_lbl.grid_remove()
        #self.fat_2_ent.grid_remove()
        #self.desc_2_ent.grid_remove()

        #self.fat_3_lbl = ttk.Label(group1, text="Plan 3:", font=NORM_FONT)
        #self.fat_3_lbl.grid(row=4, column=0, sticky="ne", **pad_opts)
        #self.fat_3_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_3_ent.insert(tk.END, "")
        #self.fat_3_ent.grid(row=4, column=1, sticky="nw", **pad_opts)
        #self.desc_3_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_3_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_3_ent.grid(row=4, column=2, sticky="ews", **pad_opts)

        #self.fat_3_lbl.grid_remove()
        #self.fat_3_ent.grid_remove()
        #self.desc_3_ent.grid_remove()

        #self.fat_4_lbl = ttk.Label(group1, text="Plan 4:", font=NORM_FONT)
        #self.fat_4_lbl.grid(row=5, column=0, sticky="ne", **pad_opts)
        #self.fat_4_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_4_ent.insert(tk.END, "")
        #self.fat_4_ent.grid(row=5, column=1, sticky="nw", **pad_opts)
        #self.desc_4_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_4_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_4_ent.grid(row=5, column=2, sticky="ews", **pad_opts)

        #self.fat_4_lbl.grid_remove()
        #self.fat_4_ent.grid_remove()
        #self.desc_4_ent.grid_remove()

        #self.fat_5_lbl = ttk.Label(group1, text="Plan 5:", font=NORM_FONT)
        #self.fat_5_lbl.grid(row=6, column=0, sticky="ne", **pad_opts)
        #self.fat_5_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_5_ent.insert(tk.END, "")
        #self.fat_5_ent.grid(row=6, column=1, sticky="nw", **pad_opts)
        #self.desc_5_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_5_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_5_ent.grid(row=6, column=2, sticky="ews", **pad_opts)

        #self.fat_5_lbl.grid_remove()
        #self.fat_5_ent.grid_remove()
        #self.desc_5_ent.grid_remove()

        #self.fat_6_lbl = ttk.Label(group1, text="Plan 6:", font=NORM_FONT)
        #self.fat_6_lbl.grid(row=7, column=0, sticky="ne", **pad_opts)
        #self.fat_6_ent = tk.Entry(group1, width=int(ENTRY_WIDTH / 5), font=SMALL_FONT)
        #self.fat_6_ent.insert(tk.END, "")
        #self.fat_6_ent.grid(row=7, column=1, sticky="nw", **pad_opts)
        #self.desc_6_ent = tk.Text(group1, width=30, height=3, font=SMALL_FONT)
        #self.desc_6_ent.insert(tk.END, "<enter a description for this fatality aversion>")
        #self.desc_6_ent.grid(row=7, column=2, sticky="ews", **pad_opts)

        #self.fat_6_lbl.grid_remove()
        #self.fat_6_ent.grid_remove()
        #self.desc_6_ent.grid_remove()


        # ===== Detects if a change occurs in the name fields on 'InfoPage'
        controller.frames[InfoPage].p1_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p2_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p3_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p4_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p5_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].p6_trace.trace("w", self.on_trace_change)
        controller.frames[InfoPage].choice_var.trace("w", self.on_trace_change)

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

    def restore(self):
        """Restores the number of the statistical life value to its default state"""
        self.life_ent.delete(0, tk.END)
        self.life_ent.insert(tk.END, "7500000")
        return

    def hover(self, _event):
        """Updates prevList when mouse is hovered over the widget"""
        self.on_trace_change('mode', 'index', 'name')

    def save(self):
        """Updates global variables with whats on the page
           in case user forgets to click 'Update Fatalities'"""
        self.add_fat()
        self.data_cont.save_info()

    def show_info(self):
        """ Pulls up information for the Fatalities page."""
        messagebox.showinfo("More Information",
                            "        'Fatalities Averted' refers to the average number "
                            "of deaths avoided per disturbance occurrence "
                            "as a result of implementing a corresponding plan. "
                            "This number can be a decimal, "
                            "representing injuries inflicted that cost a portion "
                            "of the expected cost of a complete "
                            "fatality.\n\n"
                            "Statistical Life:\n        "
                            "The calculated average value of a life. This value is subjected to "
                            "change, but exists merely to assist in cost/benefit analysis. It is "
                            "usually seen that lives saved should be taken "
                            "into consideration in any "
                            "project. For this reason, "
                            "a default value of $7.5 M has been assigned.")
    def do_nothing(self):
        """Used for the try/catch found in on_trace_change"""
        return

    def add_fat(self):
        """Appends list of fatality aversions, clears page's entry widgets,
           and updates 'Previously Inputted Fatality Aversions' section"""
        num_plans = int(self.controller.frames[InfoPage].num_plans_ent.get())
        valid = self.check_page()
        if not valid:
            return False

        self.data_cont.stat_life = self.life_ent.get()

        for i in range(0, num_plans + 1):
            self.data_cont.Fatalities[i][1] = self.fat_plan_ents[i].get()
            self.data_cont.Fatalities[i][2] = self.desc_plan_ents[i].get("1.0", "end-1c")

        #self.data_cont.Fatalities[0][1] = self.fat_b_ent.get()
        #self.data_cont.Fatalities[0][2] = self.desc_b_ent.get("1.0", "end-1c")

        #self.data_cont.Fatalities[1][1] = self.fat_1_ent.get()
        #self.data_cont.Fatalities[1][2] = self.desc_1_ent.get("1.0", "end-1c")

        #if num_plans > 1:
        #    self.data_cont.Fatalities[2][1] = self.fat_2_ent.get()
        #    self.data_cont.Fatalities[2][2] = self.desc_2_ent.get("1.0", "end-1c")
        #if num_plans > 2:
        #    self.data_cont.Fatalities[3][1] = self.fat_3_ent.get()
        #    self.data_cont.Fatalities[3][2] = self.desc_3_ent.get("1.0", "end-1c")
        #if num_plans > 3:
        #    self.data_cont.Fatalities[4][1] = self.fat_4_ent.get()
        #    self.data_cont.Fatalities[4][2] = self.desc_4_ent.get("1.0", "end-1c")
        #if num_plans > 4:
        #    self.data_cont.Fatalities[5][1] = self.fat_5_ent.get()
        #    self.data_cont.Fatalities[5][2] = self.desc_5_ent.get("1.0", "end-1c")
        #if num_plans > 5:
        #    self.data_cont.Fatalities[6][1] = self.fat_6_ent.get()
        #    self.data_cont.Fatalities[6][2] = self.desc_6_ent.get("1.0", "end-1c")

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

        num_plans = int(self.controller.frames[InfoPage].num_plans_ent.get())

        # === Fills non-mandatory description fields with filler if no description has been input
        blank_desc = "<enter a description for this fatality aversion>"
        for entry in self.desc_plan_ents:
            if "," in entry.get("1.0", "end-1c"):
                err_messages += ("Description cannot have a comma \',\'. "
                                 "Please change the description.\n\n")
                valid = False

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
            self.data_cont.stat_life = float(self.life_ent.get())
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

        for i in range(1,7):
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
                self.fat_plan_ents[i].insert(tk.END, self.data_cont.Fatalities[i][1])
                self.desc_plan_ents[i].delete('1.0', tk.END)
                self.desc_plan_ents[i].insert(tk.END, self.data_cont.Fatalities[i][2])
            except IndexError:
                self.do_nothing()
