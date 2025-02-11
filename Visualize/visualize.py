import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os
import warnings
warnings.simplefilter(action='ignore')
import pickle


# Import the Data class from clean_data.py to get dataframe
from clean_data import Data

class Visualize(Data):

    def __init__(self, df):
        super().__init__(df)

        
    def yearmonth(self, year = False, month = False, feature = None, function = None):
        data = self.df.groupby(['Year', 'Month']).agg({feature: [function]}).reset_index()
        
        if year:
            data_group = data[data['Year'] == year]
            data_group_array = data_group[['Month', feature]].to_numpy()
            fig,ax = plt.subplots()
            fig.set_size_inches(10,6)
        if month:
            y = data[data['Month'] == month]
            data_group_array = y[['Year', feature]].to_numpy()
            fig,ax = plt.subplots()
            fig.set_size_inches(18,8)
        
        # Used to make the trendline
        # x is the date (month or year)
        x = np.array(data_group_array[::1,0], dtype='int')
        # y is the values
        y = data_group_array[::,1]
        fit = np.polyfit(x,y,1)

        # trendline
        yfit = []
        for i in x:
            i = i * fit[0] + fit[1]
            yfit.append(i)

        ax = sns.barplot(x = x, y = y)
        
        ax.plot(ax.get_xticks(), yfit, alpha = .75, color = 'r')
        
        x_range = np.arange(len(y))  # the label locations
        width = 0.35  # the width of the bars
        bar_chart = ax.bar(x_range - width/2.8, y)#, width)

        # Labels, title and custom x-axis tick labels, etc.
        
        if year:
            title = str(feature) + ' for the year ' + str(year)
        if month:
            #title = feature + " per " + year
            title = str(feature) + ' for the ' + str(month) + ' Month of each Year'
        ax.set_title(title)
        ax.set_xticks(x_range)
        ax.set_xticklabels(x, rotation = 45)
        ax.set_ylabel(feature)

        self.bar_chart_labeler(bar_chart, ax)

        fig.tight_layout()

        plt.show()
     
    
    def dailygraph(self, month = None, day = None, feature = None):

        # Columns we will use
        self.cols = ['Date', feature]
        
        # Get data
        self.data = self.df[self.cols].loc[(self.df['Month'] == month) & (self.df['Day'] == day)]
        
        # Used to make the trendline
        self.x = self.data['Date'].values.tolist()
        self.y = self.data[feature].values.tolist()
        self.fit = np.polyfit(self.x,self.y,1)

        # trendline
        self.yfit = []
        for i in self.x:
            i = i * self.fit[0] + self.fit[1]
            self.yfit.append(i)

        plt.figure(figsize=(14,7))

        # Formatting to put the actual dates on the x-axis
        self.new_dates = self.data['Date'].dt.strftime('%Y-%m-%d')
        self.new_dates_2 = list(self.new_dates)

        fig,ax = plt.subplots()
        fig.set_size_inches(15,6)
        ax = sns.barplot(x = self.x, y = self.y)
        
        ax.plot(ax.get_xticks(), self.yfit, alpha = .75, color = 'r')
        
        x_range = np.arange(len(self.y))  # the label locations
        width = 0.35  # the width of the bars
        bar_chart = ax.bar(x_range - width/2.8, self.y)#, width)

        # Labels, title and custom x-axis tick labels, etc.
        title = 'Trendline of ' + str(feature) + ' for ' + str(month) + '/' + str(day)
        ax.set_title(title)
        ax.set_xticks(x_range)
        ax.set_xticklabels(self.new_dates_2, rotation = 45)
        ax.set_ylabel(feature)


        self.bar_chart_labeler(bar_chart, ax)

        fig.tight_layout()

        plt.show()
     
        
    def aggregations(self, year = False, month = False, feature = None, function = None):

        if year:
            year = 'Year'
            date = self.df.groupby(year)
            if function == 'sum':
                agg = date[feature].agg(np.sum)
            if function == 'mean':
                agg = date[feature].agg(np.mean)

            # Create a datafarme 
            aggdf = pd.DataFrame(agg,columns=[feature])
            aggdf.reset_index(inplace=True)
            
            # Used to make the trendline
            x = aggdf[year].values.tolist()
            y = aggdf[feature].values.tolist()
            fit = np.polyfit(x,y,1)

            
        elif month:
            month = 'Month'
            date = self.df.groupby(month)
            if function == 'sum':
                agg = date[feature].agg(np.sum)
            if function == 'mean':
                agg = date[feature].agg(np.mean)

            # Create a datafarme 
            aggdf = pd.DataFrame(agg,columns=[feature])
            aggdf.reset_index(inplace=True) 
            
            # Used to make the trendline
            x = aggdf[month].values.tolist()
            y = aggdf[feature].values.tolist()
            
        fit = np.polyfit(x,y,1)
        # trendline
        yfit = []
        for i in x:
            i = i * fit[0] + fit[1]
            yfit.append(i)

        fig,ax = plt.subplots()
        fig.set_size_inches(14,6)
        ax = sns.barplot(x = x, y = y)

        ax.plot(ax.get_xticks(), yfit, alpha = .75, color = 'r')

        x_range = np.arange(len(y))  # the label locations
        width = 0.35  # the width of the bars
        bar_chart = ax.bar(x_range - width/2.8, y)#, width)

        # Labels, title and custom x-axis tick labels, etc.
        if month:
            title = 'Trendline of ' + str(feature) + ' Aggregated for all ' + str(month) + ' of the Year'
        if year:
            title = 'Trendline of ' + str(feature) + ' Aggregated for all Years'

        ax.set_title(title)
        ax.set_xticks(x_range)
        ax.set_xticklabels(x, rotation = 45)
        ax.set_ylabel(feature)

        self.bar_chart_labeler(bar_chart, ax)

        fig.tight_layout()
        plt.show()        
        
        
    def stats(self):
        
        return self.data.describe()
    
    def bar_chart_labeler(self, bar_chart, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""

        for i in bar_chart:
            height = i.get_height()
            ax.annotate('{}'.format(round(height, 1)),
                        xy=(i.get_x() + i.get_width() / 2, height),
                        xytext=(0, 1),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
