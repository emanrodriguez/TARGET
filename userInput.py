from tkinter import *
import tkinter as tk


class getPath(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label1 = tk.Label(self, text="ENTER TARGET LINK").grid(row=0, column=0)
        self.e1 = tk.Entry(self, width=50)
        self.e1Grid = self.e1.grid(row=0, column=1)

        self.label2 = tk.Label(self, text="TARGET PIN(CARD ON FILE)").grid(row=2, column=0)
        self.e2 = tk.Entry(self, width=50)
        self.e2Grid = self.e2.grid(row=2, column=1)

        self.browse = tk.Button(self, text='Submit', command=self.submit).grid(row=8, column=1)

    def submit(self):
        self.userLink = self.e1.get()
        self.userPass = self.e2.get()
        self.destroy()


def userSubmission():
    app = getPath()
    app.mainloop()
    return str(app.userLink), str(app.userPass)
