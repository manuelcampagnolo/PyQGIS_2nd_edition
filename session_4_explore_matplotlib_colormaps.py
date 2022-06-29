# session_4_colormaps_from_matplotlib

import matplotlib # main python library for plots
import numpy as np # numpy, for arrays, etc


###########  from https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html
# define some array and a function "plot_color_gradients"
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
def plot_color_gradients(category, cmap_list):
    import matplotlib.pyplot as plt
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    axs[0].set_title(f'{category} colormaps', fontsize=18)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=16,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()
###########################################################

plot_color_gradients('Perceptually Uniform Sequential',
                     ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])
plt.show()

plot_color_gradients('Sequential',
                     ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'])
plt.show()

plot_color_gradients('Diverging',
                     ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'])
plt.show()

plot_color_gradients('Cyclic', ['twilight', 'twilight_shifted', 'hsv'])
plt.show()

plot_color_gradients('Qualitative',
                     ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c'])
plt.show()

plt.close('all')

##Access every single color and convert it to a QColor object
# See https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html
# The second argument gives the size of the list of colors 
viridis=matplotlib.cm.get_cmap('viridis',8) # ListedColormap
# get list of color RGBA 0-1 arrays
print('viridis.colors', viridis.colors) # numpy.ndarray
RdYlGn=matplotlib.cm.get_cmap('RdYlGn',8) # LinearSegmentedColormap
print('RdYlGn.colors', RdYlGn(range(8))) # no colors attribute; still a numpy.ndarray

# convert one of the colors from the colormap into a QColor object
mycolors=viridis.colors*255 # to be between 0 and 255
mycolor=mycolors[0] # 1st color in mycolors
QColor(mycolor[0],mycolor[1],mycolor[2],alpha=mycolor[3])