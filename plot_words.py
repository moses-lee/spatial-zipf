import matplotlib.pyplot as plt
import numpy as np

def _round(num, round_precision):
    if isinstance(num, int):
        return str(num)
    # multiply float to precision place
    num *=  10 ** round_precision
    return str(round(num) / (10 ** round_precision))



def plot_map(out_list, total_words, title, data_type, cutoff=0, round_precision=3):
    y_label = ''
    if data_type == 'freq':
        y_label = 'Number of Occurrences'
    elif data_type == 'loc':
        y_label = 'Average Distance Between Each Given Word'

    if cutoff == 0:
        cutoff = len(out_list)
    out_list = out_list[:cutoff]
    
    x_val = [x[0] for x in out_list]
    y_val = [x[1] for x in out_list]

    coef = np.polyfit(range(len(x_val)),y_val,1)
    poly1d_fn = np.poly1d(coef) 

    plt.figure(figsize=(9,6))
     # plt.bar(range(len(x_val)), y_val)
    plt.plot(range(len(x_val)), y_val, 'bo', range(len(x_val)), poly1d_fn(range(len(x_val))), '--k')
    plt.xlabel('Words (' + str(total_words) + ' total)', fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.xticks(range(len(x_val)), x_val, fontsize=10, rotation='vertical')

    for i, v in enumerate(y_val):
        plt.text(i, v, _round(v, round_precision), fontsize=8)
    
    plt.title(title)
    plt.tight_layout()
    # plt.savefig('results/' + title + '_' + data_type.upper() + '.png')
    plt.show()


