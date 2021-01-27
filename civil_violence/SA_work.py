import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
README:
To run this script, please follow the following steps:
    1. Adjust the following constants such that they correspond to those in the SA.py file. 
    2. Run the SA.py script. 
    3. Add the paths to the output files from the SA.py to the file_paths list (line36).
    4. Run the SA_work.py script. 
'''


THRESHOLD   = 150
ITERATIONS  =  10
STEPS       =  20
N_PARAMS    =   6
N_OUTPUT    =   6

PARAMS = ['active_threshold_t', 'initial_legitimacy_l0',
              'max_jail_term', 'p', 'agent_vision', 'cop_vision']
BOUNDS = [[0.01, 1], [0.01, 1], [1, 100], [0.01, 0.4], [1, 20], [1, 20]]
OUTPUT_PARAMS = ['PARAM_VAL', 'MEAN_N', 'MEAN_PEAK_HEIGHT', 'MEAN_PEAK_WIDTH', 
                'MAX_PEAK_HEIGHT', 'MAX_PEAK_WIDTH']

### TEST SETTINGS ###
ITERATIONS = 2
STEPS = 2
PARAMS = ['active_threshold_t', 'initial_legitimacy_l0','max_jail_term']
BOUNDS = [[0, 1], [0, 1], [0, 100]]

#####################


file_paths = [
        './archives/saved_data1611693859',
        './archives/saved_data1611747993_run'
    ]

def load_datacollector():
    """
    Loads in the data from the specified paths into different dictionaries.
    """
    data_dict = {}

    for path in file_paths:
        with open(path, 'rb+') as f:

            data = np.load(f, allow_pickle = True)[()]
            keys = data.keys()
            data_dict[path] = data
    
    return data_dict

def map_keys():
    """
    Maps the used parameter bounds to key values for the data dictionary.
    """
    keys_dict = {}
    iter_list = np.arange(ITERATIONS*STEPS).reshape((STEPS, ITERATIONS))
    for i in range(len(PARAMS)):
        param_list = []
        param_range = np.linspace(BOUNDS[i][0], BOUNDS[i][1], STEPS).reshape(STEPS, 1)
        param_matrix = np.repeat(param_range, ITERATIONS, axis=1)
        for j in range(STEPS):
            param_list.extend(list(zip(param_matrix[j], iter_list[j])))
        keys_dict[PARAMS[i]] = param_list

    return keys_dict

def get_param_means(data, parameter):
    """
    For a provided parameter, calculates the determined output values for every parameter/iteration
    configuration.

    Returns a dataframe with the output type as column names. Every row contains the mean values of 
    the set amount of iterations for every parameter configuration.
    """
    # Initialize outputs
    output = np.zeros((STEPS, N_OUTPUT))
    peak_heights = []
    peak_widths = []
    keys = keys_dict[parameter]
    # print('KEYS: ', keys)

    # Divide the key list in the different step sizes of the parameter.
    for i in range(STEPS):
        s_keys = keys[i*ITERATIONS : (i+1)*ITERATIONS]
        # Every key is an iteration
        for key in s_keys:
            actives = data[parameter][key]['ACTIVE']
            ph, pw = get_outbreaks(actives, THRESHOLD)
            peak_heights.extend(ph)
            peak_widths.extend(pw)
        # Output calculation
        mean_n_peaks = len(peak_heights)/ITERATIONS
        mean_peak_height = np.mean(np.array(peak_heights))
        mean_peak_width = np.mean(peak_widths)
        max_peak_height = np.max(peak_heights)
        max_peak_width = np.max(peak_widths)

        output[i] = [key[0], mean_n_peaks, mean_peak_height, mean_peak_width, max_peak_height, max_peak_width]
        # print(parameter)
        # print('MEAN_N | MEAN_PEAK_HEIGHT | MEAN_PEAK_WIDTH | MAX_PEAK_HEIGHT | MAX_PEAK_WIDTH ')
        # print(mean_n_peaks, mean_peak_height, mean_peak_width, max_peak_height, max_peak_width)
    # print(data[parameter][(0.0, 0)]['ACTIVE'])
    # print(output)

    df = pd.DataFrame({'PARAM_VAL': output[:, 0], 'MEAN_N': output[:, 1], 
        'MEAN_PEAK_HEIGHT': output[:, 2], 'MEAN_OUTBREAK_DURATION': output[:, 3], 
        'MAX_PEAK_HEIGHT': output[:, 4], 'MAX_OUTBREAK_DURATION': output[:, 5]})
    
    return df # Can also return 'output' if the data is wanted in array form.

def get_outbreaks(data, threshold):
    """
    Calculates the outbreaks from the actives data.

    Returns:
        - An array with the outbreak peak sizes.
        - An array with the outbreak durations.
    """
    outbreak_peaks = []
    outbreak_widths = []
    counting = False
    current_peak = 0

    for i in range(len(data)):

        if data[i] >= threshold and not counting:
            counting = True
            if current_peak < data[i]:
                current_peak = data[i]
            start = i

        elif data[i] >= threshold and counting:
            if current_peak < data[i]:
                current_peak = data[i]

        elif data[i] < threshold and counting:
            outbreak_peaks.append(current_peak)
            outbreak_widths.append(i-start)
            current_peak = 0
            counting = False

    return outbreak_peaks, outbreak_widths

def save_csv(name, df):
    """
    Save an output dataframe as a CSV file in the archives folder.
    """
    path = 'archives/'+name+'_out.csv'
    df.to_csv(path)


# Run the script
model_data = load_datacollector()
run_data = model_data['./archives/saved_data1611747993_run']
keys_dict = map_keys()
output_data = {}

for param in run_data.keys():
    output_data[param] = get_param_means(run_data, param)


for df in output_data:
    print('Tested parameter: ', df) # Output feedback
    print(output_data[df])          # Output feedback
    save_csv(str(df), output_data[df])