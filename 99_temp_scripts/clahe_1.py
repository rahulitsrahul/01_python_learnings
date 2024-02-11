import numpy as np
import cv2
from matplotlib import pyplot as plt

def calculate_clip_point(image, clip_limit=2.0):
    M = image.size
    N = 256  # Assuming 256 bins for simplicity
    alpha = clip_limit
    if M == 0:
        return 0
    else:
        S_max = np.max(image)
        clip_point = (N / M) * (1 + ((alpha / 100) * S_max))
        return clip_point

def calculate_histogram(image, bins=256):
    histogram = np.zeros(bins)
    for pixel_value in range(bins):
        histogram[pixel_value] = np.sum(image == pixel_value)
    return histogram

def calculate_cdf(pdf):
    cdf = np.cumsum(pdf)
    return cdf / cdf[-1]

def calculate_remap_function(cdf, lmax):
    return cdf * lmax

def bilinear_interpolation(Ta, Tb, Tc, Td, xa, xb, ya, yc, xp, yp):
    n = (xb - xp) / (xb - xa)
    m = (yc - yp) / (yc - ya)
    interpolated_value = m * (n * Ta + (1 - n) * Tb) + (1 - m) * (n * Tc + (1 - n) * Td)
    return interpolated_value

def apply_clahe(image, clip_limit=2.0, grid_size=(8, 8)):
    height, width = image.shape
    grid_height = max(height // grid_size[0], 1)  # Ensure grid size is at least 1
    grid_width = max(width // grid_size[1], 1)   # Ensure grid size is at least 1
    
    # Calculate clip point
    clip_point = calculate_clip_point(image, clip_limit)
    
    # Initialize CLAHE image
    clahe_image = np.zeros_like(image)
    
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            # Define grid boundaries
            y_start = i * grid_height
            y_end = min((i + 1) * grid_height, height)
            x_start = j * grid_width
            x_end = min((j + 1) * grid_width, width)
            
            # Check if grid size is zero for either dimension
            if y_end <= y_start or x_end <= x_start:
                continue
            
            # Extract grid from the image
            grid = image[y_start:y_end, x_start:x_end]
            
            # Calculate histogram for the grid
            histogram = calculate_histogram(grid)
            
            # Clip histogram
            excess = histogram - clip_point
            clipped_histogram = histogram - np.clip(excess, 0, None)
            total_excess = np.sum(excess[excess > 0])
            
            # Redistribute excess pixels uniformly
            n_pixels = grid.size
            avg_excess = total_excess / n_pixels
            excess_per_bin = excess / n_pixels
            redistributed_histogram = clipped_histogram + excess_per_bin
            
            # Calculate CDF
            cdf = calculate_cdf(redistributed_histogram)
            
            # Calculate remap function
            lmax = np.max(grid)
            T = calculate_remap_function(cdf, lmax)
            
            # Apply remap function to the grid
            clahe_image[y_start:y_end, x_start:x_end] = T[image[y_start:y_end, x_start:x_end]]
            
            # # Apply interpolation
            # # Apply remap function to the grid with bilinear interpolation
            # for y in range(y_start, y_end):
            #     for x in range(x_start, x_end):
            #         xa = x_start - grid_width
            #         xb = x_start
            #         ya = y_start - grid_height
            #         yc = y_start
            #         xp = x
            #         yp = y
            #         Ta = T[image[max(yp - 1, y_start), max(xp - 1, x_start)]]
            #         Tb = T[image[max(yp - 1, y_start), min(xp, x_end - 1)]]
            #         Tc = T[image[min(yp, y_end - 1), max(xp - 1, x_start)]]
            #         Td = T[image[min(yp, y_end - 1), min(xp, x_end - 1)]]
            #         clahe_image[yp, xp] = bilinear_interpolation(Ta, Tb, Tc, Td, xa, xb, ya, yc, xp, yp) 
    
    return clahe_image



# Example usage:
# Load grayscale image
image = cv2.imread('img_1.png', 0)

tile_size = (8, 8)
CL = 2.0

# Apply CLAHE algorithm
result_image = apply_clahe(image=image, clip_limit=CL, grid_size=tile_size)


# Apply OpenCV's CLAHE algorithm
clahe = cv2.createCLAHE(clipLimit=CL, tileGridSize=tile_size)
opencv_result_image = clahe.apply(image)


# Display original and resulting images
plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(result_image, cmap='gray')
plt.title('custom CLAHE')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(opencv_result_image, cmap='gray')
plt.title('openCV CLAHE')
plt.axis('off')

plt.show()


