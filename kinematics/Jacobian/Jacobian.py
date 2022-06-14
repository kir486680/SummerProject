import numpy as np 
import math 
import matplotlib.pyplot as plt 
from RobotArm import *


Arm = RobotArm2D()

Arm.add_revolute_link(length=3, thetaInit=math.radians(10))
Arm.add_revolute_link(length=3, thetaInit=math.radians(15))
Arm.add_revolute_link(length=3, thetaInit=math.radians(20))
Arm.update_joint_coords()

# Initialize target coordinates to current end effector position.
target = Arm.joints[:,[-1]]

fig, ax = plt.subplots(figsize=(5,5))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
targetPt, = ax.plot([], [], marker='o', c='r')
endEff, = ax.plot([], [], marker='o', markerfacecolor='w', c='g', lw=2)
armLine, = ax.plot([], [], marker='o', c='g', lw=2)