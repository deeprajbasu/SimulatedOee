import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import json
from PIL import Image

# Set the directory containing your data
image_dir = 'images'
prediction_dir = 'predictions'  # Set this to your actual predictions directory

# Get list of frames and predictions
frame_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])
prediction_files = sorted([f for f in os.listdir(prediction_dir) if f.endswith('.json')])

# Create a figure and axes
fig, ax = plt.subplots()

# Loop over frames
i = 0
for frame_file, prediction_file in zip(frame_files, prediction_files):
    # Skipping some frames for visualization purposes
    if i % 2 == 0 or i % 5 == 0 or i % 3 == 0:
        i += 1
        continue
    i += 1
    print(frame_file)

    # Ensure that the frame and prediction files match

    if frame_file.split('.')[0].split('_')[-1] != prediction_file.split('.')[0].split('_')[-2]:
        print(f"Skipping mismatched frame and prediction: {frame_file}, {prediction_file}")
        continue

    # Read image
    img = Image.open(os.path.join(image_dir, frame_file))
    ax.imshow(img)

    # Read prediction
    with open(os.path.join(prediction_dir, prediction_file), 'r') as file:
        prediction = json.load(file)

    # Draw bounding boxes and labels
    for box, label in zip(prediction['boxes'], prediction['labels']):
        # Convert bbox from [x, y, xmax, ymax] to [x, y, width, height]
        width = box[2] - box[0]  # width = xmax - xmin
        height = box[3] - box[1]  # height = ymax - ymin

        # Create a Rectangle patch
        rect = patches.Rectangle((box[0], box[1]), width, height, linewidth=5, edgecolor='y', facecolor='none')
        ax.add_patch(rect)

        # Add label
        plt.text(box[0], box[1] - 10, f"{label}", color='white')

    # Pause for a while
    plt.pause(0.1)

    # Clear the current axes
    plt.cla()

# Close the displayed window
plt.close()
