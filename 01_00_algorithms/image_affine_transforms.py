import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_rotation_mat(angle):
    cos_th = np.cos(np.deg2rad(angle))
    sin_th = np.sin(np.deg2rad(angle))
    
    rotation_mat = np.array([
                                [cos_th, -sin_th],
                                [sin_th,  cos_th]
    ])
    return rotation_mat


def rotate_image(img, angle):
    rotated_img  = np.zeros_like(img)
    row, col = img.shape
    
    rotation_mat = get_rotation_mat(angle)
    for i in range(row):
        for j in range(col):
            px = i - row/2
            py = j - col/2
            
            
            pxy = np.array([[px, py]]).T
            pxy_rotated = np.matmul(rotation_mat, pxy)
            
            pxy_tr = pxy_rotated.ravel() + np.array([row/2, col/2])
            pxy_tr = np.round(pxy_tr).astype(int)
            
            if ((pxy_tr[0]>=0) & (pxy_tr[0] < row) & (pxy_tr[1] >= 0) & (pxy_tr[1] < col)):
                rotated_img[pxy_tr[0], pxy_tr[1]] = img[i, j]
    return rotated_img
    
    

if __name__ == "__main__":
    img = cv2.imread('img_1.jpg', 0)
    angle = -5
    
    rotated_image = rotate_image(img=img, angle=angle)
    plt.imshow(rotated_image, cmap='gray')
