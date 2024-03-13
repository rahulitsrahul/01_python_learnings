mat = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]


def print_mat(mat):
    for i in range(len(mat)):
        print(mat[i])



print(f"Orignal Matrix:\n {print_mat(mat)}")

l, r = 0, len(mat[0])-1
top, bottom = 0, len(mat)-1

while ((l<r) & (top < bottom)):
    for i in range(r):
        top_l_temp = mat[top][l+i]
        mat[top][l+i] = mat[bottom-i][l]
        mat[bottom-i][l] = mat[bottom][r-i]
        mat[bottom][r-i] = mat[top+i][r]
        mat[top+i][r] = top_l_temp
    l += 1
    r -= 1
    top += 1
    bottom -= 1
    
print(f"Rotated Matrix: \n {print_mat(mat)}")