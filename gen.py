import os

# Define the base path to your project directory
base_path = "./DNS_audio"

# Define the models and hyperparameters
models = [ 'GRU', 'MPT', 'DPRNN']
hyperparameters = ['25%', '50%', '75%', '100%']

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

    if i> 1:
        break
    html_content += f'<div class="file-section"><h2>File {i}</h2>'
    noisy_path = os.path.join(base_path, "Noisy", file)
    target_path = os.path.join(base_path, "Target", file)

    html_content += f'''
        <p>Noisy Audio:</p><audio controls src="{noisy_path}"></audio><p>Target Audio:</p><audio controls src="{target_path}"></audio>
    '''



    for model in models:
        html_content += f'<div class="model-section"><h2>{model} Model   </h2>'
        
        for param in hyperparameters:
            # html_content += f'<div class="update ratio-section"><h3>{param}</h3>'
        
            enhanced_path = os.path.join(base_path, model, param, file)
            if os.path.isfile(enhanced_path):
                print(1)
            
            # Add HTML for the audio player for noisy, enhanced, and target
            html_content += f'<p>{param}:</p><audio controls src="{enhanced_path}"></audio>'
            
            # html_content += '</div>'  # Close hyperparameter section
        
        html_content += '</div>'  # Close model section

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
