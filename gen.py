import os

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
        body { font-family: Arial, sans-serif; }
        .model-section { margin-bottom: 40px; }
        .hyperparameter-section { margin-bottom: 20px; }
        audio { margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Speech Enhancement Demo</h1>
'''

# Generate HTML for each model and hyperparameter


for i, file in enumerate(sorted(os.listdir(os.path.join(base_path, 'Noisy')))):  # Example to get file names

    if i>= 10:
        break
    html_content += f'<div class="file-section"><h2>File {i+1}</h2>'
    noisy_path = os.path.join(base_path, "Noisy", file)
    target_path = os.path.join(base_path, "Target", file)

    html_content += f'''
        <p>Noisy Audio:<audio controls src="{noisy_path}"></audio>      Target Audio: <audio controls src="{target_path}"></audio> </p>
    '''

    # html_content += f'''<table class="center-table" border="0">
    #     <tr>
    #         <th>Model</th>
    #         <th>25%</th>
    #         <th>50%</th>
    #         <th>70%</th>
    #         <th>100%</th>
    #     </tr>'''
    
    html_content += f'''<table class="center-table" border="0">
        <tr>
            <th>Model</th>
            <th>hyperparameter 1</th>
            <th>hyperparameter 2</th>
            <th>hyperparameter 3</th>
            <th>hyperparameter 4</th>
        </tr>'''

    for i, model in enumerate(models):
        # html_content += f'<div class="model-section"><h2>{model} Model   </h2>'
        html_content += f'''<tr>'''
        html_content += f'''<td>model_{i+1}</td>'''

        for i, param in enumerate(hyperparameters):
            # html_content += f'<div class="update ratio-section"><h3>{param}</h3>'
        
            enhanced_path = os.path.join(base_path, model, param, file)
            
            # Add HTML for the audio player for noisy, enhanced, and target
            # html_content += f' <audio controls src="{enhanced_path}"></audio>'
            html_content += f'''<td> <audio controls src="{enhanced_path}"></audio></td>'''
            # html_content += '</div>'  # Close hyperparameter section
        
        # html_content += '</div>'  # Close model section
        html_content += f'''</tr>''' 
    
    html_content +=  '</table>'
    
    html_content += '</div>'  # Close file section

# End of the HTML document
html_content += '''
</body>
</html>
'''

# Write the HTML content to a file
with open("index.html", "w") as html_file:
    html_file.write(html_content)

print("HTML file generated successfully.")
