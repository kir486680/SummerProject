import numpy as np 
import math 


class RobotArm2D:

    def __init__(self, **kwargs):
        self.xRoot = kwargs.get('xRoot', 0)
        self.yRoot = kwargs.get('yRoot', 0)
        self.thetas = np.array([[]], dtype=np.float)
        self.joints = np.array([[self.xRoot, self.yRoot, 0, 1]], dtype=float).T
        self.lengths = []

    def add_revolute_link(self, **kwargs):
        self.joints = np.append(self.joints, np.array([[0,0,0,1]]).T, axis=1)
        self.lengths.append(kwargs['length'])
        self.thetas = np.append(self.thetas, kwargs.get('thataInit', 0))
    def get_transformation_matrix(self, theta, x, y):
        transformationMatrix = np.array([
            [math.cos(theta), -math.sin(theta), 0, x],
            [math.sin(theta), math.cos(theta), 0, y],
            [0,0,1,0],
            [0,0,0,1]
        ])
        return transformationMatrix
    def update_joint_coords(self):
        T = self.get_transformation_matrix(self.thetas[0].item(), self.xRoot, self.yRoot)
        for i in range(len(self.lengths) -1):
            T_next =  self.get_transformation_matrix(self.thetas[i+1], self.lengths[i], 0)
            T = T.dot(T_next)
            self.joints[:,[i+1]] = T.dot(np.array([[0,0,0,1]]).T)
        endEffectorCoords = np.array([[self.lengths[-1],0,0,1]]).T
        self.joints[:,[-1]] = T.dot(endEffectorCoords)


    def get_jacobian(self):

        kUnitVec = np.array([[0,0,1]], dtype=np.float)
        jacobian = np.zeros((3, len(self.jonts[0,:]) -1), dtype=np.float)
        endEffectorCoords = self.joints[:3,[-1]]

        for i in range(len(self.joints[0,:])-1):
            currentJointCoords = self.joints[:3, [i]]
            jacobian[:,i] = np.cross(
                kUnitVec, (endEffectorCoords - currentJointCoords).reshape(3,))
        return jacobian

    def update_theta(self, deltaTheta):
        self.thetas += deltaTheta.flatten()