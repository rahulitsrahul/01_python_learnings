import numpy as np
from matplotlib import pyplot as plt
import time
import cv2


def get_neighborhood_points(point):
    # 4 connected
    x, y = point
    points = [
        [x-1, y],
        [x+1, y],
        [x, y+1],
        [x, y-1],
        # 8 connected
        [x+1, y+1],
        [x+1, y-1],
        [x-1, y-1],
        [x-1, y+1],
     ]
    return points

if __name__ == "__main__":
    # img = np.zeros([100, 100])
    # img[20:50, 10:40] = 1
    
    img = cv2.imread(r'D:/02_my_learnings/01_python_repo/01_python_learnings/29_int_preps/img_1.png', 0)
    img = img/255
       
    plt.imshow(img, cmap='gray')
    plt.title("Input image")
    plt.show()
    
    seed_point = [60, 120]
    t1 = time.time()
    # Initialize
    points_bag = []
    visited_bag = []
    seg_img = np.zeros_like(img)
    cur_point = seed_point
    points_bag.append(cur_point)
    
    # Iterate over the loop
    while len(points_bag) > 0:
        cur_point = points_bag.pop(0)
        visited_bag.append(cur_point)
        if img[cur_point[0], cur_point[1]] == 0:
            seg_img[cur_point[0], cur_point[1]] = 1
            neighbors = get_neighborhood_points(cur_point)
            
            # for neighbor in neighbors:
            #     if neighbor not in visited_bag and neighbor not in points_bag:
            #         points_bag.append(neighbor)
                
            neighbor_pts_unvsited = [pt for pt in neighbors if ((not pt in visited_bag) and (not pt in points_bag))]
            points_bag += neighbor_pts_unvsited
    
    t2 = time.time()
    print(f"Time_elapsed: {t2 - t1}")
    
    plt.imshow(seg_img, cmap='gray')
    plt.title(f"reg_grow_img, seed: {seed_point}")
    plt.show()
    
    
    