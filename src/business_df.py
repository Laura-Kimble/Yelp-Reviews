import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

class BusinessDF(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)


    # def plot_hist(self, col_name, view_by_col=''):
    #     ''' Plot histrograms of the given col_name, one for each value of the view_by_col
    #     '''
    #     if view_by:
    #         num_plots = self[view_by].get_counts


    #     else num_plots = 1

    #     fig, ax = plt.subplots(num_plots, 1, figsize=(4, 10))

    #     true_vals = df[df[view_by]=='True'][col_name]
    #     false_vals = df[df[view_by]=='False'][col_name]

    #     ax.hist(true_vals, color='blue', label='True')
    #     ax.hist(false_vals, color='red', label='False')

    #     ax.set_title(f'{col_name} for {view_by}')
    #     ax.legend()


if __name__ == '__main__':
    businesses = BusinessDF(businesses)