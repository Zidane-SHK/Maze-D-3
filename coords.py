from PIL import Image
import matplotlib.pyplot as plt # pip install

image_path = r'/Users/zidanekhan/PirateMaze/Game/Assets/maze.png'

def pick_coordinates(image_path):
    """Interactive coordinate picker"""
    img = Image.open(image_path)
    
    # Resize to target dimensions
    img = img.resize((920, 1128))
    
    coords = {}
    
    def onclick(event):
        if event.xdata and event.ydata:
            node_id = input(f"Node ID for ({int(event.xdata)}, {int(event.ydata)}): ")
            coords[node_id] = (int(event.xdata), int(event.ydata))
            print(f"Saved: '{node_id}': ({int(event.xdata)}, {int(event.ydata)})")
    
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(img)
    ax.set_title("Click on each node (close window when done)")
    
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    
    return coords

# Usage
coordinates = pick_coordinates('/Users/zidanekhan/PirateMaze/Game/main.py')

# Print in config.py format
print("\nCOORDS = {coords}")
for node, (x, y) in sorted(coordinates.items()):
    print(f"    '{node}': ({x}, {y}),")
print("}")