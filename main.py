import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer as mpl
import numpy as np
import os

# Get some pretty fonts to use:
URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
serif_regular = mpl.FontManager(URL1)
URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
serif_extra_light = mpl.FontManager(URL2)
URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
rubik_regular = mpl.FontManager(URL3)
URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = mpl.FontManager(URL4)
URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
robotto_bold = mpl.FontManager(URL5)

# Colormap used for the different players
cmap = plt.colormaps['tab20'].colors

with pd.ExcelFile("sample.xlsx") as xls:
    st.write(xls.sheet_names)
    for sheet in xls.sheet_names:
        st.write(sheet)
        data = pd.read_excel(xls, sheet, index_col=0)

        # Zero values need to be replaced with values > 0, otherwise the used
        # spider chart visualization breaks
        data = data.astype(float)
        data[data == 0] = 0.0001

        columns=data.columns
        st.write(data.index)

        # Scale the minimum and maximum values in the chart - please feel
        # free to experiment with different multipliers.
        mins=data.min(axis=0).values
        mins=np.multiply(mins, 0.9)
        maxs=data.max(axis=0).values
        maxs=np.multiply(maxs, 1.1)

        # creating the figure using the grid function from mplsoccer:
        fig, axs = mpl.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                        title_space=0, endnote_space=0, grid_key='radar', axis=False)

        radar = mpl.Radar(columns, mins, maxs,
                      # whether to round any of the labels to integers instead of decimal places
                      round_int=[False] * len(columns),
                      num_rings=8,  # the number of concentric circles (excluding center circle)
                      # if the ring_width is more than the center_circle_radius then
                      # the center circle radius will be wider than the width of the concentric circles
                      ring_width=1, center_circle_radius=1)
        radar.setup_axis(ax=axs['radar'])  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='whitesmoke', edgecolor='lightgray')  # draw circles

        # The whole ordinal and positions index is just a hack to position the player names correctly.
        # This will currently break if there are more than 4 players in the figure, the names will be
        # printed in upper left and right corners of the figure. Should be doable with calculating
        # the spacing between names, and using a modulo operator for printing the even values to the left
        # and odd values to the right
        # TODO: make this feasible for players > 4
        ordinal = 0
        for name, data in data.iterrows():
            st.write(name)
            st.write(data)
            rdr, vertices = radar.draw_radar_solid(data, ax=axs['radar'],
                                           #kwargs={'facecolor': colors[name],
                                                   kwargs={'facecolor': cmap[ordinal],
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})
            axs['radar'].scatter(vertices[:, 0], vertices[:, 1],
                       c='#aa65b2', edgecolors='#502a54', marker='o', s=50, zorder=2)
            pos_x = 0.01
            pos_y = ordinal * 0.25
            if (ordinal % 2) != 0:
                pos_x = 0.8
                pos_y = (ordinal - 1) * 0.25
        
            #st.write(f"position x: {pos_x}, position y: {pos_y}")
            title_text = axs['title'].text(pos_x, pos_y, name, fontsize=25, color=cmap[ordinal],
                                           fontproperties=robotto_bold.prop, ha='left', va='center')

            ordinal = ordinal + 1

        # Draw the range labes into the radar
        range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=14, fontproperties=robotto_thin.prop)
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=14, fontproperties=robotto_thin.prop)

        # Show the figure in streamlit
        st.pyplot(fig)

        # ..and finally save it to the main directory. Please feel free to use a directory if so desired.
        pathname = os.path.join("images", f"{sheet}.png")
        plt.savefig(pathname,bbox_inches='tight')


