from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import dateutil.parser
import datetime as dt
import calendar
import matplotlib as mpl
import StringIO
from numpy import cumsum

def plot_total(competitors, dates, values):
    """
    Plots all progress from the beginning to the end.
    """
    color = '#F7F9FE'
    # Create a dictonary with every competitor pointing to an empty list
    plot_values = dict([(compet, []) for compet in competitors])
    plot_dates = []

    # Set up the time period to plot
    begin_date = dt.datetime(2011,9,1)
    end_date = dt.datetime(2012,6,30)
    delta = dt.timedelta(days=1)
    
    # arrange the data
    date = begin_date
    while date != end_date:
        plot_dates.append(date)        
        for competitor in competitors:
            # If a workout has been performed at the current date append the 
            # value to plot_values. Else append 0
            
            if date in dates[competitor]:
                plot_values[competitor].append(values[competitor][dates[competitor].index(date)])
            else:
                plot_values[competitor].append(0)            
        date += delta

    # make the plot
    fig = Figure(facecolor=color, edgecolor=color)
    ax = fig.add_subplot(111)
    mpl_dates = mpl.dates.date2num(plot_dates)
    #! PART HAS TO BE GENERALIZED !#
    ax.plot_date(mpl_dates, cumsum(plot_values['Viktor']), linestyle='-',
                                    marker='None', label='Viktor',color="green")
    ax.plot_date(mpl_dates, cumsum(plot_values['Kim']), linestyle='-',
                                    marker='None', label='Kim', color="blue")
    ax.plot_date(mpl_dates, cumsum(plot_values['Olof']), linestyle='-',
                                    marker='None', label='Olof', color="red")
    #! -------------------------- !#
    
    ax.legend(loc=2)

    # formatting
    dateFmt = mpl.dates.DateFormatter('%b')
    ax.xaxis.set_major_formatter(dateFmt)
    monthsLoc = mpl.dates.MonthLocator()
    ax.xaxis.set_major_locator(monthsLoc)
    fig.autofmt_xdate(bottom=0.18)

    # print to StringIO object and return the value
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    return png_output.getvalue()
            
def plot_month(competitors, year, month, dates, values):
    """
    Plots the progress of a given month
    """
    color = '#F7F9FE'
    # Create a dictonary with every competitor pointing to an empty list
    plot_values = dict([(compet, []) for compet in competitors])
    plot_dates = []
    
    # arrange the data  
    days_in_month = calendar.monthrange(year,month)[1]              
    date = dt.datetime(year,month,1) 
    delta = dt.timedelta(days=1)  
    
    for i in range(days_in_month):
        plot_dates.append(date)
        for competitor in competitors:
            # If a workout has been performed at the current date append the 
            # value to plot_values. Else append the value 0
            if date in dates[competitor]:
                plot_values[competitor].append(values[competitor][dates[competitor].index(date)])
            else:
                plot_values[competitor].append(0)            
        date += delta

    # make the plot
    fig = Figure(facecolor=color , edgecolor = color)
    ax = fig.add_subplot(111)
    mpl_dates = mpl.dates.date2num(plot_dates)
    ax.plot_date(mpl_dates, cumsum(plot_values['Viktor']), linestyle='-',
                                marker='None', label='Viktor', color='green')
    ax.plot_date(mpl_dates, cumsum(plot_values['Kim']), linestyle='-',
                                    marker='None', label='Kim', color = 'blue')
    ax.plot_date(mpl_dates, cumsum(plot_values['Olof']), linestyle='-',
                                    marker='None', label='Olof', color='red')
    ax.legend(loc=2)
    
    # formatting
    dateFmt = mpl.dates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(dateFmt)  
    daysLoc = mpl.dates.AutoDateLocator(maxticks = 7)
    ax.xaxis.set_major_locator(daysLoc)
    fig.autofmt_xdate(bottom=0.18)
    
    #print and send 
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)#,fig.get_facecolor())
    return png_output.getvalue()
        
            
