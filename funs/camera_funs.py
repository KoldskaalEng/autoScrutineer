import numpy as np
import numpy.matlib

# ------------------------- 
# Defining camera angles - put all of this vtk bullshit into a seperate file. 
def cameraBelow():
    camPos = np.array([
        [0, 0, -1]
    ])
    camViewUp = np.array([
        [0, 1, 0]
    ])
    camParProj = True
    return camPos, camViewUp, camParProj

def cameraSides():
    camPos = np.array([
        [0, 1, 0],
        [0, -1, 0]
    ])
    camViewUp = np.array([
        [0, 0, 1],
        [0, 0, 1]
    ])
    camParProj = True
    return camPos, camViewUp, camParProj

def cameraLHS():
    camPos = np.array([
        [0, -1, 0]
    ])
    camViewUp = np.array([
        [0, 0, 1]
    ])
    camParProj = True
    return camPos, camViewUp, camParProj

def cameraAbove():
    camPos = np.array([
        [0, 0, 1]
    ])
    camViewUp = np.array([
        [0, 1, 0]
    ])
    camParProj = True
    return camPos, camViewUp, camParProj

def cameraFront():
    camPos = np.array([
        [-1, 0, 0]
    ])
    camViewUp = np.array([
        [0, 0, 1]
    ])
    camParProj = True
    return camPos, camViewUp, camParProj

def cameraAllAngles():
    camPos = np.array([ 
        [-1, 0, -1], # Camera position: in front, on centerline, from below
        [-1, 1, -1], # in front, from right, from below
        [0, 1, -1], # from middle of car, right, below
        [1, 1, -1], # behind, from right, below. 
        [1, 0, -1], # behind, centerline, below...
        [1, -1, -1],
        [0, -1, -1],
        [-1, -1, -1],
        [-1, 0, 0], # <- front from 0 height 
        [-1, 1, 0], 
        [0, 1, 0], # <- side1
        [1, 1, 0],  
        [1, 0, 0], # <- back
        [1, -1, 0],
        [0, -1, 0], # <- side2
        [-1, -1, 0],
        [-1, 0, 1], # from above
        [-1, 1, 1], 
        [0, 1, 1], 
        [1, 1, 1],  
        [1, 0, 1], 
        [1, -1, 1],
        [0, -1, 1],
        [-1, -1, 1],
        [0, 0, -1], #From directly below
        [0, 0, 1] #From directly above
    ])
    camViewUp = np.matlib.repmat(np.array([0, 0, 1]),24, 1) # Allmost all views have the same camera "up-vector" (z). 
    camViewUp = np.append(camViewUp, [[0, 1, 0],[0, 1, 0]], axis=0) # Directly above, and below have y as "up-vector". 
    camParProj = False # Sets camera rendering to parallel Projection if True, Perspective projection if false. 

    return camPos, camViewUp, camParProj

def setCameraProj(camera, bool_):
    if bool_:
        camera.ParallelProjectionOn()
    else:
        camera.ParallelProjectionOff()
    return camera

