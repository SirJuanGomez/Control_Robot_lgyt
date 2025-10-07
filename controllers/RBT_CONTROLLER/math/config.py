import math 
import numpy as np


class MATH:
    @staticmethod
    def normalize_angle(angle):
        """Normalize an angle to the range [-pi, pi]."""
        return (angle + math.pi) % (2 * math.pi) - math.pi

    @staticmethod
    def matrix_kinematic(a,theta,alpha):
        mh=np.array([        
            [np.cos(theta),-np.sin(theta)*np.cos(alpha),np.sin(theta)*np.sin(alpha),a*np.cos(theta)],
            [np.sin(theta),np.cos(theta)*np.cos(alpha),-np.cos(theta)*np.sin(alpha),a*np.sin(theta)],
            [0,np.sin(alpha),np.cos(alpha),0],
            [0,0,0,1]])
        return mh
    
    