import matplotlib as mpl
from numpy import percentile
mpl.use('Agg')
import matplotlib.pyplot as pyplot
import time
import os


def get_box_plot(lst, name):
    """Constructs a box and whisker plot off a given list of numbers.

    Saves the image to the folder /utakeout/static/img with a name constructed
    from the timestamp of the function call and the given zipcode.

    Returns: filename as string
    '"""
    figure = pyplot.figure(1,figsize=(3,2))
    ax = figure.add_subplot(111)
    ax.get_xaxis().tick_bottom()
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')

    try:
        bp = ax.boxplot(lst, vert=False, patch_artist=True)
    except:
        return None

    quart_y = None
    for box in bp['boxes']:
        box.set(color='#445878',linewidth=2)
        box.set(facecolor='#445878')
    for whisker in bp['whiskers']:
        whisker.set(color='#f05f40', linewidth=2)
    cap_count = 0
    for cap in bp['caps']:
        cap.set(color='#f05f40', linewidth=2)
        x, y = cap.get_xydata()[0]
        quart_y = y - .2
        y += .02
        if cap_count == 0:
            x -= .2
            ax.text(x, y, '{:.1f}'.format(x), horizontalalignment='right',
                    verticalalignment='center', fontsize='7', color='#969696')
        else:
            x += .2
            ax.text(x, y, '{:.1f}'.format(x), horizontalalignment='left',
                    verticalalignment='center', fontsize='7', color='#969696')
        cap_count += 1
    for median in bp['medians']:
        median.set(color='#92CDCF', linewidth=2)
        x, y = median.get_xydata()[1]
        y += .1
        ax.text(x, y, '{:.1f}'.format(x), horizontalalignment='center',fontsize='7',color='#969696')
    first_q = percentile(lst, 25)
    third_q = percentile(lst, 75)
    ax.text(first_q, quart_y, '{:.1f}'.format(first_q), horizontalalignment='center',
            fontsize='7',color='#969696')
    ax.text(third_q, quart_y, '{:.1f}'.format(third_q), horizontalalignment='center',
            fontsize='7',color='#969696')

    timestamp = str(time.time()).replace('.','')
    filename = '{}{}.png'.format(name,timestamp)
    figure.savefig(os.path.join('utakeout','static','img','plot',filename), bbox_inches='tight')
    figure.clear()
    return filename