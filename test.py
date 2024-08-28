from PIL import Image
import numpy as np

def make_most_frequent_color_transparent(image_path):
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure image is in RGBA format

    # Convert image to numpy array
    data = np.array(img)

    # Flatten the array and compute the most frequent color
    colors, counts = np.unique(data.reshape(-1, 4), axis=0, return_counts=True)
    most_frequent_color = colors[np.argmax(counts)]

    # Set the alpha channel of the most frequent color to 0 (transparent)
    data[(data[:, :, 0] == most_frequent_color[0]) &
         (data[:, :, 1] == most_frequent_color[1]) &
         (data[:, :, 2] == most_frequent_color[2])] = [most_frequent_color[0], most_frequent_color[1], most_frequent_color[2], 0]

    # Convert array back to image
    new_img = Image.fromarray(data, mode="RGBA")
    # Save or display the image
    new_img.save('Fig_output.png')  # Save the output image with transparency

# Example usage
make_most_frequent_color_transparent('Fig.png')
