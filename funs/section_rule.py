import numpy as np
from util_funs import *

def ruleCutSection(rule, settings):

    reportStr = ''

    # Creating this function has proved more difficult than anticipated. 
    
    # There are many rules that could be checked with a cut-section based approach. These include:
    # 1. Number of sections on front wing, rear wing, nose and floor.  
    # 2. Overhang/Top-bottom visibility of the floor.
    # 3. Minimum area rules for nose crash-structure.
    # 4. Leading-edge Trailing-edge overhang requirements on front wing. 

    # Currently the most promising method seems to be to use vtk to create the outline of the cut section. 
    # As in cut_test2.py
    # This can be rendered as a numpy array, to be analysed further in code. (as in obscure rule) 
    
    return reportStr