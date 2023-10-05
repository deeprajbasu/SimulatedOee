import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import json
from PIL import Image

# Set the directory containing your data
image_dir = 'images'
metadata_dir = 'metadata'

# Get list of frames
frame_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])
metadata_files = sorted([f for f in os.listdir(metadata_dir) if f.endswith('.json')])

# Create a figure and axes
fig, ax = plt.subplots()

# Loop over frames
for frame_file, metadata_file in zip(frame_files, metadata_files):
    print(frame_file)
    # Ensure that the frame and metadata files match
    if frame_file.split('.')[0].split('_')[-1] != metadata_file.split('.')[0].split('_')[-1]:
        print(f"Skipping mismatched frame and metadata: {frame_file}, {metadata_file}")
        continue

    # Read image
    img = Image.open(os.path.join(image_dir, frame_file))
    ax.imshow(img)

    # Read metadata
    with open(os.path.join(metadata_dir, metadata_file), 'r') as file:
        metadata = json.load(file)

    # Draw bounding boxes and labels
    for obj in metadata['objects']:
        bbox = obj['bbox']
        label = obj['label']
        color = obj['color']
        is_error = obj['is_error']

        # Create a Rectangle patch
        rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor='w', facecolor='none')
        ax.add_patch(rect)

        # Add label and color information
        plt.text(bbox[0], bbox[1] - 10, f"{label} {color} {'Error' if is_error else ''}", color='white')

    # Pause for a while
    plt.pause(0.00000000000000000000000000000000001)

    # Clear the current axes
    plt.cla()

# Close the displayed window
plt.close()
