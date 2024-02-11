import numpy as np
import matplotlib.pyplot as plt

class CustomCLAHE:
    def __init__(self, clip_limit=2.0, grid_size=(8, 8)):
        self.clip_limit = clip_limit
        self.grid_size = grid_size
    
    def clip_histogram(self, hist):
        # Clip histogram bins exceeding the clip limit
        clipped_hist = np.minimum(hist, self.clip_limit)
        
        # Redistribute excess pixels evenly across bins
        excess = hist - self.clip_limit
        num_excess_bins = np.sum(excess > 0)
        if num_excess_bins > 0:
            excess_per_bin = np.sum(excess) / num_excess_bins
            clipped_hist += excess_per_bin
        
        return clipped_hist
    
    def create_clahe_lookup_table(self, grid):
        # Calculate histogram
        hist, _ = np.histogram(grid.flatten(), bins=256, range=[0, 256])
        
        # Clip histogram
        clipped_hist = self.clip_histogram(hist)
        
        # Calculate cumulative distribution function
        cdf = np.cumsum(clipped_hist) / np.sum(clipped_hist)
        
        # Calculate lookup table
        lookup_table = np.zeros(256)
        for i in range(256):
            lookup_table[i] = np.uint8(255 * cdf[i])
        
        return lookup_table
    
    def apply_clahe(self, image):
        # Calculate size of each grid
        grid_height = image.shape[0] // self.grid_size[0]
        grid_width = image.shape[1] // self.grid_size[1]
        
        # Initialize output image
        output_image = np.zeros_like(image)
        
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # Extract grid
                grid = image[i*grid_height:(i+1)*grid_height, j*grid_width:(j+1)*grid_width]
                
                # Create CLAHE lookup table for this grid
                lookup_table = self.create_clahe_lookup_table(grid)
                
                # Apply lookup table to grid
                output_image[i*grid_height:(i+1)*grid_height, j*grid_width:(j+1)*grid_width] = lookup_table[grid]
        
        return output_image

# Example usage
# Read grayscale image
image = plt.imread('img_1.png')

# Create CLAHE object
clahe = CustomCLAHE()

# Apply CLAHE
clahe_image = clahe.apply_clahe(image)

# Display original and CLAHE processed images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(clahe_image, cmap='gray')
plt.title('CLAHE Processed Image')

plt.show()
