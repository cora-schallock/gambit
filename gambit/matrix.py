import numpy as np

#helper functions:
def create_centered_mesh_grid(h,k,shape):
    (rows,cols) = shape
    x=np.arange(0,cols)-h 
    y=np.arange(0,rows)-k
    
    xv, yv = np.meshgrid(x, y)
    return xv, yv

def create_angle_matrix(xv,yv,theta):
    return np.arctan2(yv,xv)-theta

def create_dist_matrix(xv,yv):
    return np.sqrt(xv**2 + yv**2)

def create_disk_angle_matrix(h,k,theta,shape):
    """create angle matrix"""
    #Step 1) Create a mesh and angle matrix:
    xv, yv = create_centered_mesh_grid(h,k,shape)
    angle_matrix = create_angle_matrix(xv,yv,theta)
    
    #Step 2) Create a matrix with angles [0,2*pi] from the POS semi-major axis
    return np.mod(angle_matrix,2*np.pi)

def create_major_axis_angle_matrix(h,k,theta,shape):
    """create major axis matrix"""
    #Step 1) Create a mesh and angle matrix (with additional offset of +pi/2):
    xv, yv = create_centered_mesh_grid(h,k,shape)
    angle_matrix = create_angle_matrix(xv,yv,theta)+np.pi/2
    
    #Step 2) Create a matrix with angles [-pi/2,pi/2] from the major axis:
    return np.abs(np.mod(angle_matrix,np.pi)-np.pi/2)

def create_minor_axis_angle_matrix(h,k,theta,shape):
    """createminor axis matrix"""
    #Step 1) Create a mesh and angle matrix:
    xv, yv = create_centered_mesh_grid(h,k,shape)
    angle_matrix = create_angle_matrix(xv,yv,theta)
    
    #Step 2) Create a matrix with angles [-pi/2,pi/2] from the minor axis:
    return np.abs(np.mod(angle_matrix,np.pi)-np.pi/2)
