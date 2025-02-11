import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

import os
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
from sklearn import metrics
import warnings
warnings.simplefilter(action='ignore')


# Import the Data class from clean_data.py to get dataframe
from clean_data import Data

class Evaluate(Data):
    
    def __init__(self, df):
        super().__init__(df)
    
    def histograms(self):
        """
        This functions builds histograms for each independent variable to show 
        the distribution of your data
        """
        
        self.df1 = self.df[self.numeric_col]
        h = self.df1.hist(bins=10, figsize=(16,16), xlabelsize='10', ylabelsize='10', xrot=-15)
        [x.title.set_size(10) for x in h.ravel()]
        [x.yaxis.tick_left() for x in h.ravel()]
        return plt.show()
    
    def kde_plots(self):
        """
        Shows the distribution. Want the curves to look Gaussian if you standardize or normalize.
        """
        vals = []
        numeric_length = len(self.numeric_col)
        for i in range(numeric_length):
            vals.append(i)
        
        for i in vals:
            try:
                #ax = sns.distplot(self.df[self.numeric_col[i]], bins = 10)
                self.df1 = self.df[self.numeric_col[i]]
                sns.kdeplot(self.df1, shade = True)
                plt.show()
            except:
                continue
        
    def dist_plots(self):
        """
        Shows the distribution. Want the curves to look Gaussian if you standardize or normalize.
        """
        vals = []
        numeric_length = len(self.numeric_col)
        for i in range(numeric_length):
            vals.append(i)

        for i in vals:
            try:
                ax = sns.distplot(self.df[self.numeric_col[i]], bins = 10)
                plt.show()
            except:
                continue

    def show_outliers(self):
        """
        Shows outliers for each feature as their own boxplot
        """
        for x in self.df[self.numeric_col]:
            plt.figure()
            self.df.boxplot([x])
            
    def show_outliers_one_graph(self):
        """
        Shows outliers in one graph
        """
        counter = 0
        for i in self.df.columns:
            counter+=1
        
        if counter <= 12:
            chart = self.df.plot(kind='box', figsize = (counter,counter))
            chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
        elif counter <= 24:
            chart = self.df.plot(kind='box', figsize = (counter/1.5,counter/1.5))
            chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
        else:
            chart = self.df.plot(kind='box', figsize = (counter/4,counter/4))
            chart.set_xticklabels(chart.get_xticklabels(), rotation=60)
