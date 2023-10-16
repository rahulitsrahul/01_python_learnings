import numpy as np
import cv2
from matplotlib import pyplot as plt

def region_growing(image, seed, threshold):
    height, width = image.shape
    segmented = np.zeros_like(image, dtype=np.uint8)
    visited = np.zeros_like(image, dtype=bool)
    stack = [seed]

    while stack:
        current_point = stack.pop()
        if not visited[current_point]:
            visited[current_point] = True

            if abs(image[current_point] - image[seed]) < threshold:
                segmented[current_point] = 255

                neighbors = get_neighbors(current_point, height, width)
                for neighbor in neighbors:
                    if not visited[neighbor]:
                        stack.append(neighbor)

    return segmented

def get_neighbors(point, height, width):
    x, y = point
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < height - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < width - 1:
        neighbors.append((x, y + 1))
    return neighbors

if __name__ == "__main__":
    # Load image
    image = cv2.imread("img_1.png", cv2.IMREAD_GRAYSCALE)
    plt.imshow(image, cmap='gray')
    
    # Define seed point and threshold
    seed = (210, 210)  # You can choose any seed point
    threshold = 10  # Adjust the threshold as needed

    # Perform region growing
    print('run_region_growing')
    segmented_image = region_growing(image, seed, threshold)

    # Display the original image and segmented result
    print("Display Segmented image")
    plt.imshow(segmented_image, cmap='gray')
