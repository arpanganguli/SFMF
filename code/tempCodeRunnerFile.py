"""The aim of this module is to calculate factor sensitvity, w_i. This is done using both the Maximum Likelihood Estimation (MLE) technique and calculating it from the Probabilty of Default.
    """

# ==============================================================================================================================================
# import relevant packages
from __init__ import ImportedDataframe, generate_standard_normal_rv
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from random import uniform
import matplotlib.pyplot as plt
import os

HOME = os.getcwd()
print(HOME)