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

from Data.Exports import csv_export_uncert, word_export_uncert

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
            width_size = min(self.data_cont.num_plans * 200 + 300, 1500)
            self.container.grid_rowconfigure(0, weight=1, minsize=800)
            self.container.grid_columnconfigure(0, weight=1, minsize=width_size)

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

            any_ext = False
            for plan in self.data_cont.plan_list:
                if len(plan.exts.indiv) > 0:
                    any_ext = True

            ttk.Label(group0, text=my_tab + "Base Case" + my_tab,
                      font=NORM_FONT).grid(row=0, column=1, **pad_opts)
            for i in range(1, self.data_cont.num_plans):
                ttk.Label(group0, text=my_tab + "Alternative " + str(i) + my_tab,
                          font=NORM_FONT).grid(row=0, column=(i+1), **pad_opts)
                ttk.Label(group0, text=self.data_cont.plan_list[i].name,
                          font=SMALL_FONT).grid(row=1, column=(i+1), **pad_opts)

            ben_label = ttk.Label(group0, text="Benefits", font=SMALL_FONT, foreground="blue")
            ben_label.grid(row=2, column=0, sticky="w", **pad_opts)

            # ===== Total Benefits
            deb_index = 4
            disaster_ben_lbl = ttk.Label(group0, text="Disaster Economic Benefits", font=NORM_FONT)
            disaster_ben_lbl.grid(row=deb_index, column=0, sticky="w", **pad_opts)
            res_rec_lbl = ttk.Label(group0, text=my_tab + "Response and Recovery Costs",
                                    font=BOLD_FONT)
            res_rec_lbl.grid(row=deb_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=deb_index+2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=deb_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=deb_index+4, column=0, sticky="w", **pad_opts)
            dir_loss_lbl = ttk.Label(group0, text=my_tab + "Direct Losses", font=BOLD_FONT)
            dir_loss_lbl.grid(row=deb_index+5, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=deb_index+6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=deb_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=deb_index+8, column=0, sticky="w", **pad_opts)
            id_loss_lbl = ttk.Label(group0, text=my_tab + "Indirect Losses", font=BOLD_FONT)
            id_loss_lbl.grid(row=deb_index + 9, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=deb_index+10, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=deb_index+11, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=deb_index+12, column=0, sticky="w", **pad_opts)

            dmb_index = deb_index + 13
            disaster_non_m_ben_lbl = ttk.Label(group0, text="Disaster Non-Market Benefits",
                                               font=NORM_FONT)
            disaster_non_m_ben_lbl.grid(row=dmb_index, column=0, sticky="w", **pad_opts)
            fat_lbl = ttk.Label(group0, text=my_tab + "Value of Statistical Lives Saved",
                                font=SMALL_FONT)
            fat_lbl.grid(row=dmb_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=dmb_index+2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=dmb_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=dmb_index+4, column=0, sticky="w", **pad_opts)
            fat_lbl2 = ttk.Label(group0, text=my_tab + "Number of Statistical Lives Saved",
                                 font=SMALL_FONT)
            fat_lbl2.grid(row=dmb_index + 5, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=dmb_index+6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=dmb_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=dmb_index+8, column=0, sticky="w", **pad_opts)

            # ===== Sums up the numbers
            self.data_cont.summer()

            ndrb_index = dmb_index + 9
            non_d_ben_lbl = ttk.Label(group0, text="Non-Disaster Related Benefits",
                                      font=NORM_FONT)
            non_d_ben_lbl.grid(row=ndrb_index, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=ndrb_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=ndrb_index+2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=ndrb_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=ndrb_index+4, column=0, sticky="w", **pad_opts)

            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=ndrb_index + 5, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=ndrb_index+6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=ndrb_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=ndrb_index+8, column=0, sticky="w", **pad_opts)


            # ===== Total Costs
            cost_index = ndrb_index + 9
            cost_label = ttk.Label(group0, text="Costs", font=SMALL_FONT, foreground="blue")
            cost_label.grid(row=cost_index, column=0, sticky="w", **pad_opts)

            ic_index = cost_index + 1
            init_lbl = ttk.Label(group0, text="Direct and Indirect Costs", font=NORM_FONT)
            init_lbl.grid(row=ic_index, column=0, sticky="w", **pad_opts)
            dir_lbl = ttk.Label(group0, text=my_tab + "Direct Costs" + " "*39, font=SMALL_FONT)
            dir_lbl.grid(row=ic_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=ic_index+2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=ic_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=ic_index+4, column=0, sticky="w", **pad_opts)

            id_lbl = ttk.Label(group0, text=my_tab + "Indirect Costs", font=SMALL_FONT)
            id_lbl.grid(row=ic_index + 5, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=ic_index+6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=ic_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=ic_index+8, column=0, sticky="w", **pad_opts)

            rc_index = ic_index + 9
            rec_lbl = ttk.Label(group0, text="OMR Costs", font=NORM_FONT)
            rec_lbl.grid(row=rc_index, column=0, sticky="w", **pad_opts)
            rec_omr_lbl = ttk.Label(group0, text=my_tab + "One-Time", font=SMALL_FONT)
            rec_omr_lbl.grid(row=rc_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=rc_index+2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=rc_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=rc_index+4, column=0, sticky="w", **pad_opts)
            rec_ext_lbl = ttk.Label(group0, text=my_tab + "Recurring", font=SMALL_FONT)
            rec_ext_lbl.grid(row=rc_index + 5, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=rc_index+6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=rc_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=rc_index+8, column=0, sticky="w", **pad_opts)


            # ===== Externalities
            e_index = rc_index + 9
            ttk.Label(group0, text="Externalities", font=SMALL_FONT,
                      foreground="blue").grid(row=e_index, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text="Positive",
                      font=NORM_FONT).grid(row=e_index + 1, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=e_index + 2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=e_index+3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=e_index+4, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=e_index+5, column=0, sticky="w", **pad_opts)

            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=e_index + 6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=e_index+7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=e_index+8, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=e_index+9, column=0, sticky="w", **pad_opts)

            ttk.Label(group0, text="Negative",
                      font=NORM_FONT).grid(row=e_index + 10, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=e_index + 11, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=e_index+12, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=e_index+13, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=e_index+14, column=0, sticky="w", **pad_opts)

            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=e_index + 15, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=e_index+16, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=e_index+17, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=e_index+18, column=0, sticky="w", **pad_opts)


            # ===== Totals
            tot_index = e_index + 19
            total_label = ttk.Label(group0, text="Totals", font=SMALL_FONT, foreground="blue")
            total_label.grid(row=tot_index, column=0, sticky="w", **pad_opts)

            tot_lbl = ttk.Label(group0, text="Total: Present Expected Value", font=NORM_FONT)
            tot_lbl.grid(row=tot_index + 1, column=0, sticky="w", **pad_opts)
            ben_lbl = ttk.Label(group0, text=my_tab + "Benefits" + " "*24, font=BOLD_FONT)
            ben_lbl.grid(row=tot_index + 2, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 3, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 4, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 5, column=0, sticky="w", **pad_opts)
            cost_lbl = ttk.Label(group0, text=my_tab + "Costs", font=BOLD_FONT)
            cost_lbl.grid(row=tot_index + 6, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 7, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 8, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 9, column=0, sticky="w", **pad_opts)
            net_lbl = ttk.Label(group0, text=my_tab + "Net", font=BOLD_FONT)
            net_lbl.grid(row=tot_index + 10, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 11, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 12, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 13, column=0, sticky="w", **pad_opts)
            if any_ext:
                ttk.Label(group0, text=my_tab + "Net with Externalities",
                          font=BOLD_FONT).grid(row=tot_index + 14, column=0, sticky="w", **pad_opts)
                ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                        font=SMALL_FONT).grid(row=tot_index + 15, column=0, sticky="w", **pad_opts)
                ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                        font=BOLD_FONT).grid(row=tot_index + 16, column=0, sticky="w", **pad_opts)
                ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                        font=SMALL_FONT).grid(row=tot_index + 17, column=0, sticky="w", **pad_opts)

            sir_lbl = ttk.Label(group0, text=my_tab + "Savings-to-Investment Ratio",
                                font=BOLD_FONT)
            sir_lbl.grid(row=tot_index + 18, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 19, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 20, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 21, column=0, sticky="w", **pad_opts)

            irr_lbl = ttk.Label(group0, text=my_tab + "Internal Rate of Return", font=BOLD_FONT)
            irr_lbl.grid(row=tot_index + 22, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 23, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 24, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 25, column=0, sticky="w", **pad_opts)

            roi_lbl = ttk.Label(group0, text=my_tab + "Return on Investment", font=BOLD_FONT)
            roi_lbl.grid(row=tot_index + 26, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 27, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 28, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 29, column=0, sticky="w", **pad_opts)

            non_d_roi = ttk.Label(group0, text=my_tab + "Non-Disaster ROI", font=BOLD_FONT)
            non_d_roi.grid(row=tot_index + 30, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Lower Bound",
                      font=SMALL_FONT).grid(row=tot_index + 31, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Point Estimate",
                      font=BOLD_FONT).grid(row=tot_index + 32, column=0, sticky="w", **pad_opts)
            ttk.Label(group0, text=my_tab + my_tab + "Upper Bound",
                      font=SMALL_FONT).grid(row=tot_index + 33, column=0, sticky="w", **pad_opts)

            # === Places spaces to correct an unknown error with the window size
            ttk.Label(group0, text=" ").grid(row=tot_index + 34)
            ttk.Label(group0, text=" ").grid(row=tot_index + 35)
            ttk.Label(group0, text=" ").grid(row=tot_index + 36)
            ttk.Label(group0, text=" ").grid(row=tot_index + 37)
            ttk.Label(group0, text=" ").grid(row=tot_index + 38)


            for i in range(self.data_cont.num_plans):
                # Response and Recovery
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.res_rec_range[0]),
                          font=SMALL_FONT).grid(row=deb_index+2, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.r_sum),
                          font=BOLD_FONT).grid(row=deb_index+3, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.res_rec_range[1]),
                          font=SMALL_FONT).grid(row=deb_index+4, column=(i+1), sticky="e", **pad_opts)
                # Direct Benefits
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.direct_range[0]),
                          font=SMALL_FONT).grid(row=deb_index+6, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.d_sum),
                          font=BOLD_FONT).grid(row=deb_index+7, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.direct_range[1]),
                          font=SMALL_FONT).grid(row=deb_index+8, column=(i+1), sticky="e", **pad_opts)
                # Indirect Benefits
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.indirect_range[0]),
                          font=SMALL_FONT).grid(row=deb_index+10, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.i_sum),
                          font=BOLD_FONT).grid(row=deb_index+11, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].bens.indirect_range[1]),
                          font=SMALL_FONT).grid(row=deb_index+12, column=(i+1), sticky="e", **pad_opts)
                # Fatalaties Value averted
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].fat.value_range[0]),
                          font=SMALL_FONT).grid(row=dmb_index + 2, column=(i + 1), sticky="e", **pad_opts)                
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].fat.stat_value_averted),
                          font=BOLD_FONT).grid(row=dmb_index + 3, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].fat.value_range[1]),
                          font=SMALL_FONT).grid(row=dmb_index + 4, column=(i + 1), sticky="e", **pad_opts)                
                # Fatalaties number averted
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].fat.num_range[0]),
                          font=SMALL_FONT).grid(row=dmb_index + 7, column=(i + 1), sticky="e", **pad_opts)                
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].fat.stat_averted),
                          font=BOLD_FONT).grid(row=dmb_index + 8, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].fat.num_range[1]),
                          font=SMALL_FONT).grid(row=dmb_index + 9, column=(i + 1), sticky="e", **pad_opts)                

                # Direct Costs
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.direct_range[0]),
                          font=SMALL_FONT).grid(row=ic_index + 2, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.d_sum),
                          font=BOLD_FONT).grid(row=ic_index + 3, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.direct_range[1]),
                          font=SMALL_FONT).grid(row=ic_index + 4, column=(i+1), sticky="e", **pad_opts)

                # Indirect Costs
                ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.indirect_range[0]),
                          font=SMALL_FONT).grid(row=ic_index + 6, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.i_sum),
                          font=BOLD_FONT).grid(row=ic_index + 7, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.indirect_range[1]),
                          font=SMALL_FONT).grid(row=ic_index + 8, column=(i+1), sticky="e", **pad_opts)

                # One-Time OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_one_range[0]),
                          font=SMALL_FONT).grid(row=ic_index + 11, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_1_sum),
                          font=BOLD_FONT).grid(row=ic_index + 12, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_one_range[1]),
                          font=SMALL_FONT).grid(row=ic_index + 13, column=(i+1), sticky="e", **pad_opts)

                # Recurring OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_r_range[0]),
                          font=SMALL_FONT).grid(row=ic_index + 15, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_r_sum),
                          font=BOLD_FONT).grid(row=ic_index + 16, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].costs.omr_r_range[1]),
                          font=SMALL_FONT).grid(row=ic_index + 17, column=(i+1), sticky="e", **pad_opts)

                # One-Time Extenalities Positive
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_p_range[0]),
                          font=SMALL_FONT).grid(row=e_index + 3, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_sum_p),
                          font=BOLD_FONT).grid(row=e_index + 4, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_p_range[1]),
                          font=SMALL_FONT).grid(row=e_index + 5, column=(i+1), sticky="e", **pad_opts)
                # Recurring Externalities Positive
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_p_range[0]),
                          font=SMALL_FONT).grid(row=e_index + 7, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_sum_p),
                          font=BOLD_FONT).grid(row=e_index + 8, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_p_range[1]),
                          font=SMALL_FONT).grid(row=e_index + 9, column=(i+1), sticky="e", **pad_opts)
                # One-Time Extenalities Negative
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_n_range[0]),
                          font=SMALL_FONT).grid(row=e_index + 12, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_sum_n),
                          font=BOLD_FONT).grid(row=e_index + 13, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.one_n_range[1]),
                          font=SMALL_FONT).grid(row=e_index + 14, column=(i+1), sticky="e", **pad_opts)
                # Recurring Externalities Negative
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_n_range[0]),
                          font=SMALL_FONT).grid(row=e_index + 17, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_sum_n),
                          font=BOLD_FONT).grid(row=e_index + 18, column=(i+1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].exts.r_n_range[1]),
                          font=SMALL_FONT).grid(row=e_index + 19, column=(i+1), sticky="e", **pad_opts)

                # Non D Bens
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.one_range[0]),
                          font=SMALL_FONT).grid(row=ndrb_index+2, column=i+1, sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.one_sum),
                          font=BOLD_FONT).grid(row=ndrb_index+3, column=i+1, sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.one_range[1]),
                          font=SMALL_FONT).grid(row=ndrb_index+4, column=i+1, sticky="e", **pad_opts)

                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.r_range[0]),
                          font=SMALL_FONT).grid(row=ndrb_index+6, column=i+1, sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.r_sum),
                          font=BOLD_FONT).grid(row=ndrb_index+7, column=i+1, sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].nond_bens.r_range[1]),
                          font=SMALL_FONT).grid(row=ndrb_index+8, column=i+1, sticky="e", **pad_opts)
                # Totals
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].ben_range[0]),
                          font=SMALL_FONT).grid(row=tot_index + 3, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].total_bens),
                          font=BOLD_FONT).grid(row=tot_index + 4, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].ben_range[1]),
                          font=SMALL_FONT).grid(row=tot_index + 5, column=(i + 1), sticky="e", **pad_opts)

                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].cost_range[0]),
                          font=SMALL_FONT).grid(row=tot_index + 7, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].total_costs),
                          font=BOLD_FONT).grid(row=tot_index + 8, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(self.data_cont.plan_list[i].cost_range[1]),
                          font=SMALL_FONT).grid(row=tot_index + 9, column=(i + 1), sticky="e", **pad_opts)

                if self.data_cont.plan_list[i].net_range[0] >= 0:
                    ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net_range[0]),
                              font=SMALL_FONT).grid(row=tot_index + 11, column=(i + 1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net_range[0]) + ')',
                              font=SMALL_FONT).grid(row=tot_index + 11, column=(i + 1), sticky="e", **pad_opts)
                if self.data_cont.plan_list[i].net >= 0:
                    ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net),
                              font=BOLD_FONT).grid(row=tot_index + 12, column=(i + 1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net) + ')',
                              font=BOLD_FONT).grid(row=tot_index + 12, column=(i + 1), sticky="e", **pad_opts)
                if self.data_cont.plan_list[i].net_range[1] >= 0:
                    ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net_range[1]),
                              font=SMALL_FONT).grid(row=tot_index + 13, column=(i + 1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net_range[1]) + ')',
                              font=SMALL_FONT).grid(row=tot_index + 13, column=(i + 1), sticky="e", **pad_opts)
                if any_ext:
                    if self.data_cont.plan_list[i].net_ext_range[0] >= 0:
                        ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net_ext_range[0]),
                                font=SMALL_FONT).grid(row=tot_index + 15, column=(i + 1), sticky="e", **pad_opts)
                    else:
                        ttk.Label(group0,
                                text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net_ext_range[0]) + ')',
                                font=SMALL_FONT).grid(row=tot_index + 15, column=(i + 1), sticky="e", **pad_opts)
                    if self.data_cont.plan_list[i].net_w_ext >= 0:
                        ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net_w_ext),
                                font=BOLD_FONT).grid(row=tot_index + 16, column=(i + 1), sticky="e", **pad_opts)
                    else:
                        ttk.Label(group0,
                                text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net_w_ext) + ')',
                                font=BOLD_FONT).grid(row=tot_index + 16, column=(i + 1), sticky="e", **pad_opts)
                    if self.data_cont.plan_list[i].net_ext_range[1] >= 0:
                        ttk.Label(group0, text='${:,.0f}'.format(self.data_cont.plan_list[i].net_ext_range[1]),
                                font=SMALL_FONT).grid(row=tot_index + 17, column=(i + 1), sticky="e", **pad_opts)
                    else:
                        ttk.Label(group0,
                                text='(' + '${:,.0f}'.format(self.data_cont.plan_list[i].net_ext_range[1]) + ')',
                                font=SMALL_FONT).grid(row=tot_index + 17, column=(i + 1), sticky="e", **pad_opts)

                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].sir_range[0]),
                          font=SMALL_FONT).grid(row=tot_index + 19, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].sir()),
                          font=BOLD_FONT).grid(row=tot_index + 20, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].sir_range[1]),
                          font=SMALL_FONT).grid(row=tot_index + 21, column=(i + 1), sticky="e", **pad_opts)

                if type(self.data_cont.plan_list[i].irr_range[0]) == type("string"):
                    ttk.Label(group0, text=self.data_cont.plan_list[i].irr_range[0],
                              font=SMALL_FONT).grid(row=tot_index + 23, column=(i+1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='{:,.2f}'.format(self.data_cont.plan_list[i].irr_range[0]) + '%',
                              font=SMALL_FONT).grid(row=tot_index + 23, column=(i + 1), sticky="e", **pad_opts)
                if type(self.data_cont.plan_list[i].irr()) == type("string"):
                    ttk.Label(group0, text=self.data_cont.plan_list[i].irr(),
                              font=SMALL_FONT).grid(row=tot_index + 24, column=(i+1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='{:,.2f}'.format(self.data_cont.plan_list[i].irr()) + '%',
                              font=SMALL_FONT).grid(row=tot_index + 24, column=(i + 1), sticky="e", **pad_opts)
                if type(self.data_cont.plan_list[i].irr_range[1]) == type("string"):
                    ttk.Label(group0, text=self.data_cont.plan_list[i].irr_range[1],
                              font=SMALL_FONT).grid(row=tot_index + 25, column=(i+1), sticky="e", **pad_opts)
                else:
                    ttk.Label(group0,
                              text='{:,.2f}'.format(self.data_cont.plan_list[i].irr_range[1]) + '%',
                              font=SMALL_FONT).grid(row=tot_index + 25, column=(i + 1), sticky="e", **pad_opts)
    
                ttk.Label(group0,
                        text='{:,.2f}'.format(self.data_cont.plan_list[i].roi_range[0]) + '%',
                        font=SMALL_FONT).grid(row=tot_index + 27, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0, text='{:,.2f}'.format(self.data_cont.plan_list[i].roi()) + '%',
                          font=SMALL_FONT).grid(row=tot_index + 28, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].roi_range[1]) + '%',
                          font=SMALL_FONT).grid(row=tot_index + 29, column=(i + 1), sticky="e", **pad_opts)

                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].nond_roi_range[0]) + '%',
                          font=SMALL_FONT).grid(row=tot_index + 31, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].non_d_roi()) + '%',
                          font=SMALL_FONT).grid(row=tot_index + 32, column=(i + 1), sticky="e", **pad_opts)
                ttk.Label(group0,
                          text='{:,.2f}'.format(self.data_cont.plan_list[i].nond_roi_range[1]) + '%',
                          font=SMALL_FONT).grid(row=tot_index + 33, column=(i + 1), sticky="e", **pad_opts)
            # === Places spaces to correct an unknown error with the window size
            ttk.Label(group0, text=" ").grid(row=tot_index + 34)
            ttk.Label(group0, text=" ").grid(row=tot_index + 35)
            ttk.Label(group0, text=" ").grid(row=tot_index + 36)
            ttk.Label(group0, text=" ").grid(row=tot_index + 37)
            ttk.Label(group0, text=" ").grid(row=tot_index + 38)

            button_index = 6
            exp_button = ttk.Button(self, text="Export Summary", command=self.export)
            exp_button.grid(row=button_index)
            info_button = ttk.Button(self, text="More Information", command=self.info)
            info_button.grid(row=button_index, sticky="w")

        def export(self):
            """Prompts the user to select how to export the Analysis Summary"""
            popup = tk.Tk()

            def leavemini():
                """Destroys popup """
                popup.destroy()

            def document():
                """Destroys popup and calls docx export."""
                leavemini()
                word_export_uncert(self.data_cont)

            def commas():
                """Destroys popup and calls csv export."""
                leavemini()
                csv_export_uncert(self.data_cont)

            def both():
                """Destroys popup and calls docx and csv export."""
                leavemini()
                word_export_uncert(self.data_cont)
                csv_export_uncert(self.data_cont)

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
