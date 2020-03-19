import matplotlib.pyplot as plt
import time
import numpy as np
import os.path
from os import path


def _round(num, round_precision):
    if isinstance(num, int):
        return str(num)
    # multiply float to precision place
    num *= 10 ** round_precision
    return str(round(num) / (10 ** round_precision))


def get_linear_cutoff(slope_list):
    for index, element in enumerate(slope_list):
        if element[1] >= 0.01:
            return index


def plot_map(out_list, total_words, title, data_type, save_plot, cutoff=-1, round_precision=3):
    
    y_label = ""
    linear_cutoff = 0
    if data_type == "freq":
        y_label = "Number of Occurrences"
    elif data_type == "avg_dist":
        y_label = "Average Distance Between Each Given Word"
    elif data_type == "sloped_avg":
        # get the linear cutoff
        linear_cutoff = get_linear_cutoff(out_list)
        y_label = "Slopes of the Average Distances Between Each Word"

    # calculate cut off
    if cutoff != -1:
        co = int((cutoff / 100) * len(out_list)) - 1
        out_list = out_list[:co]
    
    # separates x and y values
    x_val = [x[0] for x in out_list]
    y_val = [x[1] for x in out_list]

    # linear regression
    coef = np.polyfit(range(len(x_val)),y_val,1)
    poly1d_fn = np.poly1d(coef) 

    # print fit line
    print(data_type + "linear regression slope: " + str(poly1d_fn) + '\n')

    plt.figure(figsize=(9,6))
    # plt.bar(range(len(x_val)), y_val)
    # linear regression graph
    plt.plot(range(len(x_val)), y_val, 'bo', range(len(x_val)), poly1d_fn(range(len(x_val))), '--k')
   

    # plt.plot(range(len(x_val)), y_val)
    plt.xlabel('Words (' + str(total_words) + ' total)', fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.xticks(range(len(x_val)), x_val, fontsize=10, rotation='vertical')

    for i, v in enumerate(y_val):
        plt.text(i, v, _round(v, round_precision), fontsize=8)
    
    plt.title(title)
    # where graph becomes no longer linear
    if data_type == "sloped_avg":
        plt.axvline(x=linear_cutoff, color='r', linestyle='-')
    plt.tight_layout()

    if save_plot:
        millis = int(round(time.time() * 1000))
        new_title = title + '_' + data_type.upper() + '_' + str(millis)
        dir = 'results/' + new_title + '.png'
        plt.savefig(dir)
        
    plt.show()


