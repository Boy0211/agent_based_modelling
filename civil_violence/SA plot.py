import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_plot_archive():
    file_paths = [
        # './archives/saved_data1611648500.npy'
        # ,'./archives/saved_data1611655989.npy'
        # ,'./archives/saved_data1611660010.npy'
        './archives/saved_data1611673329.npy'

    ]

    for path in file_paths:
        with open(path, 'rb+') as f:
            data = np.load(f, allow_pickle = True)[()]
            print(data.keys(), '\n')
            thresh_data = data['active_threshold_t']
            print(thresh_data)
            

            # data_stored_next = np.load(f, allow_pickle=True)
            # et_caetera = np.load(f)

    # print(thresh_data)

    
    # dataset = pd.DataFrame({'Column1': data[:, 0], 'Column2': data[:, 1]})

    for param in ('ACTIVE', 'JAILED'):
        plot_all_vars(dataset, param)
        plt.show()

def plot_param_var_conf(ax, df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)


def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(3, figsize=(7, 10))

    for i, var in enumerate(problem['names']):
        plot_param_var_conf(axs[i], df[var], var, param, i)


load_plot_archive()