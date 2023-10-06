import pygame
import sys
import random
import os
import json

# Create directories for images and metadata if they don't exist
if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('metadata'):
    os.makedirs('metadata')

frame_count = 0

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Shape Animation')

# Set up colors and shapes with alpha values
cream = (255, 253, 208)
gray = (169, 169, 169)
darker_gray = (159, 159, 159)
white = (100, 255, 100, 75)  # 80% opacity
red = (255, 0, 0, 75)  # 80% opacity
blue = (50, 50, 255)  # No alpha for bounding boxes
black = (50, 50, 255)  # No alpha for text

# Set up font
font = pygame.font.Font(None, 36)

# Lists to hold positions of shapes
shapes = []

# Set up the clock object
clock = pygame.time.Clock()

# Timer for shape generation
shape_timer = 0
shape_interval = 10

# Toggles for bounding box and text
show_bounding_box = False
show_text = False

classes ={ 'rect':1, 'circle':2, 'error_rect':3, 'error_circle':4}

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Press 'b' to toggle bounding boxes
                show_bounding_box = not show_bounding_box
            elif event.key == pygame.K_t:  # Press 't' to toggle text
                show_text = not show_text

    window.fill(cream)
    pygame.draw.rect(window, gray, (0, 100, width, height - 200))

    stripe_width = 10
    gap = 50
    for x in range(0, width, gap + stripe_width):
        pygame.draw.rect(window, darker_gray, (x, 100, stripe_width, height - 200))

    shape_timer += 1
    if shape_timer >= shape_interval:
        shape_timer = 0
        y_position = random.randint(100, height - 200)
        shape_type = random.choices(['rect', 'circle', 'error_rect', 'error_circle'], [0.34, 0.34, 0.05, 0.05], k=1)[0]
        shift = random.randint(-20, 20)
        color = (max(0, min(255, white[0]+shift)), max(0, min(255, white[1]+shift)), white[2], 204) if 'circle' in shape_type else (max(0, min(255, red[0]+shift)), red[1], red[2], 204)
        size = 75 if 'error' in shape_type else 50
        if random.random()<0.45:
            new_shape = (-75, y_position, shape_type, color, size)
            shapes.append(new_shape)

    shapes = [(x + 2, y, shape_type, color, size) for x, y, shape_type, color, size in shapes if x < width + 75]

    for x, y, shape_type, color, size in shapes:
        shape_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        if 'rect' in shape_type:
            pygame.draw.rect(shape_surface, color, (0, 0, size, size))
            if show_bounding_box:
                pygame.draw.rect(shape_surface, blue, (0, 0, size, size), 2)
        else:
            pygame.draw.ellipse(shape_surface, color, (0, 0, size, size))
            if show_bounding_box:
                pygame.draw.ellipse(shape_surface, blue, (0, 0, size, size), 2)
        if show_text:
            text = font.render(shape_type, True, black)
            window.blit(text, (x - 20, y - 30))


        window.blit(shape_surface, (x, y))
    if frame_count>120:
        pygame.image.save(window, f'images/frame_{frame_count:04d}.png')
        
        frame_metadata = {
            'objects': [
                {
                    'bbox': [x, y, size, size],
                    'label': f"{shape_type}",
                    'color': color,
                    'is_error': 'error' in shape_type
                    
                }
                for x, y, shape_type, color, size in shapes
            ]
        }
        num_shapes_on_screen = len(shapes)
        frame_metadata['num_shapes_on_screen'] = num_shapes_on_screen
        with open(f'metadata/frame_{frame_count:04d}.json', 'w') as metadata_file:
            json.dump(frame_metadata, metadata_file)

    frame_count += 1
    pygame.display.update()
    clock.tick(1000)
