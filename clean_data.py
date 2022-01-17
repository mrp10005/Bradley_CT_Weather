import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


class Data:
    def __init__(self, df=''):
        self.df = df
        
        self.non_numeric = []
        for x in self.df.select_dtypes(exclude='number'):
            self.non_numeric.append(x)
        self.numeric_col = []
        for x in self.df.select_dtypes(include='number'):
            self.numeric_col.append(x)
