from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontManager
import matplotlib.patches as patches
import matplotlib.colors as mcolor
from matplotlib import cm
import matplotlib.ticker as ticker
import os




def pres_count_plot(df,ax):
    plt.bar(left = df.index,width=.8,height=df['Count'],color='#382364',edgecolor='none')
    ax.set_xticks([.4+(1*x)for x in range(len(df))])
    ax.set_ylabel('Officers',fontsize = 14)
    ax.set_xticklabels([df['Category'][x]for x in range(len(df))],fontsize=10)
    ax.set_yticklabels([str(int(ax.get_yticks()[x]*.001))+'K' for x in range(len(ax.get_yticks()))],fontsize=10)

    for item in range(len(df)):
        ax.text(x=ax.get_xticks()[item],
                y=df['Count'][item],
                s="{:.1f}%".format((df['Count'][item]/df['Count'].sum())*100),
               ha='center',va='bottom')

def line_chart(x,y,xlabel=False,ylabel=False,title=False,
               figsize=(11,8),title_font=20,top=.9,labelsize=18,tickmarksize=16,
              source=False,marker=False,markersize=5,
              chart_tag='Created by the Los Angeles i-team, 2017',source_y=-.16,chart_tag_y=-.19,
              linewidth=2,linecolor='Black',label=False):

    fig = plt.figure(figsize=figsize)
    fig.suptitle(title,fontsize=title_font)
    ax = fig.add_subplot(111)
    plt.subplots_adjust(top=top)
    plt.plot(x,y,linewidth=linewidth,color=linecolor,
    clip_on=False,marker=marker,markersize=markersize,label=label)

    #set the x and y axis limits

    ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y.min(),y.max())

    #set the tick intervals - need to add

    #label axes
    ax.set_xlabel(xlabel,fontsize=labelsize)
    ax.set_ylabel(ylabel,fontsize=labelsize)

    ax.grid(alpha=.4)

    #format tick labels
    ax.tick_params(axis='both', which='major', labelsize=tickmarksize,labelcolor='#737373',pad=10)

    ax.text(0,source_y,source,transform=ax.transAxes,fontsize=14,alpha=.4)

    ax.text(0,chart_tag_y,chart_tag,transform=ax.transAxes,fontsize=14,alpha=.4)

    return fig, ax



class distributions2(object):

    def __init__ (self,df,title_='',bincolor='#3182bd',linecolor='#de2d26',edgecolor='black'):
        """
        Description
        -----------

        Parameters
        ----------
        'DF': DataFrame to use,
        'bincolor': Color for the bins
        'linecolor': Color of Kernel Density Estimate line
        'title': Title for the plot. If not specified will be blank

        Returns
        -------
        Object
        """

        self.title_ = title_
        self.bincolor = bincolor
        self.linecolor = linecolor
        self.edgecolor = edgecolor
        self.df = df

    def histo_plots_overall(self,field,min_range=20,binsize=5,max_range=80,xlabel_='Measure',type_='counts'):
        """
        Parameters
        ----------

        'Field': Numeric field from DataFarme
            Distribution field to examine
        'min_range': The lower bound for the distribution
        'binsize': length of each bin
        'max_range': The max range for the distribution
        'xlabel_': the label for the x-axis
        'type_': whether to use counts. Default is counts. Any other value produces density.

        Returns
        -------
        Distribution visualization for field


        """
        data_ = self.df[field]
        fig = plt.figure(figsize=(8,5))
        fig.suptitle(self.title_)
        ax1 = fig.add_subplot(111)

        if type_ == 'counts':
            n,bins, patches = ax1.hist(data_,[min_range+(binsize*x) for x in range(int((((max_range-min_range)/binsize)-1)))],
                                   color=self.bincolor,edgecolor=self.edgecolor,normed=False)
            ax1.set_ylabel('Officer Count',fontsize=14)
        else:
            n,bins, patches = ax1.hist(data_,[min_range+(binsize*x) for x in range(int((((max_range-min_range)/binsize)-1)))],
                                  color=self.bincolor,edgecolor=self.edgecolor,normed=True)
            data_.plot(kind='kde',ax=ax1,xlim=(min_range,max_range),color=self.linecolor)
            ax1.set_ylabel('Officer Density',fontsize=14)

        ## need to tweak this so that it's a density distribution with the axis labeled by count
        # in the meantime, will stick with just count .. if ammended, must switch the above normed to True
        #data_.plot(kind='kde',ax=ax1,xlim=(min_range,max_range),color=self.linecolor)
        #ax1.set_yticklabels([(int(round((ax1.get_yticks()[x]*bins*10000)))) for x in range(len(ax1.get_yticks()))])

        ax1.set_xlim(min_range,max_range)


        ax1.set_xlabel(xlabel_,fontsize=14)
        #ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.01))


        plt.text(.9,.8,'Count: '+str(format(self.df[field].count())),
             transform=ax1.transAxes,fontsize=12)

        plt.text(.9,.75,'Mean: '+"{0:.1f}".format(self.df[field].mean()),
             transform=ax1.transAxes,fontsize=12)

        plt.text(.9,.7,'St.Dev: '+"{0:.1f}".format(self.df[field].std()),
             transform=ax1.transAxes,fontsize=12)




    def histo_plots_cats(self,column,field,value_,min_range=20,binsize=5,max_range=80,xlabel_='Measure',
    type_='counts'):
        """
        Parameters
        ----------

        'Column': Column from DataFrame
            Subgroup column for categorical distribution
        'Value_': Value from DataFrame
            Subgroup value for categorical distribution
        'Field': Numeric field from DataFarm
            Distribution field to examine
        'min_range': The lower bound for the distribution
        'binsize': length of each bin
        'max_range': The max range for the distribution
        'xlabel_': the label for the x-axis


        Returns
        -------
        Distribution visualizations


        """


        data_ = self.df[self.df[column]==value_][field]
        fig = plt.figure(figsize=(8,5))
        fig.suptitle(self.title_+': '+str(value_)+' officers')
        ax1 = fig.add_subplot(111)


        if type_ == 'counts':

            n,bins, patches = ax1.hist(data_,[min_range+(binsize*x) for x in range(int(((max_range-min_range)/binsize)))],
                                       color=self.bincolor,edgecolor=self.edgecolor,normed=False)
            ax1.set_ylabel('Officer Count',fontsize=14)
        else:

            n,bins, patches = ax1.hist(data_,[min_range+(binsize*x) for x in range(int(((max_range-min_range)/binsize)))],
                                       color=self.bincolor,edgecolor=self.edgecolor,normed=True)
            data_.plot(kind='kde',ax=ax1,xlim=(min_range,max_range),color=self.linecolor)
            ax1.set_ylabel('Officer Density',fontsize=14)



        ax1.set_xlim(min_range,max_range)


        ax1.set_xlabel(xlabel_,fontsize=14)

        plt.text(.9,.8,'Count: '+str(format(data_.count())),
             transform=ax1.transAxes,fontsize=12)

        plt.text(.9,.75,'Mean: '+"{0:.1f}".format(data_.mean()),
             transform=ax1.transAxes,fontsize=12)

        plt.text(.9,.7,'St.Dev: '+"{0:.1f}".format(data_.std()),
             transform=ax1.transAxes,fontsize=12)

def chart_save(name,dpi=100,format='png',transparent=False):
    plt.savefig(name+'.'+format,bbox_inches = 'tight',format=format, dpi = dpi, pad_inches = .25,transparent=transparent)

def revised_base_graphs(df,figsize=(3,2),labelsize=12,grouper='DEM_GENDER',title=''):
    """
    Parameters
    ----------

    'df': Dataframe
        Dataframe to use for initial pivot counts
    'Figsize': Size of the figure
    'Labelsize': Size of visualization labels
    'Grouper': DF column to count and plot
    'Title': Title for visualization


    Returns
    -------
    Distribution visualization


    """
    df2 = df.pivot_table('EMP_EMPLOYEE_ID',grouper,aggfunc='count').sort_values()

    fig = plt.figure(figsize=figsize)
    fig.suptitle(t=title,fontsize=labelsize*1.4)
    ax = fig.add_subplot(111)
    plt.subplots_adjust(top=.8)
    ax.set_xticks([i for i,values in enumerate(df2.index)])
    plt.bar(left = [i for i,values in enumerate(df2.index)],width=.8,height=df2.values,color='#382364',edgecolor='none',zorder=2)
    ax.set_xticklabels([values for i,values in enumerate(df2.index)],fontsize=labelsize)
    ax.set_yticklabels([str(int(ax.get_yticks()[x]*.001))+'K' for x in range(len(ax.get_yticks()))],fontsize=labelsize)
    ax.set_ylabel('Officers',fontsize = labelsize*1.2)
    ax.set_ylim(0,df2.max()*1.05)
    for item in range(len(df2)):
        ax.text(x=ax.get_xticks()[item],
                y=df2.values[item],
                s="{:.1f}%".format((df2.values[item]/df2.values.sum())*100),
               ha='center',va='bottom',fontsize=labelsize)
    return fig, ax

def test_histogram_maker(data,title,passing_score,bins):
    """
    Data = Data to use for histogram
    Title = Title for histogram
    Passing_Score = Minimum passing score
    Bins = Separation valuesto use for histogram
    ------
    Return histogram plot

    """
    fig,ax = plt.subplots()
    fig.suptitle(t=title)
    counts,bins,plot = ax.hist(data,bins=bins,edgecolor='white',facecolor='#7570b3',alpha=1,zorder=2)
    ax.grid(linewidth=1,alpha=.6,zorder=1)
    ax.set_ylabel('Count',fontsize=14)
    ax.set_xlabel('Score',fontsize=14)
    ax.vlines(x=passing_score,ymin=0,ymax=counts.max(),color='red',zorder=3)
    ax.text(passing_score*.997,counts.max()*.8,'Passing Score',rotation=90,ha='right',va='center',fontsize=14)

    return fig,ax

class chart_maker(object):

    """
    Class to assist with matplotlib charts
    ------
    Initialize object with:

    title = title for plot
    title_size = title_size for plot
    alpha = transparency for plot
    ------

    """
    def __init__(self,title='Title',title_size=16,alpha=.8):
        self.title = title
        self.title_size = title_size
        self.alpha = alpha

    def initial_fig_axis(self,figsize=(11,8)):
        """
        Sets up the matplotlib figure
        set_equal to fig for use with subsequent functions
        ------

        figsize = size of the figure
        ------
        Returns figure

        """
        fig = plt.figure(figsize=figsize)
        fig.suptitle(self.title,fontsize=self.title_size,alpha=self.alpha)
        return fig

    def axes_set_up(self,fig,rows=1,columns=1,plot_num=1):
        """
        Sets up the matplolibt axes
        set_equal to ax for use with subsequent functions
        ------

        fig = Figure to use
        rows = Vertical number of plots
        columns = Horizontal number of plots
        plot_num = Mumber of plot.
        ------
        Returns axes object

        """
        ax = fig.add_subplot(rows,columns,plot_num)
        return ax

    def y_axis_setup(self,ax,min_,max_,interval=1):
        """
        easier y_axis_setup
        ------
        ax = set to ax to use
        min_ = y-axis minimum
        max_ = y-axis maximum
        interval = interval for the axis
        ------
        Returns set y-axis

        """
        yinterval = ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(interval))
        ylim = ax.set_ylim(min_,max_)
        return yinterval, ylim


    def x_axis_setup(self,ax,min_,max_,interval=1):
        """
        easier x_axis_setup
        ------
        ax = set to ax to use
        min_ = x-axis minimum
        max_ = x-axis maximum
        interval = interval for the axis
        ------
        Returns set x-axis

        """
        xinterval = ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(interval))
        xlim = ax.set_xlim(min_,max_)
        return xinterval,xlim


    def citations(self,ax,source,chart_tag,x=0,source_y=-.4,chart_tag_y=-.5,fontsize=14,color='black',alpha=.4):
        """
        Text objets for source and creditation
        ------
        ax = set to ax to use
        source = text indicating your source
        chart_tag = text indicating your creditation
        x = x-position of source and chart_tag
        source_y = y position of source
        chart_tag_y = y position of chart_tag
        fontsize = fontsize for source and chart_tag
        color = color of of source and chart_tag
        alpha = transparency
        ------
        Returns source and creditation text

        """
        source = ax.text(x,source_y,source,transform=ax.transAxes,fontsize=fontsize,color=color,alpha=alpha)
        chart_tag = ax.text(x,chart_tag_y,chart_tag,transform=ax.transAxes,fontsize=fontsize,color=color,alpha=alpha)
        return source, chart_tag

    def patch_adder(self,ax, xy=(0,0),width=1,height=1,facecolor='#f0f0f0',alpha=1):
        """
        Adds a rectangular patch to the chart
        ------
        ax = set to ax to use
        xy = bottom left of rectangular
        width = width proportion for patch to cover
        height = height proportion for patch to cover
        facecolor = color of patch
        alpha = patch transparency
        ------
        Returns rectangular patch

        """
        patch = ax.add_patch(patches.Rectangle(xy, width=width,height=height,facecolor=facecolor,alpha=alpha,transform=ax.transAxes))
        return patch

    def tick_params_(self,ax,axis='both',which='major',fontsize=16,labelcolor='#969696'):
        """
        Set global tick parameters
        ------
        ax :
            set to ax to use

        axis : {‘x’, ‘y’, ‘both’}
            Axis to set

        which : {‘major’, ‘minor’, ‘both’}
            Tick marks to set arguments to

        fontsize:
            Font size for axis ticks

        labelcolor:
            Color for ticks
        ------
        Returns set tick parameters

        """
        tick_overall_set = ax.tick_params(axis=axis, which=which, labelsize=fontsize,labelcolor='#969696')
        return tick_overall_set
