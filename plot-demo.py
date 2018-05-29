import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

lf = ttk.Labelframe(root, text='Plot Area')
lf.grid(row=0, column=0, sticky='nwes', padx=3, pady=3)

t = np.arange(0.0,3.0,0.01)
df = pd.DataFrame({'t':t, 's':np.sin(2*np.pi*t)})

fig = Figure(figsize=(5,4), dpi=100)
ax = fig.add_subplot(111)

df.plot(x='t', y='s', ax=ax)

canvas = FigureCanvasTkAgg(fig, master=lf)
canvas.show()
canvas.get_tk_widget().grid(row=0, column=0)

root.mainloop()

# set x, y plot range
# https://stackoverflow.com/questions/27425015/python-pandas-timeseries-plots-how-to-set-xlim-and-xticks-outside-ts-plot

# set bar plot
# https://stackoverflow.com/questions/29498652/plot-bar-graph-from-pandas-dataframe
