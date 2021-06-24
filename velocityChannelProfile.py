import numpy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from prompt import call
import tkinter as tk

ax = plt.subplots
fig = plt.subplots
cid = None
ATTEMPTS = 5


# Simple masking script
def apply_mask(data, mask):
    profile = np.zeros(len(data[:, 0, 0]))

    for i in range(len(profile)):
        profile[i] = np.sum(numpy.multiply(data[i, :, :], mask))

    return profile


# noinspection PyUnusedLocal
def closer(event):
    global ATTEMPTS
    root = tk.Tk()
    root.withdraw()
    user_str = call('Are you sure you want to close? Your work will not be saved.')
    if user_str == 'y':
        fig.canvas.mpl_disconnect(cid)
        plt.savefig("velocity_channel_profile.png")
        plt.close()
    else:
        ATTEMPTS = ATTEMPTS - 1
        print(str(ATTEMPTS) + " attempts remaining")
        # shape(globalTyp, globalData, globalName)


def velocities(naxis3, v, profile, win_str):
    global fig
    global ax

    fig, ax = plt.subplots(1, num=win_str + ": Velocity Channel Profile")

    lines = np.ones(naxis3)
    lines[0] = v[1] - v[0]
    for i in range(len(lines) - 1):
        lines[i + 1] = v[i + 1] - v[i]

    # cdelt3 my be pos or neg (don't worry about flipped)
    ax.bar(v, profile * 1000, lines, fill=0, color='white', edgecolor='black')  # Histogram plot
    ax.set_ylabel('Flux Density (mJy)', labelpad=10.0, fontsize=12)
    ax.set_xlabel('Velocity Channel (km/s)', labelpad=10.0, fontsize=12)
    plt.gcf().text(0.82, 0.75, "Velocities (km/s):", fontsize=11)
    plt.subplots_adjust(right=0.8)
    close_ax = plt.axes([0.85, 0.05, 0.1, 0.075])
    close_button = Button(close_ax, 'END')
    close_button.on_clicked(closer)
    print("\nClick on galaxy (average) velocity (c*z): ")
    # Have user click on locations, use pop up box (similar to what has been done earlier, same thing for fitting
    # region lower and upper bounds. Remind user to include wing structure if present

    plt.show()

    integrated_flux = profile * v  # in jy km / s, only between the channel ranges they selected
    # sum up integrated flux over the range of channels they have selected (lower to upper bound) ^--
    #    maybe relabelling axis would be easier than converting channels to...? -look into
    # print these units on side of figure- see Box demo for example
    return integrated_flux
