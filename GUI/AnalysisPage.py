"""
   File:          AnalysisPage.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the final analysis results.
"""

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels
from tkinter import messagebox

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT, BOLD_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

from GUI.AnalysisUncertainties import run_u_main_page

def run_main_page(data):
    """Only creates a new window called "MainPage" once all calculations are finished"""
    class MainPage(tk.Tk):
        """ The Analysis page of the application."""
        def __init__(self, data, *args, **kwargs):
            # args = arguments, kwargs = key word args
            tk.Tk.__init__(self, *args, **kwargs)
            self.container = tk.Frame(self)
            self.data_cont = data

            tk.Tk.wm_title(self, "NIST Economic Decision Guide")

            # ===== Adds a canvas so that the window will have a scrollbar
            vscrollbar = AutoScrollbar(self.container)
            vscrollbar.grid(row=0, column=1, sticky="ns")
            hscrollbar = AutoScrollbar(self.container, orient=tk.HORIZONTAL)
            hscrollbar.grid(row=1, column=0, sticky="ew")

            canvas = tk.Canvas(self.container,
                               yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
            canvas.grid(row=0, column=0, sticky="nsew")

            vscrollbar.config(command=canvas.yview)
            hscrollbar.config(command=canvas.xview)

            # make the canvas expandable
            self.container.grid()
            self.container.grid_rowconfigure(0, weight=1, minsize=90)
            self.container.grid_columnconfigure(0, weight=1, minsize=1500)

            # create canvas contents
            frame = tk.Frame(canvas)
            frame.rowconfigure(1, weight=1)
            frame.columnconfigure(1, weight=1)

            self.create_widgets(frame)

            canvas.create_window(0, 0, anchor="nw", window=frame)
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))


            # ===== Adds a title to the page
            title = ttk.Label(frame, text="Outputs of Economic Evaluation", font=LARGE_FONT)
            title.grid(row=0, padx=FRAME_PADDING, pady=FRAME_PADDING)

            title2 = ttk.Label(frame, text="[" + self.data_cont.title + "]",
                               font=LARGE_FONT)
            title2.grid(row=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        def create_widgets(self, frame):
            """Widgets include: menu bar, **temporary** home button"""

            """
            menubar = tk.Menu(container, tearoff=0)
            filemenu = tk.Menu(menubar)

            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=sys.exit)
            menubar.add_cascade(label="File", menu=filemenu)

            tk.Tk.config(self, menu=menubar)"""

            # ===== Labels the plans
            spacer = " " * 27
            my_tab = " " * 5
            pad_opts = {'padx': FIELDX_PADDING, 'pady':FIELDY_PADDING}

            group0 = ttk.LabelFrame(frame)
            group0.grid(row=2, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

            # === Places a space for neatness
            ttk.Label(group0,
                      text=spacer+spacer+my_tab+my_tab+my_tab).grid(row=0, column=0, **pad_opts)
            ttk.Label(group0, text=spacer+"Base Case",
                      font=NORM_FONT).grid(row=0, column=1, sticky="e", **pad_opts)
            for i in range(self.data_cont.num_plans-1):
                ttk.Label(group0, text=spacer+"Alternative " + str(i+1),
                          font=NORM_FONT).grid(row=0, column=(i+2), sticky="e", **pad_opts)
            for i in range(len(self.data_cont.plan_list)):
                ttk.Label(group0, text=self.data_cont.plan_list[i].name,
                          font=SMALL_FONT).grid(row=1, column=(i+1), sticky="e", **pad_opts)

            # ===== Total Benefits
            group1 = ttk.LabelFrame(frame, text="Benefits")
            group1.grid(row=3, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

            disaster_ben_lbl = ttk.Label(group1, text="Disaster Economic Benefits", font=NORM_FONT)
            disaster_ben_lbl.grid(row=0, column=0, sticky="w", **pad_opts)
            res_rec_lbl = ttk.Label(group1, text=my_tab + "Response and Recovery Costs",
                                    font=SMALL_FONT)
            res_rec_lbl.grid(row=1, column=0, sticky="w", **pad_opts)
            dir_loss_lbl = ttk.Label(group1, text=my_tab + "Direct Losses", font=SMALL_FONT)
            dir_loss_lbl.grid(row=2, column=0, sticky="w", **pad_opts)
            id_loss_lbl = ttk.Label(group1, text=my_tab + "Indirect Losses", font=SMALL_FONT)
            id_loss_lbl.grid(row=3, column=0, sticky="w", **pad_opts)

            disaster_non_m_ben_lbl = ttk.Label(group1, text="Disaster Non-Market Benefits",
                                               font=NORM_FONT)
            disaster_non_m_ben_lbl.grid(row=4, column=0, sticky="w", **pad_opts)
            fat_lbl = ttk.Label(group1, text=my_tab + "Value of Statistical Lives Saved",
                                font=SMALL_FONT)
            fat_lbl.grid(row=5, column=0, sticky="w", **pad_opts)
            fat_lbl2 = ttk.Label(group1, text=my_tab + "Number of Statistical Lives Saved",
                                 font=SMALL_FONT)
            fat_lbl2.grid(row=6, column=0, sticky="w", **pad_opts)

            # ===== Sums up the numbers
            self.data_cont.summer()

            non_d_ben_lbl = ttk.Label(group1, text="Non-Disaster Related Benefits",
                                      font=NORM_FONT)
            non_d_ben_lbl.grid(row=7, column=0, sticky="w", **pad_opts)

            # === Lists out all of the NonDBens
            #for i in range(len(data_cont.nonDBenNames)):
            #    ttk.Label(group1, text=my_tab + data_cont.nonDBenNames[i][0],
            #              font=SMALL_FONT).grid(column=0, sticky="w", **pad_opts)

            # ===== Total Costs
            group2 = ttk.LabelFrame(frame, text="Costs")
            group2.grid(row=4, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

            init_lbl = ttk.Label(group2, text="Initial", font=NORM_FONT)
            init_lbl.grid(row=0, column=0, sticky="w", **pad_opts)
            dir_lbl = ttk.Label(group2, text=my_tab + "Direct" + " "*39, font=SMALL_FONT)
            dir_lbl.grid(row=1, column=0, sticky="w", **pad_opts)
            id_lbl = ttk.Label(group2, text=my_tab + "Indirect", font=SMALL_FONT)
            id_lbl.grid(row=2, column=0, sticky="w", **pad_opts)
            omr_lbl = ttk.Label(group2, text=my_tab + "OMR", font=SMALL_FONT)
            omr_lbl.grid(row=3, column=0, sticky="w", **pad_opts)

            rec_lbl = ttk.Label(group2, text="Recurring Costs", font=NORM_FONT)
            rec_lbl.grid(row=4, column=0, sticky="w", **pad_opts)
            rec_omr_lbl = ttk.Label(group2, text=my_tab + "OMR", font=SMALL_FONT)
            rec_omr_lbl.grid(row=5, column=0, sticky="w", **pad_opts)

            # ===== Totals
            group3 = ttk.LabelFrame(frame, text="Totals")
            group3.grid(row=5, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

            tot_lbl = ttk.Label(group3, text="Total: Present Expected Value", font=NORM_FONT)
            tot_lbl.grid(row=0, column=0, sticky="w", **pad_opts)
            ben_lbl = ttk.Label(group3, text=my_tab + "Benefits" + " "*24, font=SMALL_FONT)
            ben_lbl.grid(row=1, column=0, sticky="w", **pad_opts)
            cost_lbl = ttk.Label(group3, text=my_tab + "Costs", font=SMALL_FONT)
            cost_lbl.grid(row=2, column=0, sticky="w", **pad_opts)
            net_lbl = ttk.Label(group3, text=my_tab + "Net", font=SMALL_FONT)
            net_lbl.grid(row=3, column=0, sticky="w", **pad_opts)

            ttk.Label(group3, text=" ").grid(row=4, **pad_opts)
            for i in range(2 + self.data_cont.num_plans):
                ttk.Separator(group3, orient=tk.HORIZONTAL).grid(row=4, column=i, sticky="ew")
            sir_lbl = ttk.Label(group3, text=my_tab + "Savings-to-Investment Ratio",
                                font=SMALL_FONT)
            sir_lbl.grid(row=5, column=0, sticky="w", **pad_opts)
            irr_lbl = ttk.Label(group3, text=my_tab + "Internal Rate of Return", font=SMALL_FONT)
            irr_lbl.grid(row=6, column=0, sticky="w", **pad_opts)
            roi_lbl = ttk.Label(group3, text=my_tab + "Return on Investment", font=SMALL_FONT)
            roi_lbl.grid(row=7, column=0, sticky="w", **pad_opts)
            non_d_roi = ttk.Label(group3, text=my_tab + "Non-Disaster ROI", font=SMALL_FONT)
            non_d_roi.grid(row=8, column=0, sticky="w", **pad_opts)
            # === Places spaces to correct an unknown error with the window size
            ttk.Label(group3, text=" ").grid(row=10)
            ttk.Label(group3, text=" ").grid(row=11)
            ttk.Label(group3, text=" ").grid(row=12)
            ttk.Label(group3, text=" ").grid(row=13)
            ttk.Label(group3, text=" ").grid(row=14)


            for i in range(self.data_cont.num_plans):
                plan = self.data_cont.plan_list[i]
                num_spaces = int(48 - (len('${:,.0f}'.format(plan.bens.r_sum)) * .8))
                text_1 = plan.bens.r_sum
                ttk.Label(group1, text=(" "*num_spaces) + '${:,.0f}'.format(text_1),
                          font=SMALL_FONT).grid(row=1, column=(i+1), sticky="e", **pad_opts)
                text_2 = plan.bens.d_sum
                ttk.Label(group1, text='${:,.0f}'.format(text_2),
                          font=SMALL_FONT).grid(row=2, column=(i+1), sticky="e", **pad_opts)
                text_3 = plan.bens.i_sum
                ttk.Label(group1, text='${:,.0f}'.format(text_3),
                          font=SMALL_FONT).grid(row=3, column=(i + 1), sticky="e", **pad_opts)
                text_4 = plan.fat.stat_value_averted
                ttk.Label(group1, text='${:,.0f}'.format(text_4),
                          font=SMALL_FONT).grid(row=5, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group1, text='{:,.2f}'.format(plan.fat.stat_averted),
                          font=SMALL_FONT).grid(row=6, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group1, text='${:,.0f}'.format(plan.nond_bens.total),
                          font=SMALL_FONT).grid(row=7, column=i+1, sticky="e", **pad_opts)

                num_spaces = int(48-(len('${:,.0f}'.format(plan.costs.d_sum))*.8))
                my_tab = " " * num_spaces
                ttk.Label(group2,
                          text=my_tab+'${:,.0f}'.format(plan.costs.d_sum),
                          font=SMALL_FONT).grid(row=1, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group2, text='${:,.0f}'.format(plan.costs.i_sum),
                          font=SMALL_FONT).grid(row=2, column=(i+1), sticky="e", **pad_opts)
                if plan.costs.omr_1_sum != "":
                    ttk.Label(group2, text='${:,.0f}'.format(plan.costs.omr_1_sum),
                              font=SMALL_FONT).grid(row=3, column=(i+1), sticky="e", **pad_opts)
                if plan.costs.omr_r_sum != "":
                    ttk.Label(group2, text='${:,.0f}'.format(plan.costs.omr_r_sum),
                              font=SMALL_FONT).grid(row=5, column=(i+1), sticky="e", **pad_opts)

            for i in range(self.data_cont.num_plans):
                plan = self.data_cont.plan_list[i]
                num_spaces = int(42 - (len('${:,.0f}'.format(plan.total_bens)) * .8))

                ttk.Label(group3,
                          text=" "*num_spaces + '${:,.0f}'.format(plan.total_bens),
                          font=BOLD_FONT).grid(row=1, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group3, text='${:,.0f}'.format(plan.costs.total),
                          font=BOLD_FONT).grid(row=2, column=(i + 1), sticky="e", **pad_opts)
                if plan.net >= 0:
                    ttk.Label(group3, text='${:,.0f}'.format(plan.net),
                              font=BOLD_FONT).grid(row=3, column=(i + 1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group3, text='(' + '${:,.0f}'.format(plan.net) + ')',
                              font=BOLD_FONT).grid(row=3, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group3, text='{:,.2f}'.format(self.data_cont.plan_list[i].sir()),
                          font=SMALL_FONT).grid(row=5, column=(i + 1), sticky="e", **pad_opts)
                if type(self.data_cont.plan_list[i].irr()) == type("string"):
                    ttk.Label(group3, text=self.data_cont.plan_list[i].irr(),
                              font=SMALL_FONT).grid(row=6, column=(i+1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group3, text='{:,.1f}'.format(self.data_cont.plan_list[i].irr()) + '%',
                              font=SMALL_FONT).grid(row=6, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group3, text='{:,.1f}'.format(self.data_cont.plan_list[i].roi()) + '%',
                          font=SMALL_FONT).grid(row=7, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group3, text='{:,.1f}'.format(self.data_cont.plan_list[i].non_d_roi()) + '%',
                          font=SMALL_FONT).grid(row=8, column=(i + 1), sticky="e", **pad_opts)

            exp_button = ttk.Button(self, text="Export Summary", command=self.export)
            exp_button.grid(row=6)
            info_button = ttk.Button(self, text="More Information", command=self.info)
            info_button.grid(row=6, sticky="w")
            uncert_button = ttk.Button(self, text="View Uncertainty", command=lambda:run_u_main_page(self.data_cont))
            uncert_button.grid(row=6, sticky="e")

        def export(self):
            """Prompts the user to select how to export the Analysis Summary"""
            popup = tk.Tk()

            def leavemini():
                """Destroys popup """
                popup.destroy()

            def document():
                """Destroys popup and calls docx export."""
                leavemini()
                self.data_cont.to_docx()

            def commas():
                """Destroys popup and calls csv export."""
                leavemini()
                self.data_cont.to_csv()

            def both():
                """Destroys popup and calls docx and csv export."""
                leavemini()
                self.data_cont.to_docx()
                self.data_cont.to_csv()

            popup.wm_title("Export")
            label = ttk.Label(popup, text="Which format would you like to export?", font=NORM_FONT)
            label.grid(padx=BASE_PADDING, pady=BASE_PADDING)

            docx_button = ttk.Button(popup, text=".docx", command=document)
            docx_button.grid(row=2, sticky="w", padx=BASE_PADDING, pady=BASE_PADDING)
            csv_button = ttk.Button(popup, text=".csv", command=commas)
            csv_button.grid(row=2, padx=BASE_PADDING, pady=BASE_PADDING)
            both_button = ttk.Button(popup, text="Both formats", command=both)
            both_button.grid(row=2, sticky="e", padx=BASE_PADDING, pady=BASE_PADDING)

            popup.mainloop()

        def info(self):
            """Provides information to the user"""
            messagebox.showinfo("More Information",
                                "For information regrading any of the particular benefits or "
                                "costs, please refer back to the previous pages of the particular"
                                " benefit or cost. The corresponding pages contain specific "
                                "information to their related benefit or cost.\n\n"
                                "The following terms are defined:\n\n"
                                "    Savings-to-Investment Ratio:\n"
                                "            Used to determine whether the potential savings of a "
                                "project justifies the inital investment and following maintenance"
                                " costs. The higher the ratio, the greater the savings; this "
                                "number can also be negative.\n\n"
                                "    Internal Rate of Return:\n"
                                "            This is the discount rate that makes the Net Present "
                                "Value of all net cash flows of a project equal zero. It measures "
                                "the profitability of potential investments. Generally speaking, "
                                "the higher this number, the more desirable the project.\n\n"
                                "    Return on Investment:\n"
                                "            Measures the amount of return on an investment "
                                " relative to the investment's cost. The annual benefit is divided"
                                " by the total cost, resulting in a ratio. The higher this number,"
                                " the higher the annual return is on a project.\n\n"
                                "    Non-Disaster ROI:\n"
                                "            Return on Investment, assuming that no disaster occurs"
                                " within the planning horizon.\n\n\n"
                                "Links to NIST's Economic Decision Guide:\n"
                                "http://www.nist.gov/el/resilience/guide.cfm\n"
                                "http://nvlpubs.nist.gov/nistpubs/"
                                "SpecialPublications/NIST.SP.1197.pdf")


    root = MainPage(data)
    root.mainloop()

class AutoScrollbar(tk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed.
     Only works if you use the grid geometry manager!"""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
    def pack(self, **_kw):
        """ I don't know what this does. """
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **_kw):
        """ I don't know what this does. """
        raise tk.TclError("cannot use place with this widget")
