"""
   File:          AnalysisUncertainties.py
   Author:        Shannon Craig
   Description:   Interacts with EconGuide.py, builds the final analysis results with Montecarlo.
"""

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels
from tkinter import messagebox

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT, BOLD_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

from monte_benefits import monte_carlo as m_bens

def run_u_main_page(data):
    """Only creates a new window called "MainPage" once all calculations are finished"""
    class UMainPage(tk.Tk):
        """ The Analysis page with uncertainty of the application."""
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
            self.container.grid_rowconfigure(0, weight=1, minsize=900)
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
            title = ttk.Label(frame, text="Uncertainty Output of Economic Evaluation",
                              font=LARGE_FONT)
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
            my_tab = " " * 5
            pad_opts = {'padx': FIELDX_PADDING, 'pady':FIELDY_PADDING}

            group0 = ttk.Frame(frame)
            group0.grid(row=2, sticky="ew", padx=FRAME_PADDING, pady=FRAME_PADDING)

            ttk.Label(group0, text=my_tab + "Base Case" + my_tab,
                      font=NORM_FONT).grid(row=0, column=1, **pad_opts)
            for i in range(1, self.data_cont.num_plans):
                ttk.Label(group0, text=my_tab + "Alternative " + str(i) + my_tab,
                          font=NORM_FONT).grid(row=0, column=(i+1), **pad_opts)
                ttk.Label(group0, text=self.data_cont.plan_list[i].name,
                          font=SMALL_FONT).grid(row=1, column=(i+1), **pad_opts)
                self.data_cont.plan_list[i].bens.monte(1000)

            ben_label = ttk.Label(group0, text="Benefits", font=SMALL_FONT, foreground="blue")
            ben_label.grid(row=2, column=0, sticky="w", **pad_opts)

            # ===== Total Benefits
            disaster_ben_lbl = ttk.Label(group0, text="Disaster Economic Benefits", font=NORM_FONT)
            disaster_ben_lbl.grid(row=4, column=0, sticky="w", **pad_opts)
            res_rec_lbl = ttk.Label(group0, text=my_tab + "Response and Recovery Costs",
                                    font=SMALL_FONT)
            res_rec_lbl.grid(row=5, column=0, sticky="w", **pad_opts)
            dir_loss_lbl = ttk.Label(group0, text=my_tab + "Direct Losses", font=SMALL_FONT)
            dir_loss_lbl.grid(row=6, column=0, sticky="w", **pad_opts)
            id_loss_lbl = ttk.Label(group0, text=my_tab + "Indirect Losses", font=SMALL_FONT)
            id_loss_lbl.grid(row=7, column=0, sticky="w", **pad_opts)

            disaster_non_m_ben_lbl = ttk.Label(group0, text="Disaster Non-Market Benefits",
                                               font=NORM_FONT)
            disaster_non_m_ben_lbl.grid(row=8, column=0, sticky="w", **pad_opts)
            fat_lbl = ttk.Label(group0, text=my_tab + "Value of Statistical Lives Saved",
                                font=SMALL_FONT)
            fat_lbl.grid(row=9, column=0, sticky="w", **pad_opts)
            fat_lbl2 = ttk.Label(group0, text=my_tab + "Number of Statistical Lives Saved",
                                 font=SMALL_FONT)
            fat_lbl2.grid(row=10, column=0, sticky="w", **pad_opts)

            # ===== Sums up the numbers
            self.data_cont.summer()

            non_d_ben_lbl = ttk.Label(group0, text="Non-Disaster Related Benefits",
                                      font=NORM_FONT)
            non_d_ben_lbl.grid(row=11, column=0, sticky="w", **pad_opts)

            # ===== Total Costs
            cost_label = ttk.Label(group0, text="Costs", font=SMALL_FONT, foreground="blue")
            cost_label.grid(row=12, column=0, sticky="w", **pad_opts)

            init_lbl = ttk.Label(group0, text="Initial", font=NORM_FONT)
            init_lbl.grid(row=13, column=0, sticky="w", **pad_opts)
            dir_lbl = ttk.Label(group0, text=my_tab + "Direct" + " "*39, font=SMALL_FONT)
            dir_lbl.grid(row=14, column=0, sticky="w", **pad_opts)
            id_lbl = ttk.Label(group0, text=my_tab + "Indirect", font=SMALL_FONT)
            id_lbl.grid(row=15, column=0, sticky="w", **pad_opts)
            omr_lbl = ttk.Label(group0, text=my_tab + "OMR", font=SMALL_FONT)
            omr_lbl.grid(row=16, column=0, sticky="w", **pad_opts)
            ext_lbl = ttk.Label(group0, text=my_tab + "Externalities", font=SMALL_FONT)
            ext_lbl.grid(row=17, column=0, sticky="w", **pad_opts)

            rec_lbl = ttk.Label(group0, text="Recurring Costs", font=NORM_FONT)
            rec_lbl.grid(row=18, column=0, sticky="w", **pad_opts)
            rec_omr_lbl = ttk.Label(group0, text=my_tab + "OMR", font=SMALL_FONT)
            rec_omr_lbl.grid(row=19, column=0, sticky="w", **pad_opts)
            rec_ext_lbl = ttk.Label(group0, text=my_tab + "Externalities", font=SMALL_FONT)
            rec_ext_lbl.grid(row=20, column=0, sticky="w", **pad_opts)

            # ===== Totals
            total_label = ttk.Label(group0, text="Totals", font=SMALL_FONT, foreground="blue")
            total_label.grid(row=21, column=0, sticky="w", **pad_opts)

            tot_lbl = ttk.Label(group0, text="Total: Present Expected Value", font=NORM_FONT)
            tot_lbl.grid(row=22, column=0, sticky="w", **pad_opts)
            ben_lbl = ttk.Label(group0, text=my_tab + "Benefits" + " "*24, font=SMALL_FONT)
            ben_lbl.grid(row=23, column=0, sticky="w", **pad_opts)
            cost_lbl = ttk.Label(group0, text=my_tab + "Costs", font=SMALL_FONT)
            cost_lbl.grid(row=24, column=0, sticky="w", **pad_opts)
            net_lbl = ttk.Label(group0, text=my_tab + "Net", font=SMALL_FONT)
            net_lbl.grid(row=25, column=0, sticky="w", **pad_opts)

            ttk.Label(group0, text=" ").grid(row=24, **pad_opts)
            sir_lbl = ttk.Label(group0, text=my_tab + "Savings-to-Investment Ratio",
                                font=SMALL_FONT)
            sir_lbl.grid(row=25, column=0, sticky="w", **pad_opts)
            irr_lbl = ttk.Label(group0, text=my_tab + "Internal Rate of Return", font=SMALL_FONT)
            irr_lbl.grid(row=26, column=0, sticky="w", **pad_opts)
            roi_lbl = ttk.Label(group0, text=my_tab + "Return on Investment", font=SMALL_FONT)
            roi_lbl.grid(row=27, column=0, sticky="w", **pad_opts)
            non_d_roi = ttk.Label(group0, text=my_tab + "Non-Disaster ROI", font=SMALL_FONT)
            non_d_roi.grid(row=28, column=0, sticky="w", **pad_opts)
            # === Places spaces to correct an unknown error with the window size
            ttk.Label(group0, text=" ").grid(row=30)
            ttk.Label(group0, text=" ").grid(row=31)
            ttk.Label(group0, text=" ").grid(row=32)
            ttk.Label(group0, text=" ").grid(row=33)
            ttk.Label(group0, text=" ").grid(row=34)


            for i in range(self.data_cont.num_plans):
                # Response and Recovery
                text_1 = self.data_cont.plan_list[i].bens.r_sum
                ttk.Label(group0, text='${:,.0f}'.format(text_1),
                          font=SMALL_FONT).grid(row=5, column=(i+1), sticky="e", **pad_opts)
                # Direct Benefits
                text_2 = self.data_cont.plan_list[i].bens.d_sum
                ttk.Label(group0, text='${:,.0f}'.format(text_2),
                          font=SMALL_FONT).grid(row=6, column=(i+1), sticky="e", **pad_opts)
                # Indirect Benefits
                text_3 = self.data_cont.plan_list[i].bens.i_sum
                ttk.Label(group0, text='${:,.0f}'.format(text_3),
                          font=SMALL_FONT).grid(row=7, column=(i + 1), sticky="e", **pad_opts)

                # Fatalaties Value averted
                text = self.data_cont.plan_list[i].fat.stat_value_averted
                ttk.Label(group0, text='${:,.0f}'.format(text),
                          font=SMALL_FONT).grid(row=9, column=(i + 1), sticky="e", **pad_opts)
                # Fatalaties number averted
                text = self.data_cont.plan_list[i].fat.stat_averted
                ttk.Label(group0, text='{:,.2f}'.format(text),
                          font=SMALL_FONT).grid(row=10, column=(i+1), sticky="e", **pad_opts)

                # Direct Costs
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.d_sum),
                          font=SMALL_FONT).grid(row=14, column=(i+1), sticky="e", **pad_opts)
                # Indirect Costs
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.i_sum),
                          font=SMALL_FONT).grid(row=15, column=(i+1), sticky="e", **pad_opts)
                # One-Time OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_1_sum),
                          font=SMALL_FONT).grid(row=16, column=(i+1), sticky="e", **pad_opts)
                # One-Time Extenalities
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_sum),
                          font=SMALL_FONT).grid(row=17, column=(i+1), sticky="e", **pad_opts)
                # Recurring OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_r_sum),
                          font=SMALL_FONT).grid(row=19, column=(i+1), sticky="e", **pad_opts)
                # Recurring Externalities
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_sum),
                          font=SMALL_FONT).grid(row=20, column=(i+1), sticky="e", **pad_opts)

                # Non D Bens
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.total),
                          font=SMALL_FONT).grid(row=11, column=i+1, sticky="e", **pad_opts)

                # Totals
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].total_bens),
                          font=BOLD_FONT).grid(row=23, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].total_costs),
                          font=BOLD_FONT).grid(row=24, column=(i + 1), sticky="e", **pad_opts)
                if self.data_cont.plan_list[i].net >= 0:
                    ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net),
                              font=BOLD_FONT).grid(row=25, column=(i + 1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net) + ')',
                              font=BOLD_FONT).grid(row=25, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].sir()),
                          font=SMALL_FONT).grid(row=26, column=(i + 1), sticky="e", **pad_opts)
                if type(self.data_cont.plan_list[i].irr()) == type("string"):
                    ttk.Label(group0, text=self.data_cont.plan_list[i].irr(),
                              font=SMALL_FONT).grid(row=28, column=(i+1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='{:,.1f}'.format(self.data_cont.plan_list[i].irr()) + '%',
                              font=SMALL_FONT).grid(row=28, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='{:,.1f}'.format(self.data_cont.plan_list[i].roi()) + '%',
                          font=SMALL_FONT).grid(row=29, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='{:,.1f}'.format(self.data_cont.plan_list[i].non_d_roi()) + '%',
                          font=SMALL_FONT).grid(row=30, column=(i + 1), sticky="e", **pad_opts)

            exp_button = ttk.Button(self, text="Export Summary", command=self.export)
            exp_button.grid(row=31)
            info_button = ttk.Button(self, text="More Information", command=self.info)
            info_button.grid(row=31, sticky="w")

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
            both_button.grid(row=2, padx=BASE_PADDING, pady=BASE_PADDING)

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


    root = UMainPage(data)
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
