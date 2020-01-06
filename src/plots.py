import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
plt.style.use('ggplot')


def plot_hist(df, col_name, view_by):
    fig, ax = plt.subplots()

    true_vals = df[df[view_by]=='True'][col_name]
    false_vals = df[df[view_by]=='False'][col_name]

    ax.hist(true_vals, color='blue', label='True')
    ax.hist(false_vals, color='red', label='False')

    ax.set_title(f'{col_name} for {view_by}')
    ax.legend()


if __name__ == '__main__':

