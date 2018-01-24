"""
   File:          VertScroll.py
   Author:        Username Gonzo on stackOverflow,
                  Shannon Grubb
   Description:   Gives a scrollbar to all pages, especially for use in long
                  ones. Note that I made several notable changes, however a
                  majority of the code is copied directly from that given by
                  Gonzo in the following question on Stack Overflow.
   http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame/16198198#16198198
"""

from tkinter import Scrollbar, Canvas, Frame, TclError
from tkinter import NW


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise TclError("cannot use place with this widget")


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = AutoScrollbar(self)
        vscrollbar.grid(row=0, column=1, sticky='NS')

        self.canvas = Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='NSEW')

        # Make canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)

        interior_id = \
            self.canvas.create_window(0, 0, anchor=NW, window=interior)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            default_height = 717
            self.canvas.update_idletasks()
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
            new_height = max(default_height, parent.winfo_height())
            self.canvas.config(height=new_height)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            self.canvas.update_idletasks()
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(
                    interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
