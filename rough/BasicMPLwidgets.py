
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

def say_something(x):
    """
    Print the current widget value in short sentence
    """
    print(f'Widget says: {x}')
 
widgets.interact(say_something, x=[0, 1, 2, 3])
widgets.interact(say_something, x=(0, 10, 1))
widgets.interact(say_something, x=(0, 10, .5))
_ = widgets.interact(say_something, x=True)
 

#############   DOES NOT WORK 

# set up plot
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_ylim([-4, 4])
ax.grid(True)
 
# generate x values
x = np.linspace(0, 2 * np.pi, 100)
 
 
def my_sine(x, w, amp, phi):
    """
    Return a sine for x with angular frequeny w and amplitude amp.
    """
    return amp*np.sin(w * (x-phi))

ax.plot(x, my_sine(x, w = 1.0, amp=1, phi=0), color='C0')
plt.draw()

 
@widgets.interact(w=(0, 10, 1), amp=(0, 4, .1), phi=(0, 2*np.pi+0.01, 0.01))
def update(w = 1.0, amp=1, phi=0):
    """Remove old lines from plot and plot new one"""
    # [l.remove() for l in ax.lines]
    ax.plot(x, my_sine(x, w, amp, phi), color='C0')




#############   DOES NOT WORK 
# https://stackoverflow.com/questions/56234947/python-plot-with-interactive-dropdown-menu



import matplotlib.pyplot as plt
import ipywidgets as widgets
import pandas as pd


def plot_w(dataframe,ticker):

    I = data_df.columns == ticker

    print(data_df.loc[:, I].head(10))
    #Code fails in the line below. 
    df = dataframe.loc[:, I].plot(x=dataframe.index, y=dataframe[ticker], style=['-bo'], figsize=(8, 5), fontsize=11, legend='False')

    plt.plot(df[ticker], label = ticker)
    #plt.plot(df["AMZN"], label = "Amazon")

    plt.legend(loc = "upper center", shadow = True, fontsize = "small", facecolor = "black")

    plt.show()

widgets.interact(plot_w,
    dataframe = widgets.fixed(data_df),
    ticker = widgets.Dropdown(
            options=data_df.columns,
            value='ATVI',
            description='Company ticker:',
            disabled=False,
        )
)