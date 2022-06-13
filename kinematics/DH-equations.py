import numpy as np 

a1 = 1
a2 = 1
a3 = 1

d1 = 1
d2 = 1
d3 = 1 
#theta, alpha, r, d
#theta - angle 
#alpha - angle from Zn-1 to Zn around Xn
#r - distance between the origin of the n-1 frame and the origin of the n frame along Xn direction
#d - distance from Xn-1 to Xn along the Zn-1 direction
d_h_table = np.array([[np.deg2rad(90), np.deg2rad(90), 0, a1 + d1],
                      [np.deg2rad(90), np.deg2rad(-90), 0, a2 + d2],
                      [0, 0, 0, a3 + d3]]) 
 
 #homogenious transformation matrix
homgen_0_1 = np.array([[np.cos(d_h_table[0,0]), -np.sin(d_h_table[0,0]) * np.cos(d_h_table[0,1]), np.sin(d_h_table[0,0]) * np.sin(d_h_table[0,1]), d_h_table[0,2] * np.cos(d_h_table[0,0])],
                      [np.sin(d_h_table[0,0]), np.cos(d_h_table[0,0]) * np.cos(d_h_table[0,1]), -np.cos(d_h_table[0,0]) * np.sin(d_h_table[0,1]), d_h_table[0,2] * np.sin(d_h_table[0,0])],
                      [0, np.sin(d_h_table[0,1]), np.cos(d_h_table[0,1]), d_h_table[0,3]],
                      [0, 0, 0, 1]])  

print(homgen_0_1)