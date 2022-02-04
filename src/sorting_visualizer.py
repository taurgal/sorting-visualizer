# Script Name     : sorting_visualizer.py
# Author          : Howard Zhang
# Contributor     : Bosché Aurélien
# Created         : 14th June 2018
# Last Modified	  : 2th Feb 2022
# Version         : 1.3
# Modifications	  : 1.2 - Added the new option of modifying the number of items to be sorted.
# Modifications	  : 1.3 - Some refactoring and added translation capabilities usns gettext
# Description     : Processing user's input, Playing animations and generating animation files.

import random
import os
import sys
import re
from matplotlib import pyplot as plt
from matplotlib import animation
from sorting.data import Data
from sorting.selectionsort import selection_sort
from sorting.bubblesort import bubble_sort
from sorting.insertionsort import insertion_sort
from sorting.shellsort import shell_sort
from sorting.mergesort import merge_sort
from sorting.quicksort import quick_sort
from sorting.heapsort import heap_sort
from sorting.combsort import comb_sort
from sorting.monkeysort import monkey_sort
import os
import gettext

fr = gettext.translation(
    'base',
    localedir=os.path.join(
        os.path.dirname(__file__),'../locales/'),
    languages=['fr'])
fr.install()
_ = fr.gettext

sort_fun_dic = {
    "all": {
        "title": _('all'), "fake": True},
    insertion_sort: {
        "title": _('Insertion Sort')+r' ($O(n^2)$)'},
    shell_sort: {
        "title": _('Shell Sort')+r' ($O(n \cdot log_2(n)^2)$)'},
    selection_sort: {
        "title": _('Selection Sort')+r' ($O(n^2)$)'},
    merge_sort: {
        "title": _('Merge Sort')+r' ($O(n \cdot log_2(n))$)'},
    quick_sort: {
        "title": _('Quick Sort')+r' ($O(n \cdot log_2(n))$)'},
    heap_sort: {
        "title": _('Heap Sort')+r' ($O(n \cdot log_2(n))$)'},
    bubble_sort: {
        "title": _('Bubble Sort')+r' ($O(n^2)$)'},
    comb_sort: {
        "title": _('Comb Sort')+r' ($O(n \cdot log_2(n))$)'}
}

str_to_sort_fun_dic_key_dict = {
    key if type(key)==str else key.__name__:
    key for key in sort_fun_dic
}

def create_initial_data(dtype):
    data = []
    if dtype == 'random':
        data = list(range(1, Data.data_count + 1))
        random.shuffle(data)
    elif dtype == 'reversed':
        data = list(range(Data.data_count, 0, -1))
    elif dtype == 'few-unique':
        d = Data.data_count // 4
        for i in range(0, d):
            data.append(d)
        for i in range(d, d*2):
            data.append(d*2)
        for i in range(d*2, d*3):
            data.append(d*3)
        for i in range(d*3, Data.data_count):
            data.append(Data.data_count)
        random.shuffle(data)
    elif dtype == 'almost-sorted':
        data = list(range(1, Data.data_count + 1))
        a = random.randint(0, Data.data_count - 1)
        b = random.randint(0, Data.data_count - 1)
        while a == b:
            b = random.randint(0, Data.data_count - 1)
        data[a], data[b] = data[b], data[a]
    return data

def draw_chart(sort_fun, initial_data, frame_interval):
    # First set up the figure, the axis, and the plot elements we want to animate.
    fig = plt.figure(1, figsize=(16, 9))
    data_set = [Data(d) for d in initial_data]
    axs = fig.add_subplot(111)
    axs.set_xticks([])
    axs.set_yticks([])
    plt.subplots_adjust(left=0.01, bottom=0.02, right=0.99, top=0.95,
                        wspace=0.05, hspace=0.15)
    
    # Get the data of all frames.
    frames = sort_fun(data_set)
    # Output the frame count.
    frame_title = sort_fun_dic[sort_fun]["title"]

    # Animation function. This is called sequentially.
    # Note: fi is framenumber.
    def animate(fi):
        bars = []
        if(len(frames) > fi):
            axs.cla()
            axs.set_title(frame_title)
            axs.set_xticks([])
            axs.set_yticks([])
            bars += axs.bar(
                list(range(Data.data_count)),        # X
                [d.value for d in frames[fi]],       # data
                1,                                   # width
                color=[d.color for d in frames[fi]]  # color
            ).get_children()
        return bars

    # Call the animator.
    anim = animation.FuncAnimation(
        fig, animate, frames=len(frames), interval=frame_interval)
    return plt, anim


def draw_all_charts(initial_data, frame_interval):
    # Set up the figure+axis+plot elements to animate.
    axs = []
    frames_per_sort_fun = {}
    fig = plt.figure(1, figsize=(16, 9))
    data_set = [Data(d) for d in initial_data]
    for i in range(9):
        axs.append(fig.add_subplot(331 + i))
        axs[-1].set_xticks([])
        axs[-1].set_yticks([])
    plt.subplots_adjust(left=0.01, bottom=0.02, right=0.99, top=0.95,
                        wspace=0.05, hspace=0.15)

    # Get the data of all frames.
    for sort_fun in sort_fun_dic:
        if not sort_fun_dic[sort_fun].get("fake",False):
            frames_per_sort_fun[sort_fun]=sort_fun(data_set)

    # Output the frame counts of all chart.
    names = [sort_fun_dic[sort_fun]["title"]
             for sort in sort_fun_dic
             if not sort_fun_dic[sort_fun].get("fake",False)]
    max_frame_length = max(
        [len(frames) for _,frames
         in frames_per_sort_fun.items()])
    max_name_length=max([len(name) for name in names])
    max_frame_length =max([len(name) for name in names])
    frames = sort_fun(data_set)
    # Animation function. This is called sequentially.
    # Note: fi is framenumber.
    def animate(fi):
        bars = []
        for i in range(9):
            if(len(frames[i]) > fi):
                axs[i].cla()
                axs[i].set_title(titles[i])
                axs[i].set_xticks([])
                axs[i].set_yticks([])
                bars += axs[i].bar(list(range(Data.data_count)),           # X
                                   [d.value for d in frames[i][fi]],       # data
                                   1,                                      # width
                                   color=[d.color for d in frames[i][fi]]  # color
                                   ).get_children()
        return bars

    # Call the animator.
    anim = animation.FuncAnimation(fig, animate, frames=max(len(f) for f in frames), interval=frame_interval)
    return plt, anim

if __name__ == "__main__":
    try:
        Data.data_count = int(input('Please set the number of items to be sorted(32): '))
    except:
        Data.data_count = 32
    if len(sys.argv) > 1:
        # Type of sort algorithm.
        if len(sys.argv) > 2:
            stype_str = sys.argv[2]
            if stype_str in str_to_sort_fun_dic_key_dict:
                stype = str_to_sort_fun_dic_key_dict[stype_str]
                stype_dict = sort_fun_dic[stype]
            else:
                print(f'Error: Wrong argument at pos 1: {sys.argv[2]}')
                exit()
        stype_str = stype_dict["title"]

        # Type of original data.
        dtype = 'random'
        if len(sys.argv) > 3:
            dtype = sys.argv[3]
            if dtype not in ('random', 'reversed', 'few-unique', 'almost-sorted'):
                print('Error: Wrong argument at pos 2: {sys.argv[3]}')
                exit()
        od = create_initial_data(dtype)

        if sys.argv[1] == 'play':
            try:
                fi = int(input('Please set the frame interval(50): '))
            except:
                fi = 50
            plt, _ = draw_all_charts(od, fi) if stype == 'all' else draw_chart(stype, od, fi)
            plt.show()
        elif sys.argv[1] == 'save-mp4':
            default_fn = stype_str + '-' + dtype + '-animation'
            fn = input('Please input a filename(%s): ' % default_fn)
            if fn == '':
                fn = default_fn
            try:
                fps = int(input('Please set the fps(25): '))
            except:
                fps = 25
            _, anim = draw_all_charts(od, 100) if stype == -1 else draw_chart(stype, od, 100)
            print('Please wait...')
            anim.save(fn + '.mp4', writer=animation.FFMpegWriter(fps=fps, extra_args=['-vcodec', 'libx264']))
            print('The file has been successfully saved in %s' % os.path.abspath(fn + '.mp4'))
        elif sys.argv[1] == 'save-html':
            default_fn = stype_str + '-' + dtype + '-animation'
            fn = input('Please input a filename(%s): ' % default_fn)
            if fn == '':
                fn = default_fn
            try:
                fps = int(input('Please set the fps(25): '))
            except:
                fps = 25
            _, anim = draw_all_charts(od, 100) if stype == -1 else draw_chart(stype, od, 100)
            print('Please wait...')
            anim.save(fn + '.html', writer=animation.HTMLWriter(fps=fps))
            print('The file has been successfully saved in %s' % os.path.abspath(fn + '.html'))
