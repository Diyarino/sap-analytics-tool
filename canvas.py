# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 12:38:48 2025

@author: Diyar Altinses, M.Sc.
"""
# %% imports

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# %%

class MplCanvas(FigureCanvas):
    """Matplotlib Canvas für die Einbettung in PySide"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
