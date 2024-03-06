import os
import pandas as pd
from scipy.signal import stft
import librosa
import numpy as np
import matplotlib.pyplot as plt
import random

def get_audio_file_list(df):
    # df_sorted = df.sort_values(by='noisy_SNR', ascending=True)
    # top_10_lowest_snr = df_sorted.head(10)
    # audio_names_with_lowest_snr = top_10_lowest_snr['audio_names']
    # name_list = audio_names_with_lowest_snr.tolist()

    # Create 10 quantile-based bins for the 'noisy_SNR' column
    df['snr_group'] = pd.qcut(df['noisy_PESQ'], q=10, labels=False, duplicates='drop')

    # Initialize an empty list to hold the audio names with the lowest PESQ in each group
    audio_names_lowest_pesq = []

    # Iterate over each group
    for group in sorted(df['snr_group'].unique()):
        # Filter the dataframe for the current group
        group_df = df[df['snr_group'] == group]
        
        # Find the row with the lowest PESQ value in the current group
        min_pesq_row = group_df.loc[group_df['noisy_SNR'].idxmin()]
        
        # Append the audio name of the row with the lowest PESQ to the list
        audio_names_lowest_pesq.append(min_pesq_row['audio_names'])
    
    # Iterate over each group
    for group in sorted(df['snr_group'].unique()):
        # Filter the dataframe for the current group
        group_df = df[df['snr_group'] == group]
        
        # Find the row with the lowest PESQ value in the current group
        min_pesq_row = group_df.loc[group_df['noisy_SNR'].idxmax()]
        
        # Append the audio name of the row with the lowest PESQ to the list
        audio_names_lowest_pesq.append(min_pesq_row['audio_names'])
    
    random.shuffle(audio_names_lowest_pesq)
    audio_names = _rank(audio_names_lowest_pesq[:10],df)
    print(audio_names)
    return audio_names['audio_names'].tolist()


def _rank(audio_names_list,df):
    filtered_df = df[df['audio_names'].isin(audio_names_list)]
    sorted_df = filtered_df.sort_values(by='noisy_SNR', ascending=True)
    sorted_audio_names_by_snr = sorted_df[['audio_names', 'noisy_SNR']]
    return sorted_audio_names_by_snr



def plot_spectrogram(file_path, sr=16000, window_length=1024, hop_size=16, nfft=1024):
    signal, fs = librosa.load(file_path, sr=sr)
    f, t, Zxx = stft(signal, fs=fs, window='hann', nperseg=window_length, noverlap=window_length - hop_size, nfft=nfft)
    plt.figure(figsize=(4,2))
    spec = np.abs(Zxx)**0.3
    spec = 10 * np.log10(np.abs(Zxx)+1e-8)

    plt.imshow(spec, aspect='auto', origin='lower', extent=[t.min(), t.max(), f.min(), f.max()])
    # plt.pcolormesh(np.linspace(0, t, t), f, np.abs(Zxx)**0.3, shading='gouraud')
    plt.axis('off')  # Turn off axes
    plt.savefig(file_path.replace('.wav','.svg'), bbox_inches='tight', pad_inches=0)
    plt.close()

# Define the base path to your project directory
base_path = "./DNS_audio"

# Define the models and hyperparameters
models = [ 'GRU', 'MPT', 'DPRNN']
hyperparameters = ['25', '50', '75', '100']

# Start of the HTML document
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech Enhancement Demo</title>
    <style>
    
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; /* Center-align all content */
        }
        h1 { 
            text-align: center; /* Center-align the title */
        } 
        .container {
            margin: 0 auto; /* Center-align the container */
            width: 100%; /* Set the width of the container */
            max-width: 1600px; /* Set a maximum width for larger screens */
            text-align: center; /* Reset text alignment within the container */
        }
        .file-section { 
            margin-top: 100px;
            margin-bottom: 40px; 
        }
        audio { 
            margin-top: 0px; 
            margin-bottom: 10px; 
            height: 10px; /* Adjust the height as needed */
        }
        table.center-table {
            margin-left: auto;
            margin-right: auto;
            margin-top: 10px; 
            margin-bottom: 40px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Speech Enhancement Demo</h1>
'''

# Generate HTML for each model and hyperparameter

noisy_metric_file = 'noisy_metric.xlsx'
df = pd.read_excel(noisy_metric_file)
name_list = get_audio_file_list(df)



# for i, file in enumerate(sorted(os.listdir(os.path.join(base_path, 'Noisy')))):  # Example to get file names
for i, file in enumerate(name_list):  # Example to get file names

    html_content += '<div class="file-section">'

    audio_row = df[df['audio_names'] == file]
    noisy_pesq = round(float(audio_row['noisy_PESQ'].values[0]),2)
    noisy_snr = int(audio_row['noisy_SNR'].values[0])
    
    html_content += f'<h2>Test File {i+1}, SNR: {noisy_snr}, PESQ: {noisy_pesq}</h2>'
    noisy_path = os.path.join(base_path, "Noisy", file)
    target_path = os.path.join(base_path, "Target", file)

    plot_spectrogram(noisy_path)
    plot_spectrogram(target_path)

    html_content += f'''<table class='center-table' border="0">
        <tr>
            <th>Noisy Input</th>
            <th style="width: 100px;"></th>
            <th>Clean Target</th>
        </tr>
        <tr>
            <td><img src={noisy_path.replace('.wav','.svg')}></img></td>
            <td style="width: 100px;"></td>
            <td><img src={target_path.replace('.wav','.svg')}></img></td>
        </tr>
        <tr>
            <td><audio controls src="{noisy_path}"></audio></td>
            <td style="width: 100px;"></td>
            <td><audio controls src="{target_path}"></audio></td>
        </tr>
        </table>'''
    

    html_content += f'''<table class="center-table" border="0">
        <tr>
            <th>Model</th>
            <th>25%</th>
            <th>50%</th>
            <th>70%</th>
            <th>100%</th>
        </tr>'''
    
    # html_content += f'''<table class='center-table' border="0">
    #     <tr>
    #         <th>Model</th>
    #         <th>hyperparameter 1</th>
    #         <th>hyperparameter 2</th>
    #         <th>hyperparameter 3</th>
    #         <th>hyperparameter 4</th>
    #     </tr>'''

    for i, model in enumerate(models):

        html_content += f'''<tr>'''

        html_content += f'''<th>{model}</th>'''

        for i_dx, param in enumerate(hyperparameters):        
            enhanced_path = os.path.join(base_path, model, param, file)
            plot_spectrogram(enhanced_path)
            
            html_content += f'''<td> <img src={enhanced_path.replace('.wav','.svg')}></img></td>'''
        
        html_content += f'''</tr>''' 
    

        html_content += f'''<tr>'''
        html_content += f'''<td> </td>'''
        for i_dx, param in enumerate(hyperparameters):        
            enhanced_path = os.path.join(base_path, model, param, file)
            html_content += f'''<td> <audio controls src="{enhanced_path}"></audio></td>'''        
        html_content += f'''</tr>''' 


        html_content += f'''<tr>'''
        html_content += f'''<td> </td>'''
        for i_dx, param in enumerate(hyperparameters):        
            html_content += f'''<td>  </td>'''
        html_content += f'''</tr>''' 
    
    html_content +=  '</table>'

    html_content += '</div>'
    
html_content += '</div>'
# End of the HTML document
html_content += '''
</body>
</html>
'''

# Write the HTML content to a file
with open("index.html", "w") as html_file:
    html_file.write(html_content)

print("HTML file generated successfully.")
