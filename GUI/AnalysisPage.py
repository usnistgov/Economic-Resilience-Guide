"""
   File:          AnalysisPage.py
   Author:        Shannon Grubb
   Description:   Interacts with EconGuide.py, builds the final analysis results.
"""

import tkinter as tk
from tkinter import ttk     #for pretty buttons/labels
from tkinter import messagebox

from GUI.Constants import SMALL_FONT, LARGE_FONT, NORM_FONT, BOLD_FONT
from GUI.Constants import FRAME_PADDING, FIELDX_PADDING, FIELDY_PADDING, BASE_PADDING

from Data.Exports import csv_export, word_export, write_pct

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
            width_size = min(self.data_cont.num_plans * 200 + 500, 1500)
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
            title = ttk.Label(frame, text="Outputs of Economic Evaluation", font=LARGE_FONT)
            title.grid(row=0, padx=FRAME_PADDING, pady=FRAME_PADDING)

            title2 = ttk.Label(frame, text="[" + self.data_cont.title + "]",
                               font=LARGE_FONT)
            title2.grid(row=1, padx=FIELDX_PADDING, pady=FIELDY_PADDING)


        def create_widgets(self, frame):
            """Widgets include: menu bar, **temporary** home button"""
            # ===== Labels the plans
            my_tab = " " * 5
            pad_opts = {'padx': FIELDX_PADDING, 'pady':FIELDY_PADDING}
            title_opts = {'column':0, 'sticky':"w", 'padx': FIELDX_PADDING, 'pady':FIELDY_PADDING}
            field_opts = {'sticky':"e", 'padx': FIELDX_PADDING, 'pady':FIELDY_PADDING}

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

            ttk.Label(group0, text="Benefits", font=SMALL_FONT,
                      foreground="blue").grid(row=2, **title_opts)

            # ===== Total Benefits
            ttk.Label(group0, text="Disaster Economic Benefits",
                      font=NORM_FONT).grid(row=4, **title_opts)
            ttk.Label(group0, text=my_tab + "Response and Recovery Costs",
                      font=SMALL_FONT).grid(row=5, **title_opts)
            ttk.Label(group0, text=my_tab + "Direct Losses",
                      font=SMALL_FONT).grid(row=6, **title_opts)
            ttk.Label(group0, text=my_tab + "Indirect Losses",
                      font=SMALL_FONT).grid(row=7, **title_opts)

            ttk.Label(group0, text="Disaster Non-Market Benefits",
                      font=NORM_FONT).grid(row=8, **title_opts)
            ttk.Label(group0, text=my_tab + "Value of Statistical Lives Saved",
                      font=SMALL_FONT).grid(row=9, **title_opts)
            ttk.Label(group0, text=my_tab + "Number of Statistical Lives Saved",
                      font=SMALL_FONT).grid(row=10, **title_opts)

            ttk.Label(group0, text="Non-Disaster Related Benefits",
                      font=NORM_FONT).grid(row=11, **title_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=12, **title_opts)
            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=13, **title_opts)

            # ===== Total Costs
            ttk.Label(group0, text="Costs", font=SMALL_FONT,
                      foreground="blue").grid(row=14, **title_opts)
            ttk.Label(group0, text="Direct and Indirect Costs",
                      font=NORM_FONT).grid(row=15, **title_opts)
            ttk.Label(group0, text=my_tab + "Direct Costs" + " " * 39,
                      font=SMALL_FONT).grid(row=16, **title_opts)
            ttk.Label(group0, text=my_tab + "Indirect Costs",
                      font=SMALL_FONT).grid(row=17, **title_opts)
            ttk.Label(group0, text="OMR Costs",
                      font=NORM_FONT).grid(row=18, **title_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=19, **title_opts)
            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=20, **title_opts)

            ttk.Label(group0, text="Externalities", font=SMALL_FONT,
                      foreground="blue").grid(row=21, **title_opts)
            ttk.Label(group0, text="Positive",
                      font=NORM_FONT).grid(row=22, **title_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=23, **title_opts)
            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=24, **title_opts)
            ttk.Label(group0, text="Negative",
                      font=NORM_FONT).grid(row=25, **title_opts)
            ttk.Label(group0, text=my_tab + "One-Time",
                      font=SMALL_FONT).grid(row=26, **title_opts)
            ttk.Label(group0, text=my_tab + "Recurring",
                      font=SMALL_FONT).grid(row=27, **title_opts)

            # ===== Totals
            ttk.Label(group0, text="Totals", font=SMALL_FONT,
                      foreground="blue").grid(row=28, **title_opts)

            ttk.Label(group0, text="Total: Present Expected Value",
                      font=NORM_FONT).grid(row=29, **title_opts)
            ttk.Label(group0, text=my_tab + "Benefits" + " " * 24,
                      font=BOLD_FONT).grid(row=30, **title_opts)
            ttk.Label(group0, text=my_tab + "Costs",
                      font=BOLD_FONT).grid(row=31, **title_opts)
            if any_ext:
                ttk.Label(group0, text=my_tab + "Externalities",
                          font=BOLD_FONT).grid(row=32, **title_opts)
                ttk.Label(group0, text=my_tab + "Net with Externalities",
                          font=BOLD_FONT).grid(row=33, **title_opts)
                ttk.Label(group0, text=my_tab + "Benefit-to-Cost Ratio with Externalities",
                          font=SMALL_FONT).grid(row=34, **title_opts)
                ttk.Label(group0, text=my_tab + "Internal Rate of Return with Externalities",
                          font=SMALL_FONT).grid(row=35, **title_opts)
                ttk.Label(group0, text=my_tab + "Return on Investment with Externalities",
                          font=SMALL_FONT).grid(row=36, **title_opts)
                ttk.Label(group0, text=my_tab + "Non-Disaster ROI with Externalities",
                          font=SMALL_FONT).grid(row=37, **title_opts)

            ttk.Label(group0, text=my_tab + "Net",
                      font=BOLD_FONT).grid(row=38, **title_opts)
            ttk.Label(group0, text=my_tab + "Benefit-to-Cost Ratio",
                      font=SMALL_FONT).grid(row=39, **title_opts)
            ttk.Label(group0, text=my_tab + "Internal Rate of Return",
                      font=SMALL_FONT).grid(row=40, **title_opts)
            ttk.Label(group0, text=my_tab + "Return on Investment",
                      font=SMALL_FONT).grid(row=41, **title_opts)
            ttk.Label(group0, text=my_tab + "Non-Disaster ROI",
                      font=SMALL_FONT).grid(row=42, **title_opts)

            # === Places spaces to correct an unknown error with the window size
            ttk.Label(group0, text=" ").grid(row=43)
            ttk.Label(group0, text=" ").grid(row=44)
            ttk.Label(group0, text=" ").grid(row=45)
            ttk.Label(group0, text=" ").grid(row=46)
            ttk.Label(group0, text=" ").grid(row=47)


            for i in range(self.data_cont.num_plans):
                plan = self.data_cont.plan_list[i]
                # Response and Recovery
                ttk.Label(group0, text='${:,.0f}'.format(plan.bens.r_sum),
                          font=SMALL_FONT).grid(row=5, column=(i+1), **field_opts)
                # Direct Benefits
                ttk.Label(group0, text='${:,.0f}'.format(plan.bens.d_sum),
                          font=SMALL_FONT).grid(row=6, column=(i+1), **field_opts)
                # Indirect Benefits
                ttk.Label(group0, text='${:,.0f}'.format(plan.bens.i_sum),
                          font=SMALL_FONT).grid(row=7, column=(i + 1), **field_opts)

                # Fatalaties Value averted
                ttk.Label(group0, text='${:,.0f}'.format(plan.fat.stat_value_averted),
                          font=SMALL_FONT).grid(row=9, column=(i + 1), **field_opts)
                # Fatalaties number averted
                ttk.Label(group0, text='{:,.2f}'.format(plan.fat.stat_averted),
                          font=SMALL_FONT).grid(row=10, column=(i+1), **field_opts)

                # Non D Bens
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.nond_bens.one_sum),
                          font=SMALL_FONT).grid(row=12, column=i+1, **field_opts)
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.nond_bens.r_sum),
                          font=SMALL_FONT).grid(row=13, column=i+1, **field_opts)

                # Direct Costs
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.costs.d_sum),
                          font=SMALL_FONT).grid(row=16, column=(i+1), **field_opts)
                # Indirect Costs
                ttk.Label(group0, text='${:,.0f}'.format(plan.costs.i_sum),
                          font=SMALL_FONT).grid(row=17, column=(i+1), **field_opts)
                # One-Time OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.costs.omr_1_sum),
                          font=SMALL_FONT).grid(row=19, column=(i+1), **field_opts)
                # Recurring OMR
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.costs.omr_r_sum),
                          font=SMALL_FONT).grid(row=20, column=(i+1), **field_opts)

                # Externalities
                # One-Time Extenalities Positive
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.exts.one_sum_p),
                          font=SMALL_FONT).grid(row=23, column=(i+1), **field_opts)
                # Recurring Externalities Positive
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.exts.r_sum_p),
                          font=SMALL_FONT).grid(row=24, column=(i+1), **field_opts)
                # One-Time Extenalities Negative
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.exts.one_sum_n),
                          font=SMALL_FONT).grid(row=26, column=(i+1), **field_opts)
                # Recurring Externalities Negative
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.exts.r_sum_n),
                          font=SMALL_FONT).grid(row=27, column=(i+1), **field_opts)

                # Totals
                ttk.Label(group0,
                          text='${:,.0f}'.format(plan.total_bens),
                          font=BOLD_FONT).grid(row=30, column=(i + 1), **field_opts)
                ttk.Label(group0, text='${:,.0f}'.format(plan.total_costs),
                          font=BOLD_FONT).grid(row=31, column=(i + 1), **field_opts)
                if any_ext:
                    if (plan.exts.total_p - plan.exts.total_n) >= 0:
                        ttk.Label(group0,
                                  text='${:,.0f}'.format(plan.exts.total_p - plan.exts.total_n),
                                  font=BOLD_FONT).grid(row=32, column=(i + 1), **field_opts)
                    else:
                        ttk.Label(group0,
                                  text=('('+'${:,.0f}'.format(plan.exts.total_p-plan.exts.total_n)
                                        +')'),
                                  font=BOLD_FONT).grid(row=32, column=(i + 1), **field_opts)
                    if plan.net_w_ext >= 0:
                        ttk.Label(group0, text='${:,.0f}'.format(plan.net_w_ext),
                                  font=BOLD_FONT).grid(row=33, column=(i + 1), **field_opts)
                    else:
                        ttk.Label(group0,
                                  text='(' + '${:,.0f}'.format(plan.net_w_ext) + ')',
                                  font=BOLD_FONT).grid(row=33, column=(i + 1), **field_opts)
                    ttk.Label(group0, text=write_pct(plan.bcr(w_ext=True), w_pct=False),
                              font=SMALL_FONT).grid(row=34, column=(i+1), **field_opts)
                    ttk.Label(group0, text=write_pct(plan.irr(w_ext=True)),
                              font=SMALL_FONT).grid(row=35, column=(i+1), **field_opts)
                    ttk.Label(group0, text=write_pct(plan.roi(w_ext=True)),
                              font=SMALL_FONT).grid(row=36, column=(i+1), **field_opts)
                    ttk.Label(group0, text=write_pct(plan.non_d_roi(w_ext=True)),
                              font=SMALL_FONT).grid(row=37, column=(i+1), **field_opts)

                if plan.net >= 0:
                    ttk.Label(group0, text='${:,.0f}'.format(plan.net),
                              font=BOLD_FONT).grid(row=38, column=(i + 1), **field_opts)
                else:
                    ttk.Label(group0,
                              text='(' + '${:,.0f}'.format(plan.net) + ')',
                              font=BOLD_FONT).grid(row=38, column=(i + 1), **field_opts)

                ttk.Label(group0, text=write_pct(plan.bcr(), w_pct=False),
                          font=SMALL_FONT).grid(row=39, column=(i+1), **field_opts)
                ttk.Label(group0, text=write_pct(plan.irr()),
                          font=SMALL_FONT).grid(row=40, column=(i+1), **field_opts)
                ttk.Label(group0, text=write_pct(plan.roi()),
                          font=SMALL_FONT).grid(row=41, column=(i+1), **field_opts)
                ttk.Label(group0, text=write_pct(plan.non_d_roi()),
                          font=SMALL_FONT).grid(row=42, column=(i+1), **field_opts)

            ttk.Button(self, text="Export Summary", command=self.export).grid(row=6)
            ttk.Button(self, text="More Information", command=self.info).grid(row=6, sticky="w")

        def export(self):
            """Prompts the user to select how to export the Analysis Summary"""
            popup = tk.Tk()

            def leavemini():
                """Destroys popup """
                popup.destroy()

            def document():
                """Destroys popup and calls docx export."""
                leavemini()
                word_export(self.data_cont)

            def commas():
                """Destroys popup and calls csv export."""
                leavemini()
                csv_export(self.data_cont)

            def both():
                """Destroys popup and calls docx and csv export."""
                leavemini()
                word_export(self.data_cont)
                csv_export(self.data_cont)

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
                                "For information regarding any of the particular benefits or "
                                "costs, please refer back to the previous pages of the particular"
                                " benefit or cost. The corresponding pages contain specific "
                                "information to their related benefit or cost.\n\n"
                                "The following terms are defined:\n\n"
                                "    Benefit-to-Cost Ratio:\n"
                                "            Used to determine whether the potential savings of a "
                                "project justifies the initial investment and following maintenance"
                                " costs. The higher the ratio, the greater the savings; this "
                                "number can also be negative.\n\n"
                                "    Internal Rate of Return:\n"
                                "            This is the discount rate that makes the Net Present "
                                "Value of all net cash flows of a project equal zero. It measures "
                                "the profitability of potential investments. Generally speaking, "
                                "the higher this number, the more debcrable the project.\n\n"
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
